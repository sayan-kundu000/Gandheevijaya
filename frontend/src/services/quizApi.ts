import { apiClient } from "./apiClient";
import { Quiz, StartQuizResponse } from "../types";

export const quizApi = {
  getQuizzes: async (filters?: {
    exam_id?: number;
    subject_id?: number;
    topic_id?: number;
    search?: string;
    page_size?: number;
  }): Promise<Quiz[]> => {
    const params: Record<string, any> = { page_size: 500, ...filters };
    const response = await apiClient.get<any>("/quizzes", { params });
    const data = response.data;
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.items)) return data.items;
    return [];
  },

  getQuizDetails: async (quizId: number): Promise<Quiz> => {
    const response = await apiClient.get<Quiz>(`/quizzes/${quizId}`);
    return response.data;
  },

  startQuiz: async (quizId: number): Promise<StartQuizResponse> => {
    const response = await apiClient.post<StartQuizResponse>(`/quizzes/${quizId}/start`);
    return response.data;
  },
};

