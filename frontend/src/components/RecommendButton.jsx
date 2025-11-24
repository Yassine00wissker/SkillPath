import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { recommendKeyword, recommendAI } from '../api/api';

const RecommendButton = ({ userId, mode = 'keyword', topN = 5, onResults }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleClick = async () => {
    setLoading(true);
    setError(null);

    try {
      let results;
      if (mode === 'keyword') {
        results = await recommendKeyword(userId, topN);
      } else {
        results = await recommendAI(userId, 'enhance', topN);
      }

      if (onResults) {
        onResults(results);
      }
    } catch (err) {
      setError(err.message);
      if (err.message.includes('401') || err.message.includes('Unauthorized')) {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-2">
      <button
        onClick={handleClick}
        disabled={loading}
        className={`px-6 py-2 rounded-lg font-medium transition-colors ${
          loading
            ? 'bg-gray-400 cursor-not-allowed'
            : mode === 'keyword'
            ? 'bg-blue-600 hover:bg-blue-700 text-white'
            : 'bg-purple-600 hover:bg-purple-700 text-white'
        }`}
      >
        {loading ? (
          <span className="flex items-center gap-2">
            <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Loading...
          </span>
        ) : (
          `Recommend (${mode === 'keyword' ? 'Keyword' : 'AI'})`
        )}
      </button>
      {error && (
        <p className="text-red-600 text-sm text-center max-w-xs">
          {error}
          {mode === 'ai' && (
            <button
              onClick={() => {
                setError(null);
                handleClick();
              }}
              className="ml-2 text-blue-600 underline"
            >
              Try keyword recommender
            </button>
          )}
        </p>
      )}
    </div>
  );
};

export default RecommendButton;

