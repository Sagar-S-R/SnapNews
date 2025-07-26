from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.schemas import (
    NewsSearchRequest, NewsSearchResponse, 
    SummarizeRequest, SummarizeResponse,
    HealthResponse, ErrorResponse
)
from app.services.news_service import news_service
from app.models.summarizer import get_summarizer
from app.utils.helpers import clean_text, extract_text_from_url_async, prepare_text_for_summarization
import logging
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        summarizer = get_summarizer()
        model_status = summarizer.is_model_loaded()
        
        return HealthResponse(
            status="healthy" if model_status else "unhealthy",
            timestamp=datetime.now(),
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Service unavailable")

@router.post("/news/search", response_model=NewsSearchResponse)
async def search_news(request: NewsSearchRequest):
    """
    Search for news articles
    
    Args:
        request: NewsSearchRequest containing search parameters
        
    Returns:
        NewsSearchResponse: List of news articles
    """
    try:
        logger.info(f"Searching news for query: {request.query}")
        
        result = await news_service.search_news(
            query=request.query,
            page_size=request.page_size,
            language=request.language
        )
        
        logger.info(f"Found {len(result.articles)} articles for query: {request.query}")
        return result
        
    except Exception as e:
        logger.error(f"Error searching news: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search news: {str(e)}"
        )

@router.get("/news/headlines", response_model=NewsSearchResponse)
async def get_top_headlines(category: str = None, country: str = "us", page_size: int = 10):
    """
    Get top headlines
    
    Args:
        category: News category (optional)
        country: Country code (default: us)
        page_size: Number of articles to fetch
        
    Returns:
        NewsSearchResponse: List of top headlines
    """
    try:
        logger.info(f"Fetching top headlines for category: {category}, country: {country}")
        
        result = await news_service.get_top_headlines(
            category=category,
            country=country,
            page_size=page_size
        )
        
        logger.info(f"Found {len(result.articles)} headlines")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching headlines: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch headlines: {str(e)}"
        )

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    """
    Summarize the provided text using BART model
    
    Args:
        request: SummarizeRequest containing text and parameters
        
    Returns:
        SummarizeResponse: Summary and metadata
    """
    try:
        logger.info("Starting text summarization")
        
        # Get the summarizer instance
        summarizer = get_summarizer()
        
        # Prepare text for summarization
        prepared_text = prepare_text_for_summarization(request.text)
        
        if len(prepared_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Text too short for summarization (minimum 50 characters required)"
            )
        
        # Generate summary
        result = summarizer.summarize(
            text=prepared_text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
        return SummarizeResponse(
            summary=result["summary"],
            original_length=result["original_length"],
            summary_length=result["summary_length"],
            processing_time=result["processing_time"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )

@router.post("/summarize-url", response_model=SummarizeResponse)
async def summarize_from_url(url: str, max_length: int = 150, min_length: int = 50):
    """
    Extract text from URL and summarize it
    
    Args:
        url: URL of the article to summarize
        max_length: Maximum summary length
        min_length: Minimum summary length
        
    Returns:
        SummarizeResponse: Summary and metadata
    """
    try:
        logger.info(f"Extracting and summarizing text from URL: {url}")
        
        # Extract text from URL
        extracted_text = await extract_text_from_url_async(url)
        
        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the provided URL"
            )
        
        # Create summarize request
        request = SummarizeRequest(
            text=extracted_text,
            max_length=max_length,
            min_length=min_length
        )
        
        # Use the existing summarize endpoint
        return await summarize_text(request)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error summarizing from URL: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process URL: {str(e)}"
        )

@router.get("/news/categories")
async def get_news_categories():
    """
    Get available news categories
    
    Returns:
        dict: Available news categories
    """
    categories = {
        "business": "Business news and finance",
        "entertainment": "Entertainment and celebrity news",
        "general": "General news",
        "health": "Health and medical news",
        "science": "Science and technology",
        "sports": "Sports news",
        "technology": "Technology news"
    }
    
    return {"categories": categories}

@router.get("/news/countries")
async def get_supported_countries():
    """
    Get supported country codes for news
    
    Returns:
        dict: Supported countries
    """
    countries = {
        "us": "United States",
        "gb": "United Kingdom",
        "ca": "Canada",
        "au": "Australia",
        "in": "India",
        "de": "Germany",
        "fr": "France",
        "jp": "Japan",
        "cn": "China",
        "br": "Brazil"
    }
    
    return {"countries": countries}