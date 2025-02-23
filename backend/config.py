import os

NEWS_API_KEY = "pub_713126568809cbb479e396fcef2b6c9d38644"
NEWS_API_URL = "https://newsdata.io/api/1/news"

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")
TOKEN_EXPIRY_HOURS = 24
