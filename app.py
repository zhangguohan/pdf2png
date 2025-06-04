from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import time

app = FastAPI()

SEARXNG_URL = "http://108.88.3.135:8081/search"
FIRECRAWL_URL = "http://108.88.3.135:3002/v1/crawl"

PLAYWRIGHT_SCRAPER_URL = "http://108.88.3.135:8083/fetch_web_content"

class QueryRequest(BaseModel):
    query: str
    max_results: int = 5


def fetch_firecrawl_content(url: str, max_wait: int = 80) -> str:
    try:
        resp = requests.post(
            PLAYWRIGHT_SCRAPER_URL,
            json={"url": url},
            timeout=max_wait
        )
        resp.raise_for_status()
        result = resp.json()
        #return result.get("content", "").strip()
        return result.get("text") or result.get("content", "")
    except Exception as e:
        print(f"[Playwright Error] URL: {url}, Error: {e}")
        return ""

@app.post("/fetch_web_content")
async def fetch_web_content(req: QueryRequest):
    params = {
        "q": req.query,
        "format": "json",
        "language": "zh-CN",
        "safesearch": 0,
        "time_range": "week"
    }

    try:
        searxng_response = requests.get(SEARXNG_URL, params=params, timeout=10)
        searxng_response.raise_for_status()
        results = searxng_response.json()
    except Exception as e:
        return {"error": f"搜索失败: {e}"}

    enriched_results = []
    for result in results.get("results", [])[:req.max_results]:
        title = result.get("title", "")
        url = result.get("url", "")
        content = fetch_firecrawl_content(url)
        enriched_results.append({
            "title": title,
            "url": url,
            "content": content
        })

    return {
        "query": req.query,
        "results": enriched_results
    }

