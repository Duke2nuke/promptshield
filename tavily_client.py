"""Tavily enrichment for PromptShield.

If TAVILY_API_KEY is set, this calls the Tavily Search API for recent
prompt injection techniques. If no key is set, it returns a clearly
labelled curated fallback list, not fake live search results.
"""
import os
import requests

FALLBACK = [
    {"title": "OWASP Top 10 for LLM Applications: Prompt Injection", "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/"},
]


def search_latest():
    key = os.environ.get("TAVILY_API_KEY")
    if not key:
        return {"live": False, "mode": "fallback", "results": FALLBACK, "note": "No Tavily API key set. Showing curated fallback links, not live Tavily results."}
    try:
        r = requests.post(
            "https://api.tavily.com/search",
            headers={"Content-Type": "application/json"},
            json={"api_key": key, "query": "prompt injection LLM security techniques 2026", "max_results": 5},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        results = [{"title": x.get("title"), "url": x.get("url")} for x in data.get("results", [])]
        return {"live": True, "mode": "tavily", "results": results}
    except Exception as e:  # noqa: BLE001
        return {"live": False, "mode": "fallback_after_error", "results": FALLBACK, "note": f"Tavily call failed ({e}). Showing fallback links."}
