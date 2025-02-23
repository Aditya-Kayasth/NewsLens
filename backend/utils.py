import json
import requests
from bs4 import BeautifulSoup

# ✅ Load JSON file
def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# ✅ Save JSON file
def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ✅ Extract article text from URL
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        return " ".join([para.get_text() for para in paragraphs])[:2000]
    except Exception as e:
        return f"Error fetching article: {str(e)}"
