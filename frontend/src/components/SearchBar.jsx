import { Search, Loader2, AlertCircle } from 'lucide-react';
import { useState } from 'react';

const SearchBar = ({ onSearch, loading, placeholder = "Search for news..." }) => {
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a search term');
      return;
    }
    
    if (query.trim().length < 2) {
      setError('Search term must be at least 2 characters long');
      return;
    }

    setError('');
    onSearch(query.trim());
  };

  const handleInputChange = (e) => {
    setQuery(e.target.value);
    if (error) setError(''); // Clear error when user starts typing
  };

  return (
    <div className="w-full max-w-xl mx-auto">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={handleInputChange}
            placeholder={placeholder}
            disabled={loading}
            className={`w-full px-4 py-2 pl-11 pr-24 text-neutral-900 bg-white border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 transition-all duration-150 text-base ${
              error 
                ? 'border-red-300 focus:ring-red-500' 
                : 'border-neutral-300 hover:border-neutral-400'
            } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
          />
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400 h-5 w-5" />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 px-5 py-1.5 bg-blue-600 text-white rounded font-medium text-sm shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              'Search'
            )}
          </button>
        </div>
        {error && (
          <div className="mt-2 flex items-center text-red-600 text-sm">
            <AlertCircle className="h-4 w-4 mr-1" />
            {error}
          </div>
        )}
      </form>
    </div>
  );
};

export default SearchBar;
