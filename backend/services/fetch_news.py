import aiohttp
import logging
from config import Config

async def fetch_articles(query: str, country: str):
    params = {
        "apikey": Config.NEWS_API_KEY,
        "q": query,
        "country": country.lower(),
        "language": "en",
        "size": 10
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(Config.NEWS_API_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("results", [])
                else:
                    logging.error(f"Error {response.status}: {await response.text()}")
        except Exception as e:
            logging.error(f"Network error: {str(e)}")
    return []
