from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: str
    url_to_image: Optional[str] = None
    published_at: Optional[str] = None
    source: Optional[str] = None

class NewsSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="Search query for news")
    page_size: Optional[int] = Field(default=10, ge=1, le=20, description="Number of articles to fetch")
    language: Optional[str] = Field(default="en", description="Language code")

class NewsSearchResponse(BaseModel):
    articles: List[NewsArticle]
    total_results: int
    status: str
    message: Optional[str] = None

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description="Text content to summarize")
    max_length: Optional[int] = Field(default=150, ge=50, le=300, description="Maximum summary length")
    min_length: Optional[int] = Field(default=50, ge=20, le=100, description="Minimum summary length")

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    processing_time: float

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int