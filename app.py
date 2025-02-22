import os
import requests
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
from transformers import pipeline
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configurations
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)

# Load News API Key
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# Sentiment Analysis & Summarization Pipelines
sentiment_analysis = pipeline('sentiment-analysis')
summarizer = pipeline('summarization', model="facebook/bart-large-cnn")

# Bias Detection using Zero-Shot Classification (Hugging Face)
from transformers import pipeline
bias_detector = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Database Model: User Preferences
class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    preference = db.Column(db.String(50), nullable=False)

# Fetch News from NewsAPI
def fetch_news(domain):
    url = f'https://newsapi.org/v2/top-headlines?category={domain}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    return response.json()

# Analyze Bias in News Article
def analyze_bias(article_text):
    labels = ["left-leaning", "right-leaning", "neutral"]
    result = bias_detector(article_text, labels)
    return result

# Authentication Route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Dummy authentication (Replace with DB-based authentication)
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify(message='Invalid credentials'), 401

# News Fetching Route with User Preferences
@app.route('/news', methods=['GET'])
@jwt_required()
def get_news():
    domain = request.args.get('domain', 'general')  # Default to 'general' news
    news_data = fetch_news(domain)
    
    if news_data.get('status') != 'ok':
        return jsonify({'message': 'Failed to fetch news'}), 500

    return jsonify(news_data), 200

# Summarization Route
@app.route('/summarize', methods=['POST'])
@jwt_required()
def summarize_article():
    article_text = request.json.get('text')

    if not article_text:
        return jsonify({'error': 'No article text provided'}), 400

    summary = summarizer(article_text, max_length=100, min_length=50, do_sample=False)
    return jsonify({'summary': summary[0]['summary_text']}), 200

# Bias Detection Route
@app.route('/bias', methods=['POST'])
@jwt_required()
def detect_bias():
    article_text = request.json.get('text')

    if not article_text:
        return jsonify({'error': 'No article text provided'}), 400

    bias_result = analyze_bias(article_text)
    return jsonify({'bias': bias_result}), 200

# Initialize Database & Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
