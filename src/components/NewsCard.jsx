import { Clock, ExternalLink, Image as ImageIcon, Loader2 } from 'lucide-react';
import { useState } from 'react';

const NewsCard = ({ article, onSummarize, loading, summary }) => {
  const [imageError, setImageError] = useState(false);
  const [imageLoading, setImageLoading] = useState(true);

  const formatDate = (dateString) => {
    if (!dateString) return 'Date unknown';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return 'Date unknown';
    }
  };

  const handleImageLoad = () => {
    setImageLoading(false);
  };

  const handleImageError = () => {
    setImageError(true);
    setImageLoading(false);
  };

  const handleSummarize = () => {
    if (article.content && article.content.length > 50) {
      onSummarize(article.content, article);
    } else {
      // If no content, try to summarize from URL
      onSummarize(article.url, article, true);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden">
      {/* Image */}
      {article.url_to_image && !imageError && (
        <div className="relative h-48 bg-gray-200">
          {imageLoading && (
            <div className="absolute inset-0 flex items-center justify-center">
              <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
            </div>
          )}
          <img
            src={article.url_to_image}
            alt={article.title}
            onLoad={handleImageLoad}
            onError={handleImageError}
            className={`w-full h-full object-cover transition-opacity duration-300 ${
              imageLoading ? 'opacity-0' : 'opacity-100'
            }`}
          />
        </div>
      )}

      {/* No image placeholder */}
      {(!article.url_to_image || imageError) && (
        <div className="h-48 bg-gray-100 flex items-center justify-center">
          <ImageIcon className="h-12 w-12 text-gray-400" />
        </div>
      )}

      <div className="p-6">
        {/* Source and Date */}
        <div className="flex items-center justify-between text-sm text-gray-500 mb-2">
          <span className="font-medium">{article.source || 'Unknown Source'}</span>
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-1" />
            {formatDate(article.published_at)}
          </div>
        </div>

        {/* Title */}
        <h3 className="text-lg font-bold text-gray-900 mb-3 line-clamp-2 leading-tight">
          {article.title}
        </h3>

        {/* Description */}
        {article.description && (
          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
            {article.description}
          </p>
        )}

        {/* Summary */}
        {summary && (
          <div className="mb-4 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400">
            <h4 className="font-semibold text-blue-900 mb-2 text-sm">AI Summary:</h4>
            <p className="text-blue-800 text-sm leading-relaxed">{summary.summary}</p>
            <div className="mt-2 text-xs text-blue-600">
              Summary: {summary.summary_length} words | Original: {summary.original_length} words | 
              Time: {summary.processing_time?.toFixed(2)}s
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex items-center justify-between gap-3">
          <button
            onClick={handleSummarize}
            disabled={loading}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 text-sm font-medium flex items-center justify-center"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Summarizing...
              </>
            ) : (
              'Summarize'
            )}
          </button>

          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200 text-sm font-medium flex items-center"
          >
            <ExternalLink className="h-4 w-4 mr-1" />
            Read Full
          </a>
        </div>
      </div>
    </div>
  );
};

export default NewsCard;
