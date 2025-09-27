import { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { token, logout } = useContext(AuthContext);

  const BASE_URL = 'http://localhost:8000';

  // useApi.js - Update the request function
const request = async (endpoint, options = {}) => {
  setLoading(true);
  setError(null);

  try {
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    // Handle FormData (for file uploads)
    if (options.body instanceof FormData) {
      delete config.headers['Content-Type'];
    } else if (config.headers['Content-Type'] === 'application/json' && options.body) {
      config.body = JSON.stringify(options.body);
    }

    console.log('API Request:', {
      endpoint: `${BASE_URL}${endpoint}`,
      method: config.method,
      body: config.body,
      headers: config.headers
    });

    const response = await fetch(`${BASE_URL}${endpoint}`, config);
    
    // Handle unauthorized responses
    if (response.status === 401) {
      logout();
      throw new Error('Authentication required. Please login again.');
    }

    if (!response.ok) {
      // Try to get detailed error message
      let errorDetail = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorData.message || JSON.stringify(errorData);
      } catch (parseError) {
        const textError = await response.text();
        errorDetail = textError || errorDetail;
      }
      throw new Error(errorDetail);
    }

    // Handle empty responses
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      const data = await response.json();
      return data;
    } else {
      return await response.text();
    }
  } catch (err) {
  const errorMessage = err.message || 'An unexpected error occurred';
  setError(errorMessage);
  console.error('API request failed:', err);
  
  // ✅ Throw a proper Error object with the message
  if (err instanceof Error) {
    throw err; // If it's already an Error object, re-throw it
  } else {
    throw new Error(errorMessage); // Convert to proper Error object
  }
} finally {
    setLoading(false);
  }
};

  const get = (endpoint, options = {}) => 
    request(endpoint, { ...options, method: 'GET' });

  const post = (endpoint, data = null, options = {}) => 
    request(endpoint, { ...options, method: 'POST', body: data });

  const put = (endpoint, data = null, options = {}) => 
    request(endpoint, { ...options, method: 'PUT', body: data });

  const patch = (endpoint, data = null, options = {}) => 
    request(endpoint, { ...options, method: 'PATCH', body: data });

  const del = (endpoint, options = {}) => 
    request(endpoint, { ...options, method: 'DELETE' });

  const clearError = () => setError(null);

  return { 
    get, 
    post, 
    put, 
    patch, 
    del, 
    loading, 
    error, 
    clearError 
  };
};