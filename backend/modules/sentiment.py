from textblob import TextBlob

def analyze_sentiments(api_response):
    """
    Analyze the sentiment of each article's content and attach the sentiment data.
    """
    for article in api_response.get('articles', []):
        content = article.get('content', '')

        if content:

            sentiment = TextBlob(content).sentiment

            polarity = sentiment.polarity
            subjectivity = sentiment.subjectivity

            if polarity < 0:
                sentiment_label = f"{abs(round(polarity * 100,1))}% negative"
            elif polarity == 0:
                sentiment_label = "Neutral"
            else:
                sentiment_label = f"{round(polarity * 100,1)}% positive"

            subjectivity_label = f"{round((1 - subjectivity) * 100,1)}% fact-based | {round(subjectivity * 100,1)}% opinion-based"

            article['sentiment'] = {'Polarity': sentiment_label, 'Subjectivity': subjectivity_label}
        else:
            article['sentiment'] = {'Polarity': None, 'Subjectivity': None}
    
    return api_response
