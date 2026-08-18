import { apiClient } from "./apiClient";
import {
  DashboardOverview,
  SubjectProgressItem,
  TopicProgressItem,
  WeakAreaItem,
} from "../types";

export const dashboardApi = {
  getOverview: async (): Promise<DashboardOverview> => {
    const response = await apiClient.get<DashboardOverview>("/dashboard/overview");
    return response.data;
  },

  getSubjectProgress: async (): Promise<{ items: SubjectProgressItem[] }> => {
    const response = await apiClient.get<{ items: SubjectProgressItem[] }>("/dashboard/subject-progress");
    return response.data;
  },

  getTopicProgress: async (): Promise<{ items: TopicProgressItem[] }> => {
    const response = await apiClient.get<{ items: TopicProgressItem[] }>("/dashboard/topic-progress");
    return response.data;
  },

  getWeakAreas: async (): Promise<{ items: WeakAreaItem[] }> => {
    const response = await apiClient.get<{ items: WeakAreaItem[] }>("/dashboard/weak-areas");
    return response.data;
  },
};
