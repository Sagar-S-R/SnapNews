# SnapNews Backend

FastAPI backend for SnapNews with AI-powered news summarization.

## Local Development

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

Create a `.env` file:

```env
NEWSAPI_KEY=your_newsapi_key_here
API_HOST=0.0.0.0
PORT=8000
DEBUG=true
ENVIRONMENT=development
SUMMARIZER_MODEL=facebook/bart-large-cnn
MAX_INPUT_LENGTH=1024
MAX_OUTPUT_LENGTH=150
MIN_OUTPUT_LENGTH=50
```

## Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the build settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker app.main:app`
4. Add environment variables in Render dashboard:
   - `NEWSAPI_KEY`: Your NewsAPI key
   - `ENVIRONMENT`: `production`
   - `DEBUG`: `false`
   - Add your Vercel frontend URL to CORS origins in settings.py

## API Endpoints

- **Health Check**: `GET /api/v1/health`
- **Search News**: `POST /api/v1/news/search`
- **Top Headlines**: `GET /api/v1/news/headlines`
- **Summarize Text**: `POST /api/v1/summarize`
- **Summarize URL**: `POST /api/v1/summarize-url`

## Docker Build

```bash
docker build -t snapnews-backend .
docker run -p 8000:8000 snapnews-backend
```
pip install -r requirements.txt
```

### 2. Configuration
Create/edit `.env` file:
```env
NEWSAPI_KEY=your_newsapi_key_here
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
SUMMARIZER_MODEL=facebook/bart-large-cnn
```

### 3. Run Server
```bash
# Development server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or use the startup script
start.bat  # Windows
./start.sh # Linux/Mac
```

## 📚 API Endpoints

### Health & Info
- `GET /` - API welcome message
- `GET /api/v1/health` - Health check
- `GET /api/v1/info` - API information and capabilities

### News Endpoints
- `POST /api/v1/news/search` - Search news articles
- `GET /api/v1/news/headlines` - Get top headlines
- `GET /api/v1/news/categories` - Available news categories
- `GET /api/v1/news/countries` - Supported countries

### Summarization Endpoints
- `POST /api/v1/summarize` - Summarize text content
- `POST /api/v1/summarize-url` - Summarize content from URL

## 🧠 AI Model Details

### BART Model Configuration
- **Model**: `facebook/bart-large-cnn`
- **Purpose**: Abstractive text summarization
- **Input Length**: Up to 1024 tokens
- **Output Length**: 50-150 tokens (configurable)
- **Device**: Auto-detects CUDA/CPU

### Model Features
- **High Quality**: State-of-the-art summarization performance
- **Fast Inference**: Optimized for real-time usage
- **Flexible Length**: Configurable summary lengths
- **Robust**: Handles various text types and lengths

## 🏗️ Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI application setup
│   ├── api/routes/
│   │   └── news.py          # API endpoints
│   ├── models/
│   │   ├── schemas.py       # Pydantic data models
│   │   ├── summarizer.py    # BART model wrapper
│   │   └── rag_model.py     # Advanced RAG implementation
│   ├── services/
│   │   └── news_service.py  # News API business logic
│   ├── config/
│   │   └── settings.py      # Configuration management
│   └── utils/
│       └── helpers.py       # Text processing utilities
├── tests/
│   └── test_api.py          # API tests
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_api.py::test_summarize_text -v
```

### Manual API Testing
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Search news  
curl -X POST http://localhost:8000/api/v1/news/search \
  -H "Content-Type: application/json" \
  -d '{"query": "technology", "page_size": 5}'

# Summarize text
curl -X POST http://localhost:8000/api/v1/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your long article text here..."}'
```

## 🚀 Deployment

### Production Setup
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

**Built with FastAPI, HuggingFace Transformers, and ❤️**