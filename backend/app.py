from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
import os
import uuid
import pyttsx3

from modules.news_api import get_articles, top_headlines
from modules.content import fetch_full_content
from modules.sentiment import analyze_sentiments
from modules.summarizer import related_articles_content, mmr_summarizer
from modules.content import clean_and_format_content
from modules.scrape_article import scrape_article
from modules.readaloud import process_article_read_aloud

# You can still have your alternative TTS function if needed:
# from modules.readout_loud import read_article_with_gtts, read_article_with_pyttsx3

app = Flask(__name__)

# Load configuration (you can set NEWSAPI_KEY as an environment variable)
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "a41360b0efc146388b0db0a7051b7e4f")

# Folder to store generated audio files
AUDIO_FOLDER = os.path.join('static', 'audio')
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

# Home route to show the input form for preferences
@app.route('/', methods=['GET', 'POST'])
def input_form():
    categories = ['Sports', 'Entertainment', 'Politics', 'Education', 'Health', 'Finance', 'Technology', 'Science']

    if request.method == 'POST':
        topics = request.form.getlist('topics')
        query = ' OR '.join(topics)  # Concatenate all the topics
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
        

        return render_template('display_results.html', api_response=api_response, topic=query)
    
    return render_template('input_form.html', categories=categories)


# Search route to search for articles by a topic
@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        topic = request.form.get('topic', '')
        from_date = (datetime.utcnow() - timedelta(days=5)).strftime('%Y-%m-%d')

        params = {
            'q': topic,
            'from': from_date,
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 10,
            'apiKey': NEWSAPI_KEY

        }

        api_response = get_articles(params)
        api_response = fetch_full_content(api_response)
        api_response = analyze_sentiments(api_response)

        return render_template('display_results.html', api_response=api_response, topic=topic)
    
    return render_template("search.html")


# Top news route to display top headlines
@app.route("/top", methods=['GET'])
def top():
    params = {
        'country': 'us',
        'apiKey': NEWSAPI_KEY
    }

    api_response = top_headlines(params)
    api_response = fetch_full_content(api_response)
    api_response = analyze_sentiments(api_response)

    return render_template('display_results.html', api_response=api_response, topic="Top Headlines")


# Summarize route for related articles summary using an article URL
@app.route("/checkb", methods=['GET', 'POST'])
def checkb():
    if request.method == 'POST':
        article_url = request.form.get('article_url')  # Article URL Check
        if not article_url:
            return "Article URL is required.", 400
        
        docs, query, info = related_articles_content(article_url, NEWSAPI_KEY)  # Related articles content

        if not docs and docs:
            return "No related articles found."  # Related Articles Check
    
        related_articles_summary = mmr_summarizer(docs, query=query, summary_length=5, info = info)
        return render_template('display_results.html', api_response=related_articles_summary, topic="Summary")
    
    return render_template("checkb.html")


# New route: Read article aloud and display its text with audio controls
@app.route("/read_article", methods=['GET', 'POST'])
def read_article():
    if request.method == 'POST':
        article_url = request.form.get('article_url')
        try:
            voice_index = int(request.form.get('voice_index', 0))
        except ValueError:
            voice_index = 0

        if not article_url:
            return "Article URL is required.", 400
        
        # Process the article using the function in readaloud.py
        formatted_text, audio_filename, error = process_article_read_aloud(article_url, voice_index)
        if error:
            return error, 400
        
        audio_url = url_for('static', filename=f"audio/{audio_filename}")
        
        # Render a page that shows the article text and an audio player with controls
        return render_template('display_read_article.html', 
                               article_text=formatted_text, 
                               audio_url=audio_url, 
                               article_url=article_url)
    
    # For GET request, list available voices for selection.
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return render_template('read_article.html', voices=voices)

if __name__ == '__main__':
    app.run(debug=True)


