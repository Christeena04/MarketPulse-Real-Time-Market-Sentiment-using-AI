import httpx
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

async def get_news(ticker: str):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": ticker,
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        articles = res.json().get("articles", [])

        return [
            {
                "title": a["title"],
                "description": a["description"] or "",
                "url": a["url"]
            }
            for a in articles
        ]
