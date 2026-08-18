import { apiClient } from "./apiClient";
import { AttemptResumeResponse, Result } from "../types";

export const attemptApi = {
  getAttempt: async (attemptId: string): Promise<AttemptResumeResponse> => {
    const response = await apiClient.get<AttemptResumeResponse>(`/attempts/${attemptId}`);
    return response.data;
  },

  saveResponse: async (
    attemptId: string,
    payload: {
      question_id: string;
      selected_answer: string | null;
      marked_for_review?: boolean;
    }
  ): Promise<{ message: string }> => {
    const response = await apiClient.post<{ message: string }>(
      `/attempts/${attemptId}/responses`,
      payload
    );
    return response.data;
  },

  submitAttempt: async (attemptId: string): Promise<Result> => {
    const response = await apiClient.post<Result>(`/attempts/${attemptId}/submit`);
    return response.data;
  },
};
