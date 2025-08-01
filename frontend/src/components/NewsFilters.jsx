import { useState } from 'react';
import { Filter, ChevronDown } from 'lucide-react';

const categories = {
  '': 'All Categories',
  'business': 'Business',
  'entertainment': 'Entertainment',
  'general': 'General',
  'health': 'Health',
  'science': 'Science',
  'sports': 'Sports',
  'technology': 'Technology'
};

const countries = {
  'us': 'United States',
  'gb': 'United Kingdom',
  'ca': 'Canada',
  'au': 'Australia',
  'in': 'India',
  'de': 'Germany',
  'fr': 'France',
  'jp': 'Japan'
};

const NewsFilters = ({ 
  category, 
  country, 
  pageSize, 
  onCategoryChange, 
  onCountryChange, 
  onPageSizeChange,
  disabled = false 
}) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="bg-white border border-neutral-200 rounded-md p-3 mb-6">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between w-full text-left focus:outline-none px-1 py-1"
        disabled={disabled}
      >
        <span className="flex items-center gap-2 text-sm font-medium text-neutral-800">
          <Filter className="h-5 w-5 text-blue-500" />
          Filters
        </span>
        <ChevronDown 
          className={`h-5 w-5 text-neutral-400 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} 
        />
      </button>
      {isOpen && (
        <div className="mt-3 pt-3 border-t border-neutral-100">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {/* Category Filter */}
            <div>
              <label className="block text-xs font-medium text-neutral-600 mb-1">
                Category
              </label>
              <select
                value={category}
                onChange={(e) => onCategoryChange(e.target.value)}
                disabled={disabled}
                className="w-full px-2 py-1.5 border border-neutral-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {Object.entries(categories).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </div>
            {/* Country Filter */}
            <div>
              <label className="block text-xs font-medium text-neutral-600 mb-1">
                Country
              </label>
              <select
                value={country}
                onChange={(e) => onCountryChange(e.target.value)}
                disabled={disabled}
                className="w-full px-2 py-1.5 border border-neutral-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {Object.entries(countries).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </div>
            {/* Page Size Filter */}
            <div>
              <label className="block text-xs font-medium text-neutral-600 mb-1">
                Articles per page
              </label>
              <select
                value={pageSize}
                onChange={(e) => onPageSizeChange(parseInt(e.target.value))}
                disabled={disabled}
                className="w-full px-2 py-1.5 border border-neutral-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-400 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <option value={5}>5 articles</option>
                <option value={10}>10 articles</option>
                <option value={15}>15 articles</option>
                <option value={20}>20 articles</option>
              </select>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NewsFilters;
