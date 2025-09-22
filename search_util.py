import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

def web_search(query: str, k: int = 3) -> List[Dict[str, str]]:
    """
    Call SerpAPI (Google Search) and return up to k results
    as [{"title":..., "url":...}, ...].
    """
    
    serp_key = os.getenv("SERPAPI_KEY")
    if not serp_key:
        raise RuntimeError("SERPAPI_KEY not set. Please configure your .env.")

    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "num": k,
        "api_key": serp_key,
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("organic_results", []):
            title = item.get("title")
            link = item.get("link")
            if title and link:
                results.append({"title": title, "url": link})
            if len(results) >= k:
                break
        return results

    except requests.RequestException as e:
        print(f"[web_search] SerpAPI error: {e}")
        return []