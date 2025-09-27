import React, { useState, useRef, useEffect, useContext } from 'react';
import { useApi } from '../../hooks/useApi';
import { AuthContext } from '../../contexts/AuthContext';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState([]);
  const messagesEndRef = useRef(null);
  const { user } = useContext(AuthContext);
  const { post, loading } = useApi();

  const suggestedQueries = [
    "Show me tomorrow's induction plan",
    "Which trains need maintenance?",
    "What if I add 2 more trains?",
    "Predict failure risks for all trains",
    "Which branding contracts need attention?",
    "Check train KMRL-001 fitness status",
    "Generate optimized schedule for next week",
    "What if maintenance takes 3 days?",
    "Show me current train eligibility",
    "What's our branding capacity?"
  ];

  useEffect(() => {
    // Initialize with welcome message
    setMessages([
      {
        id: 1,
        type: 'bot',
        content: "Hello! I'm your RailSpark assistant. I can help you with train scheduling, maintenance planning, what-if scenarios, and more. How can I assist you today?",
        timestamp: new Date(),
        data: null
      }
    ]);
    
    // Shuffle and pick 4 random suggested questions
    const shuffled = [...suggestedQueries].sort(() => 0.5 - Math.random());
    setSuggestedQuestions(shuffled.slice(0, 4));
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async (message = inputMessage) => {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await post('/chatbot/query', {
        message: message,
        user_id: user?.id || 1
      });

      if (response) {
        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: response.message,
          timestamp: new Date(),
          data: response.data,
          messageType: response.type
        };
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: "Sorry, I encountered an error. Please try again.",
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleSuggestionClick = (question) => {
    sendMessage(question);
  };

  const formatMessage = (content) => {
    // Convert line breaks to <br> tags and format lists
    return content.split('\n').map((line, index) => {
      if (line.startsWith('•') || line.startsWith('-')) {
        return <div key={index} className="flex"><span className="mr-2">•</span>{line.substring(1)}</div>;
      }
      return <div key={index}>{line}</div>;
    });
  };

  const renderMessage = (message) => {
    const isBot = message.type === 'bot';
    
    return (
      <div key={message.id} className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4`}>
        <div className={`flex max-w-[80%] ${isBot ? 'flex-row' : 'flex-row-reverse'}`}>
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
            isBot ? 'bg-blue-100 text-blue-600 mr-3' : 'bg-green-100 text-green-600 ml-3'
          }`}>
            {isBot ? '🤖' : '👤'}
          </div>
          <div className={`rounded-lg p-4 ${
            isBot 
              ? 'bg-blue-50 border border-blue-100' 
              : message.isError
                ? 'bg-red-50 border border-red-100'
                : 'bg-green-50 border border-green-100'
          }`}>
            <div className="text-sm text-gray-600 mb-1">
              {isBot ? 'RailSpark Assistant' : 'You'} • {message.timestamp.toLocaleTimeString()}
            </div>
            <div className={`${message.isError ? 'text-red-700' : 'text-gray-800'}`}>
              {formatMessage(message.content)}
            </div>
            
            {/* Render data if available */}
            {message.data && message.messageType === 'induction_plan' && (
              <div className="mt-3 p-3 bg-white rounded border">
                <h4 className="font-medium mb-2">Induction Plan Details:</h4>
                <div className="text-sm space-y-1">
                  {message.data.slice(0, 3).map((plan, idx) => (
                    <div key={idx} className="flex justify-between">
                      <span>Train {plan.train_id}</span>
                      <span className="capitalize">{plan.induction_type}</span>
                    </div>
                  ))}
                  {message.data.length > 3 && (
                    <div className="text-gray-500">... and {message.data.length - 3} more</div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-lg h-[600px] flex flex-col">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center mr-3">
              <span className="text-xl">🤖</span>
            </div>
            <div>
              <h2 className="text-xl font-bold">RailSpark Assistant</h2>
              <p className="text-blue-100 text-sm">AI-powered train scheduling help</p>
            </div>
          </div>
          <div className="text-blue-200 text-sm">
            {isLoading ? 'Thinking...' : 'Online'}
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {messages.map(renderMessage)}
          
          {isLoading && (
            <div className="flex justify-start mb-4">
              <div className="flex max-w-[80%]">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 text-blue-600 mr-3 flex items-center justify-center">
                  🤖
                </div>
                <div className="bg-blue-50 rounded-lg p-4">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Suggested Questions */}
      {messages.length <= 2 && (
        <div className="px-4 pb-2">
          <div className="text-sm text-gray-600 mb-2">Try asking:</div>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(question)}
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs px-3 py-1 rounded-full transition-colors"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t p-4">
        <div className="flex space-x-2">
          <div className="flex-1">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about schedules, maintenance, what-if scenarios..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows={2}
              disabled={isLoading}
            />
          </div>
          <button
            onClick={() => sendMessage()}
            disabled={isLoading || !inputMessage.trim()}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed self-end"
          >
            Send
          </button>
        </div>
        <div className="text-xs text-gray-500 mt-1">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>

      {/* Quick Actions */}
      <div className="border-t p-2 bg-gray-50">
        <div className="flex justify-center space-x-4 text-xs">
          <button 
            onClick={() => sendMessage("Show me today's induction plan")}
            className="text-blue-600 hover:text-blue-800"
          >
            📋 Today's Plan
          </button>
          <button 
            onClick={() => sendMessage("What if I add 2 more trains?")}
            className="text-green-600 hover:text-green-800"
          >
            🔍 What-If
          </button>
          <button 
            onClick={() => sendMessage("Predict failure risks")}
            className="text-red-600 hover:text-red-800"
          >
            ⚠️ Risk Check
          </button>
          <button 
            onClick={() => sendMessage("Help")}
            className="text-purple-600 hover:text-purple-800"
          >
            ❓ Help
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;