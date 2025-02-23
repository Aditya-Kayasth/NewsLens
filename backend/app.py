from flask import Flask, request, jsonify
from news_fetcher import NewsFetcher
from utils import load_json, save_json
import os

app = Flask(__name__)
news_fetcher = NewsFetcher()

# Ensure the 'data' directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# ✅ Route: Fetch news based on user preferences & location
@app.route("/fetch_news", methods=["GET"])
def fetch_news():
    user_prefs = request.args.getlist("topics") or []  # Ensure it's a list
    location = request.args.get("location", "us")  # Default to US if not given
    
    news_data = {}

    for topic in user_prefs[:3]:  # Limit to 3 topics
        news_data[topic] = news_fetcher.get_news(topic, location) or []

    # Fetch top news in user's location
    news_data["top_news"] = news_fetcher.get_news("top", location) or []

    # Save to JSON
    save_json("data/news_data.json", news_data)

    return jsonify(news_data)

# ✅ Route: Perform a global search
@app.route("/search", methods=["GET"])
def search_news():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    search_results = news_fetcher.get_news(query, "global") or []

    # Save search results separately
    save_json("data/search_results.json", search_results)

    return jsonify(search_results)

# ✅ Route: Generate summary for clicked article
@app.route("/summarize", methods=["POST"])
def summarize_article():
    data = request.get_json() or {}  # Ensure it's a dict
    url = data.get("url")

    if not url:
        return jsonify({"error": "Article URL is required"}), 400

    try:
        summary, citations = news_fetcher.generate_summary(url)
        return jsonify({"summary": summary, "citations": citations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
