import React, { createContext, useContext, useEffect, useState } from "react";
import { authApi } from "../services/authApi";
import { AuthTokens, User } from "../types";

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (tokens: AuthTokens) => void;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  updateUser: (updatedUser: User) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshUser = async () => {
    const token = localStorage.getItem("gandheevijaya_access_token");
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }
    try {
      const userData = await authApi.getMe();
      setUser(userData);
    } catch (err) {
      setUser(null);
      localStorage.removeItem("gandheevijaya_access_token");
      localStorage.removeItem("gandheevijaya_refresh_token");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = (tokens: AuthTokens) => {
    localStorage.setItem("gandheevijaya_access_token", tokens.access_token);
    localStorage.setItem("gandheevijaya_refresh_token", tokens.refresh_token);
    setUser(tokens.user);
  };

  const updateUser = (updatedUser: User) => {
    setUser(updatedUser);
  };

  const logout = async () => {
    try {
      await authApi.logout();
    } catch (e) {
      // Ignore API logout errors
    } finally {
      localStorage.removeItem("gandheevijaya_access_token");
      localStorage.removeItem("gandheevijaya_refresh_token");
      setUser(null);
      window.location.href = "/login";
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        refreshUser,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
