from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from utils import load_json, save_json
import os
import jwt
import bcrypt
import json
import requests
import pyttsx3
import uuid
import nltk
from modules.news_api import get_articles, top_headlines
from modules.content import fetch_full_content
from modules.sentiment import analyze_sentiments
from modules.summarizer import related_articles_content, mmr_summarizer
from modules.content import clean_and_format_content
from modules.scrape_article import scrape_article
from modules.readaloud import process_article_read_aloud
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://192.168.55.182:3000"]}})
USERS_FILE = "data/users.json"

SECRET_KEY = "your_secret_key_here"

if not os.path.exists("data"):
    os.makedirs("data")
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "a41360b0efc146388b0db0a7051b7e4f")


AUDIO_FOLDER = os.path.join('static', 'audio')

if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {"users": []}
    return {"users": []}

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=2)

# Signup route
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    
    if not all(k in data for k in ("name", "email", "password", "location")):
        return jsonify({"error": "Missing required fields"}), 400

    users = load_users()

    # Check if email already exists
    if any(user["email"] == data["email"] for user in users["users"]):
        return jsonify({"error": "User already exists"}), 400
    
    # Hash password
    hashed_pw = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
    
    new_user = {
        "name": data["name"],
        "email": data["email"],
        "password": hashed_pw,
        "location": data["location"],
        "preferred_domains": []  # Empty at signup
    }
    
    users["users"].append(new_user)
    save_users(users)
    
    return jsonify({"message": "User registered successfully. Redirecting to preferences page...", "redirect": "/preferences"}), 201

# Login route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    users = load_users()

    user = next((u for u in users["users"] if u["email"] == email), None)
    
    if not user or not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {"email": email, "exp": datetime.utcnow() + timedelta(hours=2)},
        SECRET_KEY,
        algorithm="HS256"
    )

    
    return jsonify({"token": token, "redirect": "/news-home"})


def verify_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["email"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Preferences route
@app.route("/preferences", methods=["POST", "OPTIONS"])
def update_preferences():
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight request success"}), 200

    data = request.get_json()
    email = data.get("email")
    preferences = data.get("preferred_domains", [])

    users = load_users()
    for user in users["users"]:
        if user["email"] == email:
            user["preferred_domains"] = preferences
            save_users(users)
            return jsonify({"message": "Preferences updated successfully!"}), 200

    return jsonify({"error": "User not found"}), 404

# Search route
@app.route("/search", methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')  

    if not query:
        return jsonify({"error": "Search query is required."}), 400

    from_date = (datetime.utcnow() - timedelta(days=5)).strftime('%Y-%m-%d')

    params = {
        'q': query,  
        'from': from_date,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 10,
        'apiKey': NEWSAPI_KEY
    }

    api_response = get_articles(params)
    api_response = fetch_full_content(api_response)
    api_response = analyze_sentiments(api_response)
    return jsonify({"articles": api_response})

# news-home route
@app.route('/news', methods=['POST'])
def fetch_news():
    data = request.get_json()  
    email = data.get("email")  

    with open(USERS_FILE, "r") as file:
        users = json.load(file)["users"]

    user = next((u for u in users if u["email"] == email), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    topics = user.get("preferred_domains", [])  

    if not topics:
        return jsonify({"error": "At least one topic is required."}), 400

    query = ' OR '.join(topics)
    from_date = (datetime.utcnow() - timedelta(days=3)).strftime('%Y-%m-%d')

    params = {
        'q': query,
        'from': from_date,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 20,
        'apiKey': NEWSAPI_KEY
    }

    api_response = get_articles(params)
    
    api_response = fetch_full_content(api_response)
    
    api_response = analyze_sentiments(api_response)
    # print(api_response)

    return jsonify({"articles": api_response})

# top route
@app.route("/top", methods=['GET'])
def top():
    params = {
        'country': 'us',
        'apiKey': NEWSAPI_KEY
    }

    api_response = top_headlines(params)
    api_response = fetch_full_content(api_response)
    api_response = analyze_sentiments(api_response)

    return jsonify({"top_headlines": api_response})

# checkbias route
@app.route("/checkb", methods=['GET', 'POST'])
def checkb():
    if request.method == 'POST':
        article_url = request.form.get('article_url')  
        if not article_url:
            return jsonify({"error": "Article URL is required."}), 400
        
        docs, query = related_articles_content(article_url, NEWSAPI_KEY) 

        if not docs:
            return jsonify({"error": "No related articles found."}), 404  
    
        related_articles_summary = mmr_summarizer(docs, query=query, summary_length=5)
        return jsonify({"summary": related_articles_summary})
    
    return jsonify({"message": "Send a POST request with 'article_url'."}), 405

# read_article route
@app.route("/read_article", methods=['GET', 'POST'])
def read_article():
    if request.method == 'POST':
        data = request.json  
        article_url = data.get('article_url')
        
        try:
            voice_index = int(data.get('voice_index', 0))
        except (ValueError, TypeError):
            voice_index = 0

        if not article_url:
            return jsonify({"error": "Article URL is required."}), 400

        formatted_text, audio_filename, error = process_article_read_aloud(article_url, voice_index)
        if error:
            return jsonify({"error": error}), 400
        
        audio_url = url_for('static', filename=f"audio/{audio_filename}", _external=True)

        return jsonify({
            "article_text": formatted_text,
            "audio_url": audio_url,
            "article_url": article_url
        })

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    voice_list = [{"id": i, "name": v.name} for i, v in enumerate(voices)]
    return jsonify({"voices": voice_list})


if __name__ == '__main__':
    app.run(debug=True)