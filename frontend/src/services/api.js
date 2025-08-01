import axios from 'axios';

// API Configuration - Update this with your Render backend URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (import.meta.env.PROD 
    ? 'https://your-backend-app.onrender.com/api/v1' 
    : 'http://localhost:8000/api/v1'
  );

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// News API functions
export const newsAPI = {
  // Search news articles
  searchNews: async (query, pageSize = 10, language = 'en') => {
    try {
      const response = await api.post('/news/search', {
        query,
        page_size: pageSize,
        language,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to search news');
    }
  },

  // Get top headlines
  getTopHeadlines: async (category = null, country = 'us', pageSize = 10) => {
    try {
      const params = new URLSearchParams();
      if (category) params.append('category', category);
      params.append('country', country);
      params.append('page_size', pageSize.toString());

      const response = await api.get(`/news/headlines?${params.toString()}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch headlines');
    }
  },

  // Get news categories
  getCategories: async () => {
    try {
      const response = await api.get('/news/categories');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch categories');
    }
  },

  // Get supported countries
  getCountries: async () => {
    try {
      const response = await api.get('/news/countries');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch countries');
    }
  },
};

// Summarization API functions
export const summarizationAPI = {
  // Summarize text
  summarizeText: async (text, maxLength = 150, minLength = 50) => {
    try {
      const response = await api.post('/summarize', {
        text,
        max_length: maxLength,
        min_length: minLength,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to summarize text');
    }
  },

  // Summarize from URL
  summarizeFromUrl: async (url, maxLength = 150, minLength = 50) => {
    try {
      const params = new URLSearchParams();
      params.append('url', url);
      params.append('max_length', maxLength.toString());
      params.append('min_length', minLength.toString());

      const response = await api.post(`/summarize-url?${params.toString()}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to summarize from URL');
    }
  },
};

// Health check API
export const healthAPI = {
  checkHealth: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Health check failed');
    }
  },
};

export default api;
