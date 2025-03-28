import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '@shared/types';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoading: true,
  isAuthenticated: false,
  login: async () => {},
  logout: async () => {},
  register: async () => {},
});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in on app load
    const checkAuthStatus = async () => {
      try {
        // In a real app, you would make an API call to validate the token
        // and get the current user's information
        const token = localStorage.getItem('token');

        if (token) {
          // This is a placeholder - you would fetch the user data from your API
          // For demo purposes, we're creating a mock user
          const mockUser: User = {
            id: 'user-123',
            email: 'user@example.com',
            name: 'Test User',
            isActive: true,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          };

          setUser(mockUser);
        }
      } catch (error) {
        console.error('Authentication error:', error);
        // Clear any invalid tokens
        localStorage.removeItem('token');
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);

      // In a real app, you would make an API call to authenticate
      // and get a token and user data

      // For demo purposes, we're creating a mock token and user
      const mockToken = 'mock-jwt-token';
      const mockUser: User = {
        id: 'user-123',
        email,
        name: 'Test User',
        isActive: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      localStorage.setItem('token', mockToken);
      setUser(mockUser);
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      setIsLoading(true);

      // In a real app, you might want to invalidate the token on the server

      localStorage.removeItem('token');
      setUser(null);
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (email: string, password: string, name: string) => {
    try {
      setIsLoading(true);

      // In a real app, you would make an API call to register the user

      // After registration, we can log the user in automatically
      await login(email, password);
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const value = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    logout,
    register,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
