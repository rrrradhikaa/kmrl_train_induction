import React from 'react';
import ChatInterface from '../components/Chatbot/ChatInterface';

const Chatbot = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">AI Assistant</h1>
            <p className="text-gray-600">
              Get intelligent help with scheduling, what-if scenarios, and train management
            </p>
          </div>
          <div className="text-right">
            <div className="text-4xl mb-2">🤖</div>
            <div className="text-sm text-gray-500">Powered by AI</div>
          </div>
        </div>
      </div>

      {/* Chat Interface */}
      <ChatInterface />

      {/* Quick Scenarios */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4 text-center">
          <div className="text-2xl mb-2">📋</div>
          <h3 className="font-medium text-gray-900 mb-1">Plan Generation</h3>
          <p className="text-xs text-gray-600">Create optimized induction plans</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4 text-center">
          <div className="text-2xl mb-2">🔍</div>
          <h3 className="font-medium text-gray-900 mb-1">What-If Analysis</h3>
          <p className="text-xs text-gray-600">Simulate different scenarios</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4 text-center">
          <div className="text-2xl mb-2">⚡</div>
          <h3 className="font-medium text-gray-900 mb-1">Quick Checks</h3>
          <p className="text-xs text-gray-600">Instant status and eligibility</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4 text-center">
          <div className="text-2xl mb-2">📊</div>
          <h3 className="font-medium text-gray-900 mb-1">Predictive Insights</h3>
          <p className="text-xs text-gray-600">Risk assessment and forecasts</p>
        </div>
      </div>

      {/* Capabilities */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-medium text-blue-900 mb-3">What I Can Help You With</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
          <div>
            <strong>📅 Scheduling & Planning:</strong>
            <ul className="mt-1 space-y-1">
              <li>• Generate daily induction plans</li>
              <li>• Optimize train assignments</li>
              <li>• Balance mileage and maintenance</li>
              <li>• Handle branding commitments</li>
            </ul>
          </div>
          <div>
            <strong>🔮 Analysis & Prediction:</strong>
            <ul className="mt-1 space-y-1">
              <li>• What-if scenario simulation</li>
              <li>• Failure risk prediction</li>
              <li>• Capacity planning analysis</li>
              <li>• Performance optimization</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;