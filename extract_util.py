import io
import re
import requests
import trafilatura
from typing import Optional
from pypdf import PdfReader

USER_AGENT = "ai-agent-intern/1.0"

def is_probable_pdf_url(url: str) -> bool:
    return url.lower().endswith(".pdf")

def extract_pdf_text_from_bytes(pdf_bytes: bytes, max_pages: int = 15) -> str:
    """
    Extract text from first max_pages to keep prompts manageable.
    """
    reader = PdfReader(io.BytesIO(pdf_bytes))
    texts = []
    for i, page in enumerate(reader.pages[:max_pages]):
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        if txt:
            texts.append(txt.strip())
    return "\n\n".join(texts).strip()

def extract_content(url: str, timeout: int = 20) -> str:
    """
    Returns cleaned text from HTML or PDF. Empty string if unavailable.
    """
    try:
        # Try HEAD to detect content-type
        head = requests.head(url, headers={"User-Agent": USER_AGENT}, allow_redirects=True, timeout=10)
        ctype = head.headers.get("Content-Type", "").lower()
    except requests.RequestException:
        ctype = ""

    try:
        if "application/pdf" in ctype or is_probable_pdf_url(url):
            r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
            r.raise_for_status()
            return extract_pdf_text_from_bytes(r.content)

        # HTML path via Trafilatura (can also auto-fetch)
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            # Fallback: manual GET then extract
            resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
            resp.raise_for_status()
            downloaded = resp.text

        extracted = trafilatura.extract(downloaded, include_comments=False, include_images=False)
        if not extracted:
            return ""
        cleaned = re.sub(r"\n{3,}", "\n\n", extracted).strip()
        return cleaned
    except requests.RequestException as e:
        print(f"[extract_content] HTTP error for {url}: {e}")
        return ""
    except Exception as e:
        print(f"[extract_content] Parse error for {url}: {e}")
        return ""