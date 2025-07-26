import httpx
import logging
from typing import List, Optional
from app.config.settings import settings
from app.models.schemas import NewsArticle, NewsSearchResponse
import asyncio

logger = logging.getLogger(__name__)

class NewsService:
    """Service to fetch news from NewsAPI"""
    
    def __init__(self):
        self.base_url = settings.NEWSAPI_BASE_URL
        self.api_key = settings.NEWSAPI_KEY
        
        if not self.api_key:
            logger.warning("NEWSAPI_KEY not found in environment variables")
    
    async def search_news(self, query: str, page_size: int = 10, language: str = "en") -> NewsSearchResponse:
        """
        Search for news articles using NewsAPI
        
        Args:
            query (str): Search query
            page_size (int): Number of articles to fetch (max 20 for free tier)
            language (str): Language code (e.g., 'en', 'es', 'fr')
            
        Returns:
            NewsSearchResponse: Response containing news articles
        """
        if not self.api_key:
            return NewsSearchResponse(
                articles=[],
                total_results=0,
                status="error",
                message="NewsAPI key not configured"
            )
        
        url = f"{self.base_url}/everything"
        params = {
            "q": query,
            "apiKey": self.api_key,
            "language": language,
            "pageSize": min(page_size, 20),  # NewsAPI free tier limit
            "sortBy": "publishedAt"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "ok":
                    articles = []
                    for article_data in data.get("articles", []):
                        article = NewsArticle(
                            title=article_data.get("title", ""),
                            description=article_data.get("description"),
                            content=article_data.get("content"),
                            url=article_data.get("url", ""),
                            url_to_image=article_data.get("urlToImage"),
                            published_at=article_data.get("publishedAt"),
                            source=article_data.get("source", {}).get("name")
                        )
                        articles.append(article)
                    
                    return NewsSearchResponse(
                        articles=articles,
                        total_results=data.get("totalResults", 0),
                        status="ok"
                    )
                else:
                    error_message = data.get("message", "Unknown error from NewsAPI")
                    logger.error(f"NewsAPI error: {error_message}")
                    return NewsSearchResponse(
                        articles=[],
                        total_results=0,
                        status="error",
                        message=error_message
                    )
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error when fetching news: {e}")
            return NewsSearchResponse(
                articles=[],
                total_results=0,
                status="error",
                message=f"HTTP error: {e.response.status_code}"
            )
        except Exception as e:
            logger.error(f"Unexpected error when fetching news: {str(e)}")
            return NewsSearchResponse(
                articles=[],
                total_results=0,
                status="error",
                message=f"Unexpected error: {str(e)}"
            )
    
    async def get_top_headlines(self, category: Optional[str] = None, country: str = "us", page_size: int = 10) -> NewsSearchResponse:
        """
        Get top headlines from NewsAPI
        
        Args:
            category (str, optional): News category (business, entertainment, general, health, science, sports, technology)
            country (str): Country code (e.g., 'us', 'gb', 'in')
            page_size (int): Number of articles to fetch
            
        Returns:
            NewsSearchResponse: Response containing news articles
        """
        if not self.api_key:
            return NewsSearchResponse(
                articles=[],
                total_results=0,
                status="error",
                message="NewsAPI key not configured"
            )
        
        url = f"{self.base_url}/top-headlines"
        params = {
            "apiKey": self.api_key,
            "country": country,
            "pageSize": min(page_size, 20)
        }
        
        if category:
            params["category"] = category
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "ok":
                    articles = []
                    for article_data in data.get("articles", []):
                        article = NewsArticle(
                            title=article_data.get("title", ""),
                            description=article_data.get("description"),
                            content=article_data.get("content"),
                            url=article_data.get("url", ""),
                            url_to_image=article_data.get("urlToImage"),
                            published_at=article_data.get("publishedAt"),
                            source=article_data.get("source", {}).get("name")
                        )
                        articles.append(article)
                    
                    return NewsSearchResponse(
                        articles=articles,
                        total_results=data.get("totalResults", 0),
                        status="ok"
                    )
                else:
                    error_message = data.get("message", "Unknown error from NewsAPI")
                    logger.error(f"NewsAPI error: {error_message}")
                    return NewsSearchResponse(
                        articles=[],
                        total_results=0,
                        status="error",
                        message=error_message
                    )
                    
        except Exception as e:
            logger.error(f"Error fetching top headlines: {str(e)}")
            return NewsSearchResponse(
                articles=[],
                total_results=0,
                status="error",
                message=f"Error: {str(e)}"
            )

# Global news service instance
news_service = NewsService()