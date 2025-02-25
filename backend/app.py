from flask import Flask, request, jsonify
from flask_cors import CORS
from news_fetcher import NewsFetcher
from utils import load_json, save_json
import os
import jwt
import bcrypt
import datetime
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://192.168.55.182:3000"]}})
USERS_FILE = "data/users.json"
news_fetcher = NewsFetcher()

SECRET_KEY = "your_secret_key_here"

# Ensure the 'data' directory exists
if not os.path.exists("data"):
    os.makedirs("data")

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

# ✅ Login Route (JWT Authentication)
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
        {"email": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
        SECRET_KEY,
        algorithm="HS256"
    )
    
    return jsonify({"token": token, "redirect": "/news-home"})

# ✅ Token Verification Function (Middleware)
def verify_token():
    token = request.headers.get("Authorization")
    if not token:
        return None
    try:
        decoded = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
        return decoded["email"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# ✅ Update Preferences Route
@app.route("/update_preferences", methods=["POST"])
def update_preferences():
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
