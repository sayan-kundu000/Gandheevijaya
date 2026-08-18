import { apiClient } from "./apiClient";
import { AuthTokens, User } from "../types";

export const authApi = {
  login: async (credentials: Record<string, string>): Promise<AuthTokens> => {
    const email = credentials.email || credentials.username || "";
    const password = credentials.password || "";

    const response = await apiClient.post<AuthTokens>("/auth/login", {
      email,
      password,
    });
    return response.data;
  },

  register: async (payload: {
    email: string;
    password: string;
    full_name: string;
    target_exams?: string[];
    target_exam?: string;
  }): Promise<AuthTokens> => {
    await apiClient.post("/auth/register", {
      email: payload.email,
      password: payload.password,
      full_name: payload.full_name,
      target_exams: payload.target_exams || (payload.target_exam ? [payload.target_exam] : ["GATE_CS"]),
    });
    // Automatically log in to get session tokens
    return authApi.login({ email: payload.email, password: payload.password });
  },

  getMe: async (): Promise<User> => {
    const response = await apiClient.get<User>("/auth/me");
    return response.data;
  },

  updateProfile: async (payload: {
    full_name?: string;
    target_exams?: string[];
  }): Promise<User> => {
    const response = await apiClient.patch<User>("/users/me", payload);
    return response.data;
  },

  logout: async (): Promise<{ message: string }> => {
    const refreshToken = localStorage.getItem("gandheevijaya_refresh_token");
    const response = await apiClient.post<{ message: string }>("/auth/logout", {
      refresh_token: refreshToken,
    });
    return response.data;
  },
};
