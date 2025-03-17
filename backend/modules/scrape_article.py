import logging
from bs4 import BeautifulSoup
import requests


HEADERS = {

    "User-Agent": (
        
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}


def scrape_article(url):
    """
    Given an article URL, fetch and return the article content.
    Extracts text from <p> tags.
    """
    try:

        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        article_text = "\n".join(p.get_text() for p in paragraphs)
        
        return article_text.strip()
    
    except Exception as e:

        logging.error(f"Error scraping article at {url}: {e}")
        return ""