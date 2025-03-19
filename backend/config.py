import os

NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "a41360b0efc146388b0db0a7051b7e4f")

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")
TOKEN_EXPIRY_HOURS = 24
