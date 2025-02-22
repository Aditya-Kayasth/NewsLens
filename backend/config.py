import os

class Config:
    # API and key configuration (use environment variables in production)
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "pub_713126568809cbb479e396fcef2b6c9d38644")
    NEWS_API_URL = os.getenv("NEWS_API_URL", "https://newsdata.io/api/1/news")
    
    # Country codes for filtering news
    COUNTRIES = {
        "India": "in", "USA": "us", "UK": "gb", "Canada": "ca", "Australia": "au",
        "Germany": "de", "France": "fr", "China": "cn", "Japan": "jp"
    }
