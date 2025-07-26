import re
import html
from typing import Optional
from urllib.parse import urlparse
import httpx
import asyncio
from newspaper import Article
import logging

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Clean and preprocess text content
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Remove any remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:\-\'"()]', '', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text

def extract_text_from_url(url: str, timeout: int = 10) -> Optional[str]:
    """
    Extract full article text from URL using newspaper3k
    
    Args:
        url (str): Article URL
        timeout (int): Request timeout in seconds
        
    Returns:
        Optional[str]: Extracted article text or None if failed
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        if article.text:
            return clean_text(article.text)
        else:
            logger.warning(f"No text extracted from URL: {url}")
            return None
            
    except Exception as e:
        logger.error(f"Error extracting text from URL {url}: {str(e)}")
        return None

async def extract_text_from_url_async(url: str, timeout: int = 10) -> Optional[str]:
    """
    Async version of extract_text_from_url
    
    Args:
        url (str): Article URL
        timeout (int): Request timeout in seconds
        
    Returns:
        Optional[str]: Extracted article text or None if failed
    """
    try:
        # Run the synchronous newspaper3k extraction in a thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, extract_text_from_url, url, timeout)
        return result
    except Exception as e:
        logger.error(f"Error in async text extraction from URL {url}: {str(e)}")
        return None

def validate_url(url: str) -> bool:
    """
    Validate if the provided string is a valid URL
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add if truncated
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    # Try to truncate at the last complete sentence
    truncated = text[:max_length - len(suffix)]
    last_sentence_end = max(
        truncated.rfind('.'),
        truncated.rfind('!'),
        truncated.rfind('?')
    )
    
    if last_sentence_end > max_length * 0.7:  # Only if we don't lose too much content
        return text[:last_sentence_end + 1]
    
    # Otherwise, truncate at the last word
    last_space = truncated.rfind(' ')
    if last_space > 0:
        return text[:last_space] + suffix
    
    return text[:max_length - len(suffix)] + suffix

def get_text_stats(text: str) -> dict:
    """
    Get basic statistics about the text
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Text statistics
    """
    if not text:
        return {
            "word_count": 0,
            "character_count": 0,
            "sentence_count": 0,
            "avg_words_per_sentence": 0.0
        }
    
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return {
        "word_count": len(words),
        "character_count": len(text),
        "sentence_count": len(sentences),
        "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0.0
    }

def prepare_text_for_summarization(text: str, max_input_length: int = 1024) -> str:
    """
    Prepare text for summarization by cleaning and truncating if necessary
    
    Args:
        text (str): Raw text
        max_input_length (int): Maximum input length for the model
        
    Returns:
        str: Prepared text
    """
    # Clean the text
    cleaned_text = clean_text(text)
    
    # If text is still too long, truncate it intelligently
    if len(cleaned_text.split()) > max_input_length:
        cleaned_text = truncate_text(cleaned_text, max_input_length * 5)  # rough character estimate
    
    return cleaned_text