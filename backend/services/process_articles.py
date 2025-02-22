import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load NLP models only once to optimize performance
nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = SentimentIntensityAnalyzer()

def analyze_content(text: str):
    doc = nlp(text)
    return {
        "sentiment": sentiment_analyzer.polarity_scores(text),
        "entities": {ent.text: ent.label_ for ent in doc.ents},
        "keywords": [chunk.text for chunk in doc.noun_chunks]
    }

def process_article(article: dict):
    description = article.get("description")
    if not description:
        return None
    
    return {
        "title": article.get("title", "Untitled Article"),
        "source": article.get("source_id", "Unknown source"),
        "description": description,
        "url": article.get("link", "#"),
        "published_date": article.get("pubDate", ""),
        "analysis": analyze_content(description)
    }
