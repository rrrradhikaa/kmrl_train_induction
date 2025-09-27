import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import FeedbackForm from '../components/Feedback/FeedbackForm';

const Feedback = () => {
  const [recentFeedback, setRecentFeedback] = useState([]);
  const [showForm, setShowForm] = useState(true);
  const { get } = useApi();

  const fetchRecentFeedback = async () => {
    const data = await get('/feedback/');
    if (data) {
      setRecentFeedback(data.slice(0, 5)); // Show only recent 5
    }
  };

  useEffect(() => {
    fetchRecentFeedback();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Feedback & Suggestions</h1>
            <p className="text-gray-600">
              Help us improve RailSpark by sharing your feedback, bug reports, and feature requests
            </p>
          </div>
          <div className="text-right">
            <div className="text-4xl mb-2">💬</div>
            <div className="text-sm text-gray-500">Your opinion matters</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Feedback Form */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-gray-800">Share Your Feedback</h2>
              <button
                onClick={() => setShowForm(!showForm)}
                className="bg-gray-100 text-gray-700 px-3 py-1 rounded-lg text-sm hover:bg-gray-200 transition-colors"
              >
                {showForm ? 'Hide Form' : 'Show Form'}
              </button>
            </div>
            {showForm && <FeedbackForm />}
          </div>
        </div>

        {/* Recent Feedback & Statistics */}
        <div className="space-y-6">
          {/* Statistics */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-medium text-gray-900 mb-4">Feedback Statistics</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Total Feedback</span>
                <span className="font-medium text-gray-900">47</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Implemented</span>
                <span className="font-medium text-green-600">12</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">In Progress</span>
                <span className="font-medium text-blue-600">8</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Under Review</span>
                <span className="font-medium text-yellow-600">15</span>
              </div>
            </div>
          </div>

          {/* Recent Feedback */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-medium text-gray-900 mb-4">Recent Feedback</h3>
            <div className="space-y-3">
              {recentFeedback.length > 0 ? (
                recentFeedback.map((feedback, index) => (
                  <div key={index} className="border-l-4 border-blue-500 pl-3 py-1">
                    <div className="text-sm text-gray-900 line-clamp-2">{feedback.feedback_text}</div>
                    <div className="text-xs text-gray-500 mt-1">
                      {new Date(feedback.created_at).toLocaleDateString()}
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-gray-500 text-sm">No recent feedback</div>
              )}
            </div>
          </div>

          {/* Quick Links */}
          <div className="bg-blue-50 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">Need Help?</h4>
            <div className="space-y-2 text-sm">
              <a href="/help" className="block text-blue-700 hover:text-blue-900">📚 User Guide</a>
              <a href="/contact" className="block text-blue-700 hover:text-blue-900">📞 Contact Support</a>
              <a href="/updates" className="block text-blue-700 hover:text-blue-900">🔄 System Updates</a>
            </div>
          </div>
        </div>
      </div>

      {/* Feedback Impact */}
      <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg p-6">
        <h3 className="font-medium text-gray-900 mb-3">How Your Feedback Helps</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm text-gray-700">
          <div className="text-center">
            <div className="text-2xl mb-2">🚀</div>
            <div>Improve System Performance</div>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">🎯</div>
            <div>Enhance User Experience</div>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">💡</div>
            <div>Guide New Features</div>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">🔧</div>
            <div>Fix Issues Quickly</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Feedback;