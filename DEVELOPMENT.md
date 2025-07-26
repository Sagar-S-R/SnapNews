# 🚀 SnapNews Development Guide

## 📋 Prerequisites Checklist

Before starting development, ensure you have:

- [ ] **Python 3.8+** installed and in PATH
- [ ] **Node.js 16+** installed and in PATH
- [ ] **Git** installed
- [ ] **NewsAPI Key** from https://newsapi.org/register (free)
- [ ] **2GB+ RAM** available (for AI model)
- [ ] **Stable internet connection** (for model downloads)

## 🎯 Getting Started (Step by Step)

### Step 1: Environment Setup
```bash
# 1. Open PowerShell/Command Prompt as Administrator
# 2. Navigate to your development folder
cd C:\your-projects-folder

# 3. Clone or download the project
# 4. Navigate to SnapNews folder
cd SnapNews
```

### Step 2: Quick Setup (Automated)
```bash
# Run the automated setup script
setup-dev.bat

# This will:
# ✅ Install all frontend dependencies
# ✅ Create Python virtual environment  
# ✅ Install all backend dependencies
# ✅ Show you next steps
```

### Step 3: Get NewsAPI Key
1. Visit https://newsapi.org/register
2. Sign up with your email (it's free)
3. Copy your API key
4. Open `backend\.env` file
5. Replace `your_newsapi_key_here` with your actual key:
   ```env
   NEWSAPI_KEY=abcd1234your-actual-key-here
   ```

### Step 4: Start Development Servers

#### Terminal 1 - Backend
```bash
cd backend
start.bat
```
Wait for: `✅ AI models loaded successfully!`

#### Terminal 2 - Frontend  
```bash
start-frontend.bat
```
Wait for: `Local: http://localhost:5173/`

### Step 5: Verify Everything Works
1. Open http://localhost:5173 in your browser
2. You should see SnapNews homepage
3. Try searching for "technology" 
4. Click "Summarize" on any article
5. Check if you get an AI summary

## 🛠️ Development Workflow

### Daily Development
```bash
# Start backend (Terminal 1)
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload

# Start frontend (Terminal 2)  
npm run dev
```

### Making Changes

#### Frontend Changes
- Edit files in `src/` folder
- Changes auto-reload in browser
- Check browser console for errors

#### Backend Changes  
- Edit files in `backend/app/` folder
- Server auto-reloads with `--reload` flag
- Check terminal for error messages

#### Adding New Features
1. Plan the feature
2. Create/modify backend API if needed
3. Update frontend to use new API
4. Test thoroughly
5. Commit changes

## 🔧 Common Development Tasks

### Adding New API Endpoint
1. Edit `backend/app/api/routes/news.py`
2. Add new route function
3. Update frontend `src/services/api.js`
4. Test with browser or curl

### Modifying UI Components
1. Edit files in `src/components/`
2. Use Tailwind CSS classes
3. Test responsiveness on different screen sizes

### Changing AI Model Settings
1. Edit `backend/app/config/settings.py`
2. Restart backend server
3. Test summarization functionality

## 🐛 Troubleshooting Guide

### Backend Won't Start
```bash
# Check Python version
python --version

# Reinstall dependencies
cd backend
venv\Scripts\activate
pip install -r requirements.txt --force-reinstall

# Check for port conflicts
netstat -an | findstr :8000
```

### Frontend Won't Start
```bash  
# Clear cache and reinstall
del /f /s /q node_modules
del package-lock.json
npm install

# Check Node version
node --version
```

### AI Model Issues
```bash
# Check model loading
cd backend
venv\Scripts\activate
python -c "from app.models.summarizer import get_summarizer; s = get_summarizer(); print('Model loaded:', s.is_model_loaded())"

# Clear model cache if needed
rmdir /s /q %USERPROFILE%\.cache\huggingface
```

### NewsAPI Not Working
1. Check your API key is correct
2. Verify you haven't hit rate limits (1000 requests/day)
3. Check internet connection
4. Visit https://newsapi.org/ to verify service status

## 📊 Testing Your Changes

### Manual Testing Checklist
- [ ] Homepage loads correctly
- [ ] Search functionality works
- [ ] Top headlines display properly
- [ ] Summarization works on articles
- [ ] Error messages display appropriately
- [ ] Loading states work correctly
- [ ] Responsive design works on mobile

### Backend API Testing
```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Test news search
curl -X POST http://localhost:8000/api/v1/news/search -H "Content-Type: application/json" -d "{\"query\": \"test\", \"page_size\": 5}"

# Test summarization
curl -X POST http://localhost:8000/api/v1/summarize -H "Content-Type: application/json" -d "{\"text\": \"This is a test article with enough content to be summarized properly by the AI model.\"}"
```

### Automated Tests
```bash
# Backend tests
cd backend
venv\Scripts\activate
python -m pytest tests/ -v

# Frontend tests (if added)
npm test
```

## 🔍 Debugging Tips

### Backend Debugging
- Check terminal output for errors
- Visit http://localhost:8000/docs for API documentation
- Use print statements or logging in Python code
- Check `backend/.env` file for correct configuration

### Frontend Debugging
- Open browser Developer Tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for API request failures
- Use React Developer Tools browser extension

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Kill the process or use different port |
| Model not loading | Check internet connection and disk space |
| CORS errors | Verify ALLOWED_ORIGINS in backend/.env |
| API key errors | Double-check NewsAPI key is correct |
| Build errors | Clear caches and reinstall dependencies |

## 📈 Performance Optimization

### Backend Performance
- Use caching for repeated requests
- Optimize model loading time
- Implement connection pooling
- Monitor memory usage

### Frontend Performance
- Optimize image loading
- Implement lazy loading for news cards
- Use React.memo for components
- Minimize bundle size

## 🚀 Next Steps

### Feature Ideas
- [ ] Add speech synthesis for reading summaries
- [ ] Implement user preferences storage
- [ ] Add social sharing functionality
- [ ] Create bookmark/favorites system
- [ ] Add real-time news updates
- [ ] Implement multiple summary lengths
- [ ] Add news categories filtering
- [ ] Create mobile app version

### Technical Improvements
- [ ] Add comprehensive error logging
- [ ] Implement rate limiting
- [ ] Add database for caching
- [ ] Create Docker containers
- [ ] Set up CI/CD pipeline
- [ ] Add end-to-end tests
- [ ] Implement authentication
- [ ] Add monitoring dashboard

## 💡 Tips for Success

1. **Start Small**: Make small changes and test frequently
2. **Read Errors**: Error messages usually tell you exactly what's wrong
3. **Use Documentation**: Check API docs at http://localhost:8000/docs
4. **Stay Updated**: Keep dependencies updated for security
5. **Backup Work**: Commit changes regularly to Git
6. **Ask for Help**: Use GitHub issues or community forums

## 📚 Learning Resources

- **React**: https://react.dev/learn
- **FastAPI**: https://fastapi.tiangolo.com/tutorial/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **HuggingFace**: https://huggingface.co/docs/transformers
- **NewsAPI**: https://newsapi.org/docs

---

**Happy Coding! 🎉**
