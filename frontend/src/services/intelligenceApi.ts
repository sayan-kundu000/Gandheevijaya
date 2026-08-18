import { apiClient } from "./apiClient";
import {
  PerformanceDelta,
  PrescriptiveRecommendation,
  SpeedAccuracyResponse,
  StudentIntelligenceProfile,
  TopicMatrixItem,
} from "../types";

export const intelligenceApi = {
  getProfile: async (): Promise<StudentIntelligenceProfile> => {
    const response = await apiClient.get<StudentIntelligenceProfile>("/intelligence/student/profile");
    return response.data;
  },

  getRecommendations: async (limit: number = 5): Promise<{ items: PrescriptiveRecommendation[] }> => {
    const response = await apiClient.get<{ items: PrescriptiveRecommendation[] }>(
      "/intelligence/student/recommendations",
      { params: { limit } }
    );
    return response.data;
  },

  getSpeedAccuracy: async (): Promise<SpeedAccuracyResponse> => {
    const response = await apiClient.get<SpeedAccuracyResponse>("/intelligence/student/speed-accuracy");
    return response.data;
  },

  getPerformanceDelta: async (days: number = 7): Promise<PerformanceDelta> => {
    const response = await apiClient.get<PerformanceDelta>("/intelligence/student/performance-delta", {
      params: { days },
    });
    return response.data;
  },

  getTopicMatrix: async (): Promise<{ items: TopicMatrixItem[] }> => {
    const response = await apiClient.get<{ items: TopicMatrixItem[] }>("/intelligence/topics/matrix");
    return response.data;
  },
};
