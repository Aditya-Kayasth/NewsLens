from modules.scrape_article import scrape_article
from bs4 import BeautifulSoup
import re
from datetime import datetime

def clean_and_format_content(raw_content):
    """
    Cleans and formats raw HTML content.
    Parses the HTML, extracts text with newline separators, 
    cleans extra whitespace, and returns well-formatted text.
    """
    # Parse the HTML content
    soup = BeautifulSoup(raw_content, "html.parser")
    
    # Extract text using newline as separator to preserve paragraph breaks
    text = soup.get_text(separator="\n")
    
    # Split the text into lines, clean each line, and remove empty lines
    paragraphs = [re.sub(r'\s+', ' ', para).strip() for para in text.splitlines() if para.strip()]
    
    # Join cleaned paragraphs with double newlines for clear separation
    formatted_text = "\n\n".join(paragraphs)
    return formatted_text

def fetch_full_content(api_response):
    """
    For each article in the API response, scrape, clean, and attach the full content.
    Also, parse and separate the publishedAt field into date and time.
    """
    for article in api_response.get('articles', []):
        # Process the article content
        url = article.get('url')
        if url:
            try:
                raw_content = scrape_article(url)
                formatted_content = clean_and_format_content(raw_content)
                article['content'] = formatted_content
            except Exception as e:
                article['content'] = None
        else:
            article['content'] = None

        # Process the publishedAt field
        published_at = article.get('publishedAt')
        if published_at:
            try:
                # Parse the ISO 8601 datetime string (e.g., "2025-03-10T19:08:20Z")
                dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                article['published_date'] = dt.strftime("%Y-%m-%d")
                article['published_time'] = dt.strftime("%H:%M:%S")
            except Exception as e:
                # Fallback: if parsing fails, assign the original value and an empty time
                article['published_date'] = published_at
                article['published_time'] = ""
        else:
            article['published_date'] = ""
            article['published_time'] = ""

    return api_response
