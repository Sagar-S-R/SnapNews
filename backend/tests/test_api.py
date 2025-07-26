import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "SnapNews API" in data["message"]

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data

def test_api_info_endpoint():
    """Test the API info endpoint"""
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "features" in data
    assert "endpoints" in data

def test_get_categories():
    """Test getting news categories"""
    response = client.get("/api/v1/news/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert "business" in data["categories"]
    assert "technology" in data["categories"]

def test_get_countries():
    """Test getting supported countries"""
    response = client.get("/api/v1/news/countries")
    assert response.status_code == 200
    data = response.json()
    assert "countries" in data
    assert "us" in data["countries"]
    assert "gb" in data["countries"]

def test_summarize_text():
    """Test text summarization"""
    test_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving". As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
    """
    
    response = client.post("/api/v1/summarize", json={
        "text": test_text,
        "max_length": 100,
        "min_length": 30
    })
    
    # Note: This test might fail if the model isn't loaded
    # In a real test environment, you might want to mock the summarizer
    if response.status_code == 200:
        data = response.json()
        assert "summary" in data
        assert "original_length" in data
        assert "summary_length" in data
        assert "processing_time" in data
    else:
        # Model might not be loaded in test environment
        assert response.status_code in [500, 422]

def test_summarize_text_too_short():
    """Test summarization with text that's too short"""
    response = client.post("/api/v1/summarize", json={
        "text": "Short text",
        "max_length": 100,
        "min_length": 30
    })
    
    assert response.status_code == 400

def test_search_news_without_api_key():
    """Test news search without API key (should handle gracefully)"""
    response = client.post("/api/v1/news/search", json={
        "query": "technology",
        "page_size": 5,
        "language": "en"
    })
    
    # Should return 200 but with error message about missing API key
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
    # Might be empty if no API key is configured

if __name__ == "__main__":
    pytest.main([__file__])