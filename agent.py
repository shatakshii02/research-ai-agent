import os
from typing import List, Tuple

from dotenv import load_dotenv
from groq import Groq 

from search_util import web_search
from extract_util import extract_content
from db_util import save_report
from prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# Load .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

# Read Groq config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set. Please configure your .env.")

client = Groq(api_key=GROQ_API_KEY)

def gather_sources(query: str, k: int = 3) -> List[Tuple[str, str, str]]:
    """
    Returns list of (title, text, url) for up to k valid sources.
    """
    results = web_search(query, k=max(4, k))  # fetch a few extra in case of skips
    gathered = []
    for res in results:
        title, url = res["title"], res["url"]
        text = extract_content(url)
        if text and len(text.split()) > 120:  # ensure some substance
            gathered.append((title, text, url))
        if len(gathered) >= k:
            break
    return gathered

def summarize_with_llm(query: str, sources: List[Tuple[str, str, str]]) -> str:
    """
    Build a markdown report with bullets and hyperlinks using Groq LLaMA3.
    """
    # Build a trimmed sources block to avoid overlong prompts
    src_blocks = []
    for i, (title, text, url) in enumerate(sources, start=1):
        trimmed = text[:4000]  # keep within Groq LLaMA3 input size
        src_blocks.append(f"[{i}] {title} ({url})\n{trimmed}\n")
    sources_blob = "\n\n".join(src_blocks) if src_blocks else "(No usable sources.)"

    user_prompt = USER_PROMPT_TEMPLATE.format(query=query, sources=sources_blob)

    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=700,
    )
    return resp.choices[0].message.content.strip()

def generate_report(query: str) -> str:
    """
    Main pipeline: search → extract → summarize → save → return summary text.
    """
    sources = gather_sources(query, k=3)
    if not sources:
        summary = "⚠️ I couldn’t retrieve useful content for this query. Please try a more specific query."
        save_report(query, summary)
        return summary

    summary = summarize_with_llm(query, sources)

    # Post-process: ensure at least some links included (best-effort)
    if all("http" not in summary for _ in [0]):
        links = "\n".join([f"- [{t}]({u})" for (t, _, u) in sources])
        summary += "\n\n**Sources:**\n" + links

    save_report(query, summary)
    return summary