import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from flask import jsonify

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from modules.scrape_article import scrape_article
from modules.news_api import get_articles
from modules.content import clean_and_format_content

from datetime import datetime, timedelta
import json

# Download NLTK resources if not already present
nltk.download('punkt')
nltk.download('stopwords')


def extract_keywords(text, num_keywords=5):
    """
    Extract keywords from text using NLTK frequency distribution.
    """
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    freq = nltk.FreqDist(filtered_words)
    most_common = freq.most_common(num_keywords)
    keywords = [word for word, _ in most_common]
    print(f"Extracted Keywords: {keywords}")  # Debug print
    return keywords


def related_articles_content(article_url, NEWSAPI_KEY):
    """
    Given an article URL, scrape its content, extract keywords,
    use them to fetch related articles from the news API, and return a list of cleaned contents.
    """
    content = scrape_article(article_url)  # Get the original article content

    if content:
        # Extract keywords from the main article
        keywords = extract_keywords(content)
        # Use the keywords to form a search query
        query = ' '.join(keywords)
        print(f"Search Query: {query}")  # Debug print

        from_date = (datetime.utcnow() - timedelta(days=2)).strftime('%Y-%m-%d')

        params = {
            'q': query,
            'from': from_date,
            'language': 'en',
            'sortBy': 'relevancy',
            'pageSize': 10,
            'apiKey': NEWSAPI_KEY
        }

        related_articles_api_response = get_articles(params)
        related_articles = related_articles_api_response.get('articles', [])
        print(f"Number of related articles found: {len(related_articles)}")  # Debug print

        docs = []
        info = []

        for article in related_articles:
            url = article.get('url')
        
            title = article.get('title')
            
            info.append({'title':title,'url':url})
            # Scrape each related article's content
            content = scrape_article(url)
            if content:
                # Clean and format the content using BeautifulSoup & regex
                formatted_content = clean_and_format_content(content)
                if formatted_content:
                    docs.append(formatted_content)
        
            #docs.append()
        print(f"Number of documents for summarization: {len(docs)}")  # Debug print
        return docs, query, info  # Return both the docs and the query for summarization

    return None, None, None


def mmr_summarizer(docs, query=None, lambda_param=0.5, summary_length=6, related= None, info=None):
    """
    Extractive summarization using Maximal Marginal Relevance (MMR).
    Returns a dictionary with the selected summary sentences.
    """
    # Tokenize each document into sentences
    sentences = [sent_tokenize(doc) for doc in docs if doc]

    # Flatten the list of lists
    sentences = [s for sublist in sentences for s in sublist]
    print(f"Total number of sentences: {len(sentences)}")  # Debug print

    if not sentences:
        return {'articles': [{'title': 'Summary', 'description': 'No sentences available for summarization.'}]}
    
    # Create a TF-IDF representation of the sentences
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)
    sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    summary_indices = []
    candidate_indices = list(range(len(sentences)))
    
    for _ in range(min(summary_length, len(candidate_indices))):
        mmr_scores = []
        for i in candidate_indices:
            relevance = 0
            if query:
                query_vec = vectorizer.transform([query])
                # Calculate cosine similarity between sentence and query vector
                relevance = cosine_similarity(tfidf_matrix[i], query_vec)[0][0]
            
            diversity = max([sim_matrix[i][j] for j in summary_indices], default=0)
            mmr_score = lambda_param * relevance - (1 - lambda_param) * diversity
            mmr_scores.append((mmr_score, i))

        if mmr_scores:
            # Select the sentence with the highest MMR score
            _, selected_idx = max(mmr_scores)
            summary_indices.append(selected_idx)
            candidate_indices.remove(selected_idx)

    summary_sentences = [sentences[idx] for idx in summary_indices]
    summary = ' '.join(summary_sentences)
    print(f"Generated Summary: {summary}")  # Debug print
   ## print(f"===================={info}=================================")

    return {'articles': [{'title': 'Summary', 'description': summary , 'info':info}]}