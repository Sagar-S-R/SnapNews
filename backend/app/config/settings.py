import os
from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # News API
    NEWSAPI_KEY: Optional[str] = None
    NEWSAPI_BASE_URL: str = "https://newsapi.org/v2"
    
    # Model settings
    SUMMARIZER_MODEL: str = "facebook/bart-large-cnn"
    MAX_INPUT_LENGTH: int = 1024
    MAX_OUTPUT_LENGTH: int = 150
    MIN_OUTPUT_LENGTH: int = 50
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()