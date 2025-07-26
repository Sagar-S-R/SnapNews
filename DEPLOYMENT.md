# 🚀 SnapNews Deployment Guide

## 📋 Deployment Options

### 1. Local Development
- **Frontend**: Vite dev server (port 5173)
- **Backend**: Uvicorn dev server (port 8000)
- **Purpose**: Development and testing

### 2. Local Production
- **Frontend**: Static build served by Vite preview
- **Backend**: Gunicorn with Uvicorn workers
- **Purpose**: Production testing locally

### 3. Cloud Deployment
- **Frontend**: Vercel, Netlify, or GitHub Pages
- **Backend**: Render, Railway, Google Cloud Run
- **Purpose**: Live production deployment

## 🛠️ Local Production Setup

### Backend Production
```bash
cd backend

# Activate virtual environment
venv\Scripts\activate

# Install production server
pip install gunicorn

# Create production environment file
copy .env .env.production
# Edit .env.production:
# DEBUG=False
# ALLOWED_ORIGINS=["https://your-frontend-domain.com"]

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Production
```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Or serve with any static server
npx serve dist
```

## ☁️ Cloud Deployment

### Backend on Render

1. **Create Render Account**
   - Visit https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   ```
   Name: snapnews-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

4. **Environment Variables**
   ```
   NEWSAPI_KEY=your_actual_key_here
   DEBUG=False
   ALLOWED_ORIGINS=["https://your-frontend-url.vercel.app"]
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment

### Frontend on Vercel

1. **Create Vercel Account**
   - Visit https://vercel.com
   - Sign up with GitHub

2. **Import Project**
   - Click "New Project"
   - Select your repository
   - Framework: Vite
   - Root Directory: ./

3. **Environment Variables**
   ```
   VITE_API_BASE_URL=https://your-backend-url.onrender.com/api/v1
   ```

4. **Deploy**
   - Click "Deploy"
   - Get your deployment URL

### Alternative: Railway Deployment

#### Backend on Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add environment variables
railway variables set NEWSAPI_KEY=your_key_here
railway variables set DEBUG=False

# Deploy
railway up
```

#### Frontend on Netlify
1. Build your project: `npm run build`
2. Drag `dist` folder to Netlify
3. Configure environment variables in Netlify dashboard

## 🐳 Docker Deployment

### Backend Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - NEWSAPI_KEY=${NEWSAPI_KEY}
      - DEBUG=False
      - ALLOWED_ORIGINS=["http://localhost:3000"]
    volumes:
      - ./backend:/app
    restart: unless-stopped

  frontend:
    build: .
    ports:
      - "3000:80"
    environment:
      - VITE_API_BASE_URL=http://localhost:8000/api/v1
    depends_on:
      - backend
    restart: unless-stopped
```

## 🔧 Production Configuration

### Backend Production Settings
```python
# backend/app/config/settings.py
class Settings(BaseSettings):
    # Production settings
    DEBUG: bool = False
    API_HOST: str = "0.0.0.0"
    API_PORT: int = int(os.getenv("PORT", 8000))
    
    # Security
    ALLOWED_ORIGINS: List[str] = [
        "https://your-frontend-domain.com",
        "https://your-custom-domain.com"
    ]
    
    # Performance
    MAX_INPUT_LENGTH: int = 1024
    MAX_OUTPUT_LENGTH: int = 150
```

### Frontend Production Build
```javascript
// vite.config.js
export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['lucide-react'],
        }
      }
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

## 🔒 Security Considerations

### Environment Variables
```bash
# Never commit these to version control
NEWSAPI_KEY=your_secret_key
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

### CORS Configuration
```python
# Only allow your frontend domains
ALLOWED_ORIGINS = [
    "https://yourapp.vercel.app",
    "https://your-custom-domain.com"
]
```

### HTTPS Setup
- Use HTTPS for all production deployments
- Most cloud providers (Render, Vercel) provide HTTPS automatically
- For custom domains, use Let's Encrypt certificates

## 📊 Monitoring & Logging

### Backend Monitoring
```python
# Add to main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
```

### Performance Monitoring
- Use cloud provider monitoring (Render metrics, Vercel analytics)
- Add custom health check endpoints
- Monitor API response times
- Track error rates

## 🚀 CI/CD Pipeline

### GitHub Actions Example
```yaml
# .github/workflows/deploy.yml
name: Deploy SnapNews

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          
      - name: Run tests
        run: |
          cd backend
          python -m pytest tests/
          
      - name: Deploy to Render
        # Add your deployment steps here

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
          
      - name: Install and build
        run: |
          npm install
          npm run build
          
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 🔧 Troubleshooting Deployment

### Common Issues

#### Backend Deployment Issues
```bash
# Check logs
railway logs
# or
render logs

# Common fixes:
# 1. Wrong Python version
# 2. Missing environment variables
# 3. Port binding issues
# 4. Model download failures
```

#### Frontend Deployment Issues
```bash
# Build issues
npm run build

# Environment variable issues
# Make sure VITE_ prefix is used
VITE_API_BASE_URL=https://your-backend.com

# CORS issues
# Update backend ALLOWED_ORIGINS
```

### Performance Optimization

#### Backend Optimization
- Use Gunicorn with multiple workers
- Enable gzip compression
- Implement caching for repeated requests
- Optimize model loading

#### Frontend Optimization
- Enable code splitting
- Optimize images
- Use lazy loading
- Enable service worker for caching

## 📈 Scaling Considerations

### Backend Scaling
- Use multiple Gunicorn workers
- Implement Redis for caching
- Use database for persistent storage
- Consider using a CDN

### Frontend Scaling
- Use CDN for static assets
- Enable browser caching
- Optimize bundle size
- Implement code splitting

## 💡 Best Practices

1. **Environment Separation**: Use different environments for dev/staging/prod
2. **Secret Management**: Never commit API keys or secrets
3. **Error Handling**: Implement comprehensive error handling
4. **Monitoring**: Set up alerts for failures
5. **Backups**: Regular backups of important data
6. **Testing**: Automated testing before deployment
7. **Documentation**: Keep deployment docs updated

---

**Happy Deploying! 🚀**
