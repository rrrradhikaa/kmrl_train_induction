import { useApi } from '../hooks/useApi';

// Authentication service functions
export const useAuthService = () => {
  const { post, get } = useApi();

  return {
    // Login with username and password
    login: async (username, password) => {
      try {
        // Using form data as required by FastAPI
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await post('/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });

        if (response && response.access_token) {
          return {
            success: true,
            token: response.access_token,
            user: {
              id: response.user_id,
              username: response.username,
              role: response.role
            }
          };
        } else {
          return {
            success: false,
            error: response?.detail || 'Login failed'
          };
        }
      } catch (error) {
        return {
          success: false,
          error: error.message || 'Login failed'
        };
      }
    },

    // Register new user
    register: async (userData) => {
      try {
        const response = await post('/auth/register', userData);
        
        if (response) {
          return {
            success: true,
            message: 'Registration successful'
          };
        } else {
          return {
            success: false,
            error: 'Registration failed'
          };
        }
      } catch (error) {
        return {
          success: false,
          error: error.message || 'Registration failed'
        };
      }
    },

    // Get current user info
    getCurrentUser: async (token) => {
      try {
        const response = await get('/auth/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response) {
          return {
            success: true,
            user: response
          };
        } else {
          return {
            success: false,
            error: 'Failed to fetch user info'
          };
        }
      } catch (error) {
        return {
          success: false,
          error: error.message || 'Failed to fetch user info'
        };
      }
    },

    // Change password
    changePassword: async (currentPassword, newPassword) => {
      try {
        const response = await post('/auth/change-password', {
          current_password: currentPassword,
          new_password: newPassword
        });

        if (response) {
          return {
            success: true,
            message: 'Password changed successfully'
          };
        } else {
          return {
            success: false,
            error: 'Password change failed'
          };
        }
      } catch (error) {
        return {
          success: false,
          error: error.message || 'Password change failed'
        };
      }
    },

    // Reset password (initiate)
    resetPassword: async (email) => {
      try {
        const response = await post('/auth/reset-password', { email });
        
        return {
          success: true,
          message: 'Password reset instructions sent to your email'
        };
      } catch (error) {
        return {
          success: false,
          error: error.message || 'Password reset failed'
        };
      }
    },

    // Verify token validity
    verifyToken: async (token) => {
      try {
        const response = await get('/auth/verify', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        return {
          success: true,
          valid: response.valid || false
        };
      } catch (error) {
        return {
          success: false,
          valid: false,
          error: error.message
        };
      }
    },

    // Logout (client-side only - backend might have token blacklisting)
    logout: async () => {
      // Client-side cleanup - backend logout would be called here if implemented
      return { success: true };
    }
  };
};

// Utility functions for authentication
export const authUtils = {
  // Check if user has required role
  hasRole: (user, requiredRole) => {
    return user && user.role === requiredRole;
  },

  // Check if user has any of the required roles
  hasAnyRole: (user, requiredRoles) => {
    return user && requiredRoles.includes(user.role);
  },

  // Check if user is authenticated
  isAuthenticated: (token) => {
    return !!token;
  },

  // Validate password strength
  validatePassword: (password) => {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    const issues = [];
    
    if (password.length < minLength) {
      issues.push(`Password must be at least ${minLength} characters long`);
    }
    if (!hasUpperCase) {
      issues.push('Password must contain at least one uppercase letter');
    }
    if (!hasLowerCase) {
      issues.push('Password must contain at least one lowercase letter');
    }
    if (!hasNumbers) {
      issues.push('Password must contain at least one number');
    }
    if (!hasSpecialChar) {
      issues.push('Password must contain at least one special character');
    }

    return {
      isValid: issues.length === 0,
      issues
    };
  },

  // Validate email format
  validateEmail: (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  // Generate random password
  generatePassword: (length = 12) => {
    const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
    let password = '';
    for (let i = 0; i < length; i++) {
      password += charset.charAt(Math.floor(Math.random() * charset.length));
    }
    return password;
  }
};

// Default export for easy importing
export default useAuthService;