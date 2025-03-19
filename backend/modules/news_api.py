import os 
import requests

NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "793bd31b9d764aee827e466fcc6c01f0")

# Fetching News articles from API
def get_articles(params):

    response = requests.get(f"https://newsapi.org/v2/everything",params=params)
    
    return response.json()


# Fetching Top headlines
def top_headlines(params):

    response = requests.get('https://newsapi.org/v2/top-headlines', params=params)

    return response.json()