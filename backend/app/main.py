from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.api.routes.news import router as news_router
from app.models.summarizer import get_summarizer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler for startup and shutdown events
    """
    # Startup
    logger.info("Starting SnapNews API...")
    
    try:
        # Initialize the summarizer model on startup
        logger.info("Loading AI models...")
        summarizer = get_summarizer()
        if summarizer.is_model_loaded():
            logger.info("✅ AI models loaded successfully!")
        else:
            logger.error("❌ Failed to load AI models")
    except Exception as e:
        logger.error(f"❌ Error loading models: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SnapNews API...")

# Create FastAPI application
app = FastAPI(
    title="SnapNews API",
    description="AI-Powered News Summarizer & Reader API built with FastAPI and HuggingFace BART",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(news_router, prefix="/api/v1", tags=["news"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to SnapNews API! 🚀",
        "description": "AI-Powered News Summarizer & Reader",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

@app.get("/api/v1/info")
async def get_api_info():
    """Get API information and capabilities"""
    return {
        "name": "SnapNews API",
        "version": "1.0.0",
        "description": "AI-Powered News Summarizer & Reader API",
        "features": [
            "News search and retrieval",
            "AI-powered text summarization",
            "URL content extraction",
            "Top headlines by category",
            "Multi-language support"
        ],
        "endpoints": {
            "health": "/api/v1/health",
            "search_news": "/api/v1/news/search",
            "top_headlines": "/api/v1/news/headlines",
            "summarize_text": "/api/v1/summarize",
            "summarize_url": "/api/v1/summarize-url",
            "categories": "/api/v1/news/categories",
            "countries": "/api/v1/news/countries"
        },
        "model": {
            "name": settings.SUMMARIZER_MODEL,
            "max_input_length": settings.MAX_INPUT_LENGTH,
            "max_output_length": settings.MAX_OUTPUT_LENGTH
        }
    }

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": "The requested resource was not found",
            "available_endpoints": [
                "/",
                "/docs",
                "/api/v1/health",
                "/api/v1/news/search",
                "/api/v1/news/headlines",
                "/api/v1/summarize"
            ]
        }
    )

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later."
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )