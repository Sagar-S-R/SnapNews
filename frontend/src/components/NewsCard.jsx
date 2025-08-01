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
    <div className="bg-white border border-neutral-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden flex flex-col">
      {/* Image */}
      {article.url_to_image && !imageError ? (
        <div className="relative h-40 bg-neutral-100">
          {imageLoading && (
            <div className="absolute inset-0 flex items-center justify-center">
              <Loader2 className="h-7 w-7 animate-spin text-neutral-300" />
            </div>
          )}
          <img
            src={article.url_to_image}
            alt={article.title}
            onLoad={handleImageLoad}
            onError={handleImageError}
            className={`w-full h-full object-cover transition-opacity duration-300 ${imageLoading ? 'opacity-0' : 'opacity-100'}`}
          />
        </div>
      ) : (
        <div className="h-40 bg-neutral-100 flex items-center justify-center">
          <ImageIcon className="h-10 w-10 text-neutral-300" />
        </div>
      )}

      <div className="flex-1 flex flex-col p-5 gap-2">
        {/* Source and Date */}
        <div className="flex items-center justify-between text-xs text-neutral-500 mb-1">
          <span className="font-medium truncate max-w-[60%]">{article.source || 'Unknown Source'}</span>
          <span className="flex items-center gap-1">
            <Clock className="h-4 w-4" />
            {formatDate(article.published_at)}
          </span>
        </div>

        {/* Title */}
        <h3 className="text-base font-semibold text-neutral-900 mb-1 line-clamp-2 leading-tight">
          {article.title}
        </h3>

        {/* Description */}
        {article.description && (
          <p className="text-neutral-600 text-sm mb-1 line-clamp-3">
            {article.description}
          </p>
        )}

        {/* Summary */}
        {summary && (
          <div className="mb-2 p-3 bg-neutral-50 border border-blue-100 rounded text-blue-900 text-sm">
            <div className="font-medium mb-1">AI Summary:</div>
            <div>{summary.summary}</div>
            <div className="mt-1 text-xs text-blue-700 opacity-80">
              {summary.summary_length} words | Orig: {summary.original_length} | {summary.processing_time?.toFixed(2)}s
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex items-center gap-2 mt-auto">
          <button
            onClick={handleSummarize}
            disabled={loading}
            className="flex-1 px-3 py-1.5 bg-blue-600 text-white rounded border border-blue-700 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed text-xs font-medium flex items-center justify-center"
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
            className="px-3 py-1.5 border border-neutral-300 text-neutral-700 rounded hover:bg-neutral-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 text-xs font-medium flex items-center"
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
