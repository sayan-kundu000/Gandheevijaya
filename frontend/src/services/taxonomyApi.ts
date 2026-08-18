import { apiClient } from "./apiClient";
import { Exam, Subject, Topic } from "../types";

export const taxonomyApi = {
  getExams: async (): Promise<Exam[]> => {
    const response = await apiClient.get<any>("/exams");
    const data = response.data;
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.items)) return data.items;
    return [];
  },

  getSubjects: async (examId?: number): Promise<Subject[]> => {
    const params: Record<string, any> = { page_size: 100 };
    if (examId) params.exam_id = examId;
    const response = await apiClient.get<any>("/subjects", { params });
    const data = response.data;
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.items)) return data.items;
    return [];
  },

  getTopics: async (subjectId?: number): Promise<Topic[]> => {
    const params: Record<string, any> = { page_size: 100 };
    if (subjectId) params.subject_id = subjectId;
    const response = await apiClient.get<any>("/topics", { params });
    const data = response.data;
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.items)) return data.items;
    return [];
  },
};

