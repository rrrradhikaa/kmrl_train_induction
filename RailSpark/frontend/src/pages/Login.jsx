import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await login(username, password);
      if (result.success) {
        navigate('/');
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  const demoLogin = (role) => {
    const demoCredentials = {
      operator: { username: 'operator', password: 'operator123' },
      supervisor: { username: 'supervisor', password: 'supervisor123' },
      admin: { username: 'admin', password: 'admin123' }
    };

    const creds = demoCredentials[role];
    setUsername(creds.username);
    setPassword(creds.password);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center">
              <span className="text-3xl">🚆</span>
            </div>
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">RailSpark</h1>
          <p className="text-blue-100">KMRL Train Induction System</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Sign In</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="username" className="form-label">Username</label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="form-input"
                placeholder="Enter your username"
                required
                disabled={loading}
              />
            </div>

            <div>
              <label htmlFor="password" className="form-label">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-input"
                placeholder="Enter your password"
                required
                disabled={loading}
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <div className="flex items-center">
                  <span className="text-red-600 mr-2">❌</span>
                  <span className="text-red-700 text-sm">{error}</span>
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-3 text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="spinner w-5 h-5 mr-2"></div>
                  Signing In...
                </div>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Demo Login Buttons */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-center text-gray-600 text-sm mb-4">Quick Demo Access:</p>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => demoLogin('operator')}
                className="btn-outline py-2 text-xs"
                disabled={loading}
              >
                Operator
              </button>
              <button
                onClick={() => demoLogin('supervisor')}
                className="btn-outline py-2 text-xs"
                disabled={loading}
              >
                Supervisor
              </button>
              <button
                onClick={() => demoLogin('admin')}
                className="btn-outline py-2 text-xs"
                disabled={loading}
              >
                Admin
              </button>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-6 text-center">
            <p className="text-gray-500 text-sm">
              Forgot your password?{' '}
              <a href="/reset-password" className="text-blue-600 hover:text-blue-800">
                Reset it here
              </a>
            </p>
          </div>
        </div>

        {/* System Info */}
        <div className="mt-6 text-center">
          <p className="text-blue-200 text-sm">
            RailSpark v1.0 • AI-Driven Train Induction System
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;