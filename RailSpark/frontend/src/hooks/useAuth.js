import { useState, useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { useApi } from './useApi';

export const useAuth = () => {
  const { user, token, login: contextLogin, logout: contextLogout } = useContext(AuthContext);
  const { post, loading, error } = useApi();
  const [authLoading, setAuthLoading] = useState(false);

  const login = async (username, password) => {
    setAuthLoading(true);
    try {
      const result = await contextLogin(username, password);
      return result;
    } catch (err) {
      console.error('Login error:', err);
      return { success: false, error: err.message };
    } finally {
      setAuthLoading(false);
    }
  };

  const register = async (userData) => {
    setAuthLoading(true);
    try {
      const response = await post('/auth/register', userData);
      if (response) {
        return { success: true, message: 'Registration successful' };
      }
      return { success: false, error: 'Registration failed' };
    } catch (err) {
      return { success: false, error: err.message };
    } finally {
      setAuthLoading(true);
    }
  };

  const logout = () => {
    contextLogout();
  };

  const changePassword = async (currentPassword, newPassword) => {
    try {
      const response = await post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword
      });
      return { success: !!response, message: response?.message };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  const refreshToken = async () => {
    // This would typically call a refresh token endpoint
    console.log('Token refresh functionality would be implemented here');
  };

  const hasRole = (requiredRole) => {
    if (!user || !user.role) return false;
    return user.role === requiredRole;
  };

  const hasAnyRole = (requiredRoles) => {
    if (!user || !user.role) return false;
    return requiredRoles.includes(user.role);
  };

  return {
    // State
    user,
    token,
    isAuthenticated: !!token,
    
    // Loading states
    loading: authLoading || loading,
    authLoading,
    error,
    
    // Actions
    login,
    register,
    logout,
    changePassword,
    refreshToken,
    
    // Role-based access
    hasRole,
    hasAnyRole,
    
    // User info shortcuts
    isOperator: user?.role === 'operator',
    isSupervisor: user?.role === 'supervisor',
    isAdmin: user?.role === 'admin'
  };
};