import React, { useState, useContext } from 'react';
import { useApi } from '../../hooks/useApi';
import { AuthContext } from '../../contexts/AuthContext';

const FeedbackForm = () => {
  const [feedbackText, setFeedbackText] = useState('');
  const [feedbackType, setFeedbackType] = useState('general');
  const [rating, setRating] = useState(5);
  const [submissionStatus, setSubmissionStatus] = useState('');
  const { user } = useContext(AuthContext);
  const { post, loading } = useApi();

  const feedbackTypes = [
    { value: 'general', label: 'General Feedback', icon: '💬' },
    { value: 'bug', label: 'Bug Report', icon: '🐛' },
    { value: 'feature', label: 'Feature Request', icon: '💡' },
    { value: 'ui', label: 'UI/UX Feedback', icon: '🎨' },
    { value: 'performance', label: 'Performance Issue', icon: '⚡' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!feedbackText.trim()) {
      setSubmissionStatus('error');
      return;
    }

    const feedbackData = {
      user_id: user?.id || 1, // Fallback for demo
      feedback_text: `${feedbackType.toUpperCase()}: ${feedbackText}`,
      rating: rating,
      metadata: {
        type: feedbackType,
        timestamp: new Date().toISOString()
      }
    };

    const response = await post('/feedback/', feedbackData);

    if (response) {
      setSubmissionStatus('success');
      setFeedbackText('');
      setRating(5);
      setFeedbackType('general');
    } else {
      setSubmissionStatus('error');
    }
  };

  const getEmojiForRating = (score) => {
    const emojis = ['😞', '😐', '😊', '😄', '🤩'];
    return emojis[score - 1] || '😊';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-2">Share Your Feedback</h2>
      <p className="text-gray-600 mb-6">Help us improve the RailSpark system</p>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Feedback Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            What type of feedback are you sharing?
          </label>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {feedbackTypes.map((type) => (
              <button
                key={type.value}
                type="button"
                onClick={() => setFeedbackType(type.value)}
                className={`p-3 border-2 rounded-lg text-center transition-all ${
                  feedbackType === type.value
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="text-2xl mb-1">{type.icon}</div>
                <div className="text-xs font-medium text-gray-700">{type.label}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Rating */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            How would you rate your experience?
            <span className="ml-2 text-2xl">{getEmojiForRating(rating)}</span>
          </label>
          <div className="flex items-center space-x-2">
            {[1, 2, 3, 4, 5].map((score) => (
              <button
                key={score}
                type="button"
                onClick={() => setRating(score)}
                className={`w-10 h-10 rounded-full border-2 flex items-center justify-center transition-all ${
                  rating >= score
                    ? 'bg-yellow-100 border-yellow-400'
                    : 'bg-gray-100 border-gray-300'
                }`}
              >
                <span className="text-lg">{score}</span>
              </button>
            ))}
            <span className="ml-3 text-sm text-gray-600">
              {rating === 1 && 'Very Poor'}
              {rating === 2 && 'Poor'}
              {rating === 3 && 'Average'}
              {rating === 4 && 'Good'}
              {rating === 5 && 'Excellent'}
            </span>
          </div>
        </div>

        {/* Feedback Text */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Your Feedback {feedbackType !== 'general' && `(${feedbackTypes.find(t => t.value === feedbackType)?.label})`}
          </label>
          <textarea
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
            placeholder={
              feedbackType === 'bug' ? 'Describe the issue you encountered...' :
              feedbackType === 'feature' ? 'What feature would you like to see?...' :
              feedbackType === 'ui' ? 'Share your thoughts on the interface...' :
              feedbackType === 'performance' ? 'Describe any performance issues...' :
              'Share your thoughts, suggestions, or concerns...'
            }
            rows={6}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            required
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Be specific and detailed for better understanding</span>
            <span>{feedbackText.length}/1000 characters</span>
          </div>
        </div>

        {/* Submission Status */}
        {submissionStatus === 'success' && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center">
              <div className="text-green-600 text-lg mr-2">✅</div>
              <div>
                <strong className="text-green-800">Thank you!</strong>
                <p className="text-green-700 text-sm">Your feedback has been submitted successfully.</p>
              </div>
            </div>
          </div>
        )}

        {submissionStatus === 'error' && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <div className="text-red-600 text-lg mr-2">❌</div>
              <div>
                <strong className="text-red-800">Error!</strong>
                <p className="text-red-700 text-sm">Failed to submit feedback. Please try again.</p>
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-between items-center">
          <div className="text-sm text-gray-600">
            {user ? `Submitting as: ${user.username}` : 'Submitting anonymously'}
          </div>
          <button
            type="submit"
            disabled={loading || !feedbackText.trim()}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Submitting...' : 'Submit Feedback'}
          </button>
        </div>
      </form>

      {/* Feedback Guidelines */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-medium text-blue-900 mb-2">Feedback Guidelines</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Be specific and provide examples when possible</li>
          <li>• For bug reports, include steps to reproduce the issue</li>
          <li>• Feature requests should explain the problem you're trying to solve</li>
          <li>• Constructive criticism helps us improve the system</li>
        </ul>
      </div>

      {/* Recent Feedback Preview */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-medium text-gray-900 mb-2">Why Your Feedback Matters</h3>
        <p className="text-sm text-gray-600">
          Your feedback helps us prioritize improvements, fix issues, and make RailSpark better 
          for all KMRL operators. We review every submission and use it to guide our development.
        </p>
      </div>
    </div>
  );
};

export default FeedbackForm;