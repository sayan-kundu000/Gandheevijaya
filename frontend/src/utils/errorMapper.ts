import { AxiosError } from "axios";

export interface BackendErrorDetail {
  loc?: (string | number)[];
  msg?: string;
  type?: string;
}

export interface BackendErrorPayload {
  error?: {
    code?: string;
    message?: string;
    details?: BackendErrorDetail[] | string | null;
    request_id?: string;
  };
}

export const getErrorMessage = (error: unknown, fallbackMessage = "An unexpected error occurred."): string => {
  if (!error) return fallbackMessage;

  if (typeof error === "string") return error;

  const axiosErr = error as AxiosError<BackendErrorPayload>;

  if (axiosErr.response?.data?.error) {
    const backendErr = axiosErr.response.data.error;

    if (backendErr.message) {
      return backendErr.message;
    }

    if (Array.isArray(backendErr.details) && backendErr.details.length > 0) {
      const firstDetail = backendErr.details[0];
      if (firstDetail.msg) {
        return firstDetail.msg;
      }
    }
  }

  if (axiosErr.response?.status === 401) {
    return "Your session has expired. Please log in again.";
  }

  if (axiosErr.response?.status === 403) {
    return "You do not have permission to access this resource.";
  }

  if (axiosErr.response?.status === 404) {
    return "The requested resource was not found.";
  }

  if (axiosErr.response?.status === 429) {
    return "Too many requests. Please wait a moment before trying again.";
  }

  if (axiosErr.message === "Network Error") {
    return "Unable to connect to Gandheevijaya backend server. Please check your internet connection.";
  }

  return axiosErr.message || fallbackMessage;
};
