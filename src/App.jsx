import { useState, useEffect } from 'react';
import { Newspaper, Zap, Globe, TrendingUp, AlertCircle } from 'lucide-react';

// Components
import SearchBar from './components/SearchBar';
import NewsCard from './components/NewsCard';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import NewsFilters from './components/NewsFilters';

// Services
import { newsAPI, summarizationAPI, healthAPI } from './services/api';

function App() {
  // State management
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [summaries, setSummaries] = useState({});
  const [summarizingIds, setSummarizingIds] = useState(new Set());
  const [apiHealth, setApiHealth] = useState('unknown');
  
  // Filter states
  const [category, setCategory] = useState('');
  const [country, setCountry] = useState('us');
  const [pageSize, setPageSize] = useState(10);
  const [viewMode, setViewMode] = useState('search'); // 'search' or 'headlines'

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
    // Load top headlines by default
    loadTopHeadlines();
  }, []);

  const checkApiHealth = async () => {
    try {
      await healthAPI.checkHealth();
      setApiHealth('healthy');
    } catch (error) {
      console.error('API health check failed:', error);
      setApiHealth('unhealthy');
    }
  };

  const loadTopHeadlines = async () => {
    setLoading(true);
    setError('');
    setViewMode('headlines');
    
    try {
      const response = await newsAPI.getTopHeadlines(
        category || null, 
        country, 
        pageSize
      );
      
      if (response.status === 'ok') {
        setArticles(response.articles);
        setSearchQuery('');
      } else {
        setError(response.message || 'Failed to load headlines');
      }
    } catch (error) {
      console.error('Error loading headlines:', error);
      setError(error.message || 'Failed to load headlines');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query) => {
    setLoading(true);
    setError('');
    setSearchQuery(query);
    setViewMode('search');
    
    try {
      const response = await newsAPI.searchNews(query, pageSize, 'en');
      
      if (response.status === 'ok') {
        setArticles(response.articles);
        if (response.articles.length === 0) {
          setError('No articles found for your search. Try different keywords.');
        }
      } else {
        setError(response.message || 'Search failed');
      }
    } catch (error) {
      console.error('Search error:', error);
      setError(error.message || 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSummarize = async (textOrUrl, article, isUrl = false) => {
    const articleId = article.url; // Use URL as unique identifier
    
    // Add to summarizing set
    setSummarizingIds(prev => new Set(prev).add(articleId));
    
    try {
      let result;
      
      if (isUrl) {
        result = await summarizationAPI.summarizeFromUrl(textOrUrl);
      } else {
        result = await summarizationAPI.summarizeText(textOrUrl);
      }
      
      // Store summary
      setSummaries(prev => ({
        ...prev,
        [articleId]: result
      }));
      
    } catch (error) {
      console.error('Summarization error:', error);
      // Show error in summary area
      setSummaries(prev => ({
        ...prev,
        [articleId]: {
          summary: `Failed to generate summary: ${error.message}`,
          error: true
        }
      }));
    } finally {
      // Remove from summarizing set
      setSummarizingIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(articleId);
        return newSet;
      });
    }
  };

  // Handle filter changes for headlines
  useEffect(() => {
    if (viewMode === 'headlines') {
      loadTopHeadlines();
    }
  }, [category, country, pageSize]);

  const handleRetry = () => {
    if (viewMode === 'search' && searchQuery) {
      handleSearch(searchQuery);
    } else {
      loadTopHeadlines();
    }
  };

  const clearSearch = () => {
    setSearchQuery('');
    setError('');
    loadTopHeadlines();
  };

  return (
    <div className="min-h-screen w-full bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <div className="flex items-center space-x-3">
                <div className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-lg">
                  <Newspaper className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">SnapNews</h1>
                  <p className="text-xs text-gray-500">AI-Powered News Summarizer</p>
                </div>
              </div>
            </div>
            
            {/* API Health Indicator */}
            <div className="flex items-center space-x-2">
              <div className={`flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                apiHealth === 'healthy' 
                  ? 'bg-green-100 text-green-800' 
                  : apiHealth === 'unhealthy'
                  ? 'bg-red-100 text-red-800'
                  : 'bg-gray-100 text-gray-800'
              }`}>
                <div className={`w-2 h-2 rounded-full mr-2 ${
                  apiHealth === 'healthy' ? 'bg-green-400' : 
                  apiHealth === 'unhealthy' ? 'bg-red-400' : 'bg-gray-400'
                }`} />
                API {apiHealth === 'healthy' ? 'Online' : apiHealth === 'unhealthy' ? 'Offline' : 'Unknown'}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Hero Section */}
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Stay Informed with AI-Powered Summaries
          </h2>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Search for the latest news or browse top headlines, then get instant AI summaries 
            to understand the key points quickly.
          </p>
          
          {/* Search Bar */}
          <SearchBar 
            onSearch={handleSearch}
            loading={loading}
            placeholder="Search for news topics (e.g., technology, politics, sports)..."
          />
        </div>

        {/* Mode Toggle */}
        <div className="flex justify-center mb-6">
          <div className="bg-white rounded-lg p-1 shadow-sm border border-gray-200">
            <div className="flex">
              <button
                onClick={() => handleSearch(searchQuery || 'latest')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  viewMode === 'search'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Globe className="h-4 w-4 inline mr-2" />
                Search News
              </button>
              <button
                onClick={loadTopHeadlines}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  viewMode === 'headlines'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <TrendingUp className="h-4 w-4 inline mr-2" />
                Top Headlines
              </button>
            </div>
          </div>
        </div>

        {/* Filters (only show for headlines) */}
        {viewMode === 'headlines' && (
          <NewsFilters
            category={category}
            country={country}
            pageSize={pageSize}
            onCategoryChange={setCategory}
            onCountryChange={setCountry}
            onPageSizeChange={setPageSize}
            disabled={loading}
          />
        )}

        {/* Results Header */}
        {(articles.length > 0 || loading || error) && (
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {viewMode === 'search' 
                    ? `Search Results${searchQuery ? ` for "${searchQuery}"` : ''}` 
                    : 'Top Headlines'
                  }
                </h3>
                {articles.length > 0 && (
                  <p className="text-sm text-gray-600">
                    {articles.length} article{articles.length !== 1 ? 's' : ''} found
                  </p>
                )}
              </div>
              
              {searchQuery && (
                <button
                  onClick={clearSearch}
                  className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                >
                  Clear Search
                </button>
              )}
            </div>
          </div>
        )}

        {/* Content Area */}
        {loading && <LoadingSpinner size="lg" text="Loading news articles..." />}
        
        {error && (
          <ErrorMessage 
            error={error}
            onRetry={handleRetry}
            title="Failed to load news"
          />
        )}

        {!loading && !error && articles.length === 0 && (
          <div className="text-center py-12">
            <Newspaper className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No articles to display
            </h3>
            <p className="text-gray-600 mb-4">
              Search for news topics or browse top headlines to get started.
            </p>
          </div>
        )}

        {/* News Grid */}
        {!loading && !error && articles.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {articles.map((article, index) => (
              <NewsCard
                key={article.url + index}
                article={article}
                onSummarize={handleSummarize}
                loading={summarizingIds.has(article.url)}
                summary={summaries[article.url]}
              />
            ))}
          </div>
        )}

        {/* Features Section (shown when no content) */}
        {!loading && !error && articles.length === 0 && !searchQuery && (
          <div className="mt-16">
            <div className="text-center mb-12">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Powerful Features for Modern News Consumption
              </h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center p-6">
                <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mx-auto mb-4">
                  <Zap className="h-6 w-6 text-blue-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">
                  AI-Powered Summaries
                </h4>
                <p className="text-gray-600">
                  Get instant, accurate summaries of any news article using advanced AI technology.
                </p>
              </div>
              
              <div className="text-center p-6">
                <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg mx-auto mb-4">
                  <Globe className="h-6 w-6 text-green-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">
                  Global News Search
                </h4>
                <p className="text-gray-600">
                  Search news from thousands of sources worldwide on any topic that interests you.
                </p>
              </div>
              
              <div className="text-center p-6">
                <div className="flex items-center justify-center w-12 h-12 bg-purple-100 rounded-lg mx-auto mb-4">
                  <TrendingUp className="h-6 w-6 text-purple-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">
                  Top Headlines
                </h4>
                <p className="text-gray-600">
                  Browse the latest top headlines by category and country to stay updated.
                </p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-gray-600 text-sm">
              © 2025 SnapNews. Built with React, FastAPI, and HuggingFace BART.
            </p>
            <p className="text-gray-500 text-xs mt-2">
              News powered by NewsAPI.org • AI summaries by Facebook BART
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
