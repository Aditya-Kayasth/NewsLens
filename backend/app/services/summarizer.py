import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Initialize the summarization model (this might take a few seconds to load)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_url(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([para.get_text() for para in paragraphs])
        return text[:2000]  # Limit to first 2000 characters for summarization
    except Exception:
        return None

def summarize_text(text: str):
    try:
        summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
        return summary[0]["summary_text"]
    except Exception:
        return "No summary available."
