import aiohttp
import asyncio
import spacy
import logging
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils import extract_text_from_url


# ✅ Load NLP Models
nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = SentimentIntensityAnalyzer()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

NEWS_API_KEY = "pub_713126568809cbb479e396fcef2b6c9d38644"
NEWS_API_URL = "https://newsdata.io/api/1/news"

class NewsFetcher:
    async def fetch_news(self, query, country):
        params = {
            "apikey": NEWS_API_KEY,
            "q": query,
            "country": country.lower(),
            "language": "en",
            "size": 10
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(NEWS_API_URL, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("results", [])
            except Exception as e:
                logging.error(f"API Error: {str(e)}")
        return []

    def get_news(self, query, country):
        return asyncio.run(self.fetch_news(query, country))  # ✅ Fix: Use asyncio.run()

    def process_article(self, article):
        description = article.get("description", "")
        if not description:
            return None
        
        return {
            "title": article.get("title", "Untitled"),
            "source": article.get("source_id", "Unknown"),
            "description": description,
            "url": article.get("link", "#"),
            "published_date": article.get("pubDate", ""),
            "analysis": self.analyze_text(description)
        }

    def analyze_text(self, text):
        doc = nlp(text)
        return {
            "sentiment": sentiment_analyzer.polarity_scores(text),
            "entities": {ent.text: ent.label_ for ent in doc.ents},
            "keywords": [chunk.text for chunk in doc.noun_chunks]
        }

    def generate_summary(self, url):
        article_text = extract_text_from_url(url)
        if "Error" in article_text:
            return article_text, []

        summary = summarizer(article_text, max_length=150, min_length=50, do_sample=False)
        return summary[0]["summary_text"], [url]  # URL as citation
