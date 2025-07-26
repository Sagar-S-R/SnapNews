# 🚀 SnapNews - AI-Powered News Summarizer & Reader

An intelligent news application that fetches the latest headlines and provides AI-powered summaries using HuggingFace BART model. Built with React + FastAPI for a modern, responsive experience.

![SnapNews Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![React](https://img.shields.io/badge/React-19.0.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

## 🌟 Features

### 🧠 AI-Powered Summarization
- **Advanced BART Model**: Uses Facebook's `bart-large-cnn` for high-quality summaries
- **Intelligent Text Processing**: Automatic text cleaning and preprocessing
- **URL Content Extraction**: Extract and summarize content directly from news URLs
- **Customizable Summary Length**: Adjustable min/max summary lengths

### 📰 News Integration
- **Live News Search**: Search across thousands of global news sources
- **Top Headlines**: Browse latest headlines by category and country
- **Multiple Sources**: Powered by NewsAPI with 70,000+ sources
- **Real-time Updates**: Fresh content updated continuously

### 🎨 Modern UI/UX
- **Responsive Design**: Built with Tailwind CSS for all devices
- **Dark/Light Mode**: Automatic theme adaptation
- **Loading States**: Smooth loading animations and feedback
- **Error Handling**: Graceful error messages and retry mechanisms

### ⚡ Performance & Reliability
- **Fast API Backend**: High-performance FastAPI with async support
- **Caching**: Intelligent caching for better performance
- **Error Recovery**: Robust error handling and fallback mechanisms
- **Health Monitoring**: Built-in health checks and monitoring

## 🏗️ Tech Stack

### Frontend
- **React 19** - Modern React with hooks
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests
- **Lucide React** - Beautiful icons

### Backend
- **FastAPI** - Modern Python web framework
- **HuggingFace Transformers** - BART model for summarization
- **PyTorch** - Deep learning framework
- **Pydantic** - Data validation and settings
- **Uvicorn** - ASGI server

### AI/ML
- **facebook/bart-large-cnn** - Pre-trained summarization model
- **newspaper3k** - Article content extraction
- **Beautiful Soup** - HTML parsing and cleaning

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** - [Download here](https://python.org)
- **Node.js 16+** - [Download here](https://nodejs.org)
- **NewsAPI Key** - [Get free key](https://newsapi.org/register)

### 🔧 Automated Setup (Windows)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd SnapNews
   ```

2. **Run the setup script**
   ```bash
   setup-dev.bat
   ```

3. **Configure API key**
   - Open `backend\.env`
   - Replace `your_newsapi_key_here` with your actual NewsAPI key

4. **Start the application**
   ```bash
   # Terminal 1 - Backend
   cd backend
   start.bat
   
   # Terminal 2 - Frontend
   start-frontend.bat
   ```

### 🔧 Manual Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate
# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit backend/.env and add your NewsAPI key

# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## 📚 API Documentation

### Core Endpoints

#### 🔍 News Search
```http
POST /api/v1/news/search
Content-Type: application/json

{
  "query": "artificial intelligence",
  "page_size": 10,
  "language": "en"
}
```

#### 📰 Top Headlines
```http
GET /api/v1/news/headlines?category=technology&country=us&page_size=10
```

#### 🤖 Text Summarization
```http
POST /api/v1/summarize
Content-Type: application/json

{
  "text": "Long article text here...",
  "max_length": 150,
  "min_length": 50
}
```

#### 🔗 URL Summarization
```http
POST /api/v1/summarize-url?url=https://example.com/article&max_length=150
```

#### ❤️ Health Check
```http
GET /api/v1/health
```

### Response Format

#### News Articles
```json
{
  "articles": [
    {
      "title": "Article Title",
      "description": "Article description",
      "content": "Article content...",
      "url": "https://example.com/article",
      "url_to_image": "https://example.com/image.jpg",
      "published_at": "2025-01-26T10:30:00Z",
      "source": "News Source"
    }
  ],
  "total_results": 100,
  "status": "ok"
}
```

#### Summarization
```json
{
  "summary": "AI-generated summary text...",
  "original_length": 500,
  "summary_length": 75,
  "processing_time": 2.34
}
```

## 🏛️ Project Structure

```
SnapNews/
├── frontend/                    # React application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── SearchBar.jsx   # Search functionality
│   │   │   ├── NewsCard.jsx    # News article display
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── ErrorMessage.jsx
│   │   ├── services/           # API services
│   │   │   └── api.js          # HTTP client setup
│   │   ├── App.jsx             # Main application
│   │   └── main.jsx            # Entry point
│   ├── package.json
│   └── vite.config.js
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── main.py             # FastAPI app setup
│   │   ├── api/routes/         # API endpoints
│   │   │   └── news.py         # News and summarization routes
│   │   ├── models/             # Data models
│   │   │   ├── schemas.py      # Pydantic models
│   │   │   └── summarizer.py   # BART model wrapper
│   │   ├── services/           # Business logic
│   │   │   └── news_service.py # News API integration
│   │   ├── config/             # Configuration
│   │   │   └── settings.py     # App settings
│   │   └── utils/              # Utilities
│   │       └── helpers.py      # Text processing helpers
│   ├── requirements.txt
│   └── .env                    # Environment variables
├── start-frontend.bat          # Frontend startup script
├── setup-dev.bat              # Complete setup script
└── README.md
```

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)
```env
# News API Configuration
NEWSAPI_KEY=your_newsapi_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Model Configuration
SUMMARIZER_MODEL=facebook/bart-large-cnn
MAX_INPUT_LENGTH=1024
MAX_OUTPUT_LENGTH=150
MIN_OUTPUT_LENGTH=50

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

#### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_NEWSAPI_KEY=your_newsapi_key_here
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### API Testing
```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Test summarization
curl -X POST http://localhost:8000/api/v1/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here..."}'
```

## 🚀 Deployment

### Local Production Build

#### Frontend
```bash
npm run build
npm run preview
```

#### Backend
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 5173
CMD ["npm", "run", "preview"]
```

### Cloud Deployment Options

- **Frontend**: Vercel, Netlify, GitHub Pages
- **Backend**: Render, Railway, Google Cloud Run, AWS Lambda
- **Full Stack**: Heroku, DigitalOcean App Platform

## 🔧 Troubleshooting

### Common Issues

#### Backend not starting
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check if port 8000 is available
netstat -an | find "8000"
```

#### Frontend build issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version
```

#### Model loading issues
- Ensure stable internet connection for model download
- Check available disk space (models are ~1.6GB)
- Verify PyTorch installation: `python -c "import torch; print(torch.__version__)"`

#### NewsAPI issues
- Verify API key is correct
- Check API usage limits (1000 requests/day for free tier)
- Ensure proper internet connectivity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **HuggingFace** for the BART model and transformers library
- **NewsAPI** for providing news data
- **Facebook AI** for the BART-large-CNN model
- **FastAPI** team for the excellent framework
- **React** and **Vite** teams for the frontend tools

## 📞 Support

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/snapnews/issues)
- 📖 Documentation: [Wiki](https://github.com/your-username/snapnews/wiki)

---

**Built with ❤️ using React, FastAPI, and HuggingFace Transformers**
