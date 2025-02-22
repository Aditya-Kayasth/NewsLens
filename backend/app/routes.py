import asyncio
from flask import Blueprint, request, jsonify
from app.services.fetch_news import fetch_articles
from app.services.process_articles import process_article
from app.services.summarizer import extract_text_from_url, summarize_text

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return jsonify({"message": "Welcome to the News API!"})

@main_bp.route('/get_news', methods=['GET'])
def get_news():
    topic = request.args.get("topic", "technology")
    country = request.args.get("country", "us")
    
    # Create a new event loop to run asynchronous functions
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    articles = loop.run_until_complete(fetch_articles(topic, country))
    
    processed_articles = [process_article(a) for a in articles if a]
    results = [p for p in processed_articles if p is not None]
    
    return jsonify(results)

@main_bp.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get("url")
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    article_text = extract_text_from_url(url)
    if not article_text:
        return jsonify({"error": "Failed to extract article text"}), 400
    
    summary = summarize_text(article_text)
    return jsonify({"summary": summary})
