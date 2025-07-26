import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

const ErrorMessage = ({ 
  error, 
  onRetry, 
  onHome,
  title = 'Something went wrong',
  showHomeButton = false 
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <div className="bg-red-50 border border-red-200 rounded-lg p-8 max-w-md w-full text-center">
        <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
        
        <h3 className="text-lg font-semibold text-red-900 mb-2">
          {title}
        </h3>
        
        <p className="text-red-700 text-sm mb-6 leading-relaxed">
          {error || 'An unexpected error occurred. Please try again.'}
        </p>
        
        <div className="flex flex-col gap-3">
          {onRetry && (
            <button
              onClick={onRetry}
              className="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors duration-200 font-medium flex items-center justify-center"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Try Again
            </button>
          )}
          
          {showHomeButton && onHome && (
            <button
              onClick={onHome}
              className="w-full px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200 font-medium flex items-center justify-center"
            >
              <Home className="h-4 w-4 mr-2" />
              Go Home
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
