import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '../config/api';

interface User {
  id: string;
  username: string;
  email: string;
  native_language: string;
  target_language: string;
  created_at: string;
  is_active: boolean;
  preferences: Record<string, any>;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, native_language: string, target_language: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check if user is already logged in on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      checkAuthStatus();
    } else {
      setIsLoading(false);
    }
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setIsLoading(false);
        return;
      }
      
      const response = await api.get('/api/v1/auth/me');
      setUser(response.data);
      setError(null);
    } catch (err) {
      console.error('Auth check failed:', err);
      localStorage.removeItem('token');
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await api.post('/api/v1/auth/login', {
        username: email,  // ✅ FIXED: Changed from 'email' to 'username'
        password,
      });

      const { access_token, user: userData } = response.data;
      
      // Store token
      localStorage.setItem('token', access_token);
      
      setUser(userData);
      setError(null);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Login failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (
    username: string, 
    email: string, 
    password: string, 
    native_language: string, 
    target_language: string
  ) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await api.post('/api/v1/auth/register', {
        username,
        email,
        password,
        native_language,
        target_language,
      });

      const { access_token, user: userData } = response.data;
      
      // Store token
      localStorage.setItem('token', access_token);
      
      setUser(userData);
      setError(null);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Registration failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setError(null);
  };

  const value: AuthContextType = {
    user,
    login,
    register,
    logout,
    isLoading,
    error,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 