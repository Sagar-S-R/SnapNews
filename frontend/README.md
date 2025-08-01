# SnapNews Frontend

React + Vite + Tailwind CSS frontend for SnapNews.

## Local Development

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create a `.env.local` file:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=SnapNews
VITE_APP_VERSION=1.0.0
```

## Vercel Deployment

1. Connect your GitHub repository to Vercel
2. Set the build settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add environment variables:
   - `VITE_API_BASE_URL=https://your-backend-app.onrender.com/api/v1`

## Build for Production

```bash
npm run build
npm run preview
```

## Docker Build

```bash
docker build -t snapnews-frontend .
docker run -p 80:80 snapnews-frontend
```
