import { apiClient } from "./apiClient";
import { Result } from "../types";

export const resultsApi = {
  getResult: async (resultId: string): Promise<Result> => {
    const response = await apiClient.get<Result>(`/results/${resultId}`);
    return response.data;
  },

  getUserHistory: async (): Promise<Result[]> => {
    const response = await apiClient.get<any>("/attempts", {
      params: { status: "SUBMITTED", page_size: 50 },
    });
    const data = response.data;
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.items)) return data.items;
    return [];
  },
};

