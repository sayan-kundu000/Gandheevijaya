import axios from "axios";

// Environment-driven API base URL default
const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: `${baseURL.replace(/\/$/, "")}/api/v1`,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

// Request Interceptor: Automatically attach Access Token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("gandheevijaya_access_token");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Centralized 401 Session Expiration Handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("gandheevijaya_refresh_token");

      if (refreshToken) {
        try {
          const refreshRes = await axios.post(`${baseURL.replace(/\/$/, "")}/api/v1/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const newAccessToken = refreshRes.data.access_token;
          const newRefreshToken = refreshRes.data.refresh_token;

          localStorage.setItem("gandheevijaya_access_token", newAccessToken);
          if (newRefreshToken) {
            localStorage.setItem("gandheevijaya_refresh_token", newRefreshToken);
          }

          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return apiClient(originalRequest);
        } catch (refreshErr) {
          // Token refresh failed -> Clear session and redirect to login
          localStorage.removeItem("gandheevijaya_access_token");
          localStorage.removeItem("gandheevijaya_refresh_token");
          if (window.location.pathname !== "/login") {
            window.location.href = "/login";
          }
        }
      } else {
        localStorage.removeItem("gandheevijaya_access_token");
        if (window.location.pathname !== "/login") {
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);
