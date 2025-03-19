import os
import uuid
import pyttsx3
from modules.scrape_article import scrape_article
from modules.content import clean_and_format_content

# Define folder to store generated audio files
AUDIO_FOLDER = os.path.join('static', 'audio')
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

def process_article_read_aloud(article_url, voice_index=0):
    """
    Process an article URL to scrape, clean, and convert it to speech.
    Returns a tuple of (formatted_text, audio_filename, error_message).
    """
    # Scrape the article content
    raw_content = scrape_article(article_url)
    if not raw_content:
        return None, None, "Could not fetch the article."
    
    # Clean and format the article content
    formatted_text = clean_and_format_content(raw_content)
    
    # Initialize pyttsx3 engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Select the voice based on the provided index (fallback to the first voice)
    if voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    else:
        engine.setProperty('voice', voices[0].id)
    
    # Save the speech output to a file
    output_filename = f"{uuid.uuid4().hex}.wav"
    output_filepath = os.path.join(AUDIO_FOLDER, output_filename)
    engine.save_to_file(formatted_text, output_filepath)
    engine.runAndWait()
    
    return formatted_text, output_filename, None
