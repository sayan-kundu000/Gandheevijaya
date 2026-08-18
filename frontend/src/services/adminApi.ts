import { apiClient } from "./apiClient";
import {
  AdminDashboardOverview,
  AdminUserItem,
  AdminUserDetailResponse,
  Question,
  Quiz,
  ContentImportJobItem,
  ContentImportJobDetailResponse,
  ContentImportReport,
  ContentHealthReport,
  SecurityAuditLogItem,
  QuestionPoolInfoResponse,
  AdminExamCreateRequest,
  AdminSubjectCreateRequest,
  AdminTopicCreateRequest,
  AdminQuestionCreateRequest,
  AdminQuestionUpdateRequest,
  Attempt,
} from "../types";

export const adminApi = {
  // Dashboard & System Statistics
  getOverview: async (): Promise<AdminDashboardOverview> => {
    const response = await apiClient.get<AdminDashboardOverview>("/admin/dashboard");
    return response.data;
  },

  getStats: async (): Promise<Record<string, any>> => {
    const response = await apiClient.get<Record<string, any>>("/admin/stats");
    return response.data;
  },

  // User Management
  getUsers: async (params?: {
    search?: string;
    role?: string;
    is_active?: boolean;
    page?: number;
    page_size?: number;
  }): Promise<{ items: AdminUserItem[]; total: number }> => {
    const response = await apiClient.get<{ items: AdminUserItem[]; total: number }>("/admin/users", { params });
    return response.data;
  },

  getUserDetail: async (userId: string): Promise<AdminUserDetailResponse> => {
    const response = await apiClient.get<AdminUserDetailResponse>(`/admin/users/${userId}`);
    return response.data;
  },

  updateUser: async (userId: string, body: { full_name?: string; role?: string }): Promise<AdminUserItem> => {
    const response = await apiClient.patch<AdminUserItem>(`/admin/users/${userId}`, body);
    return response.data;
  },

  disableUser: async (userId: string, reason?: string): Promise<AdminUserDetailResponse> => {
    const response = await apiClient.post<AdminUserDetailResponse>(`/admin/users/${userId}/disable`, { reason });
    return response.data;
  },

  reactivateUser: async (userId: string, reason?: string): Promise<AdminUserDetailResponse> => {
    const response = await apiClient.post<AdminUserDetailResponse>(`/admin/users/${userId}/reactivate`, { reason });
    return response.data;
  },

  // Question Bank Management
  getQuestions: async (params?: {
    topic_id?: number;
    status?: string;
    question_type?: string;
    difficulty?: string;
    page?: number;
    page_size?: number;
  }): Promise<{ items: Question[]; total: number }> => {
    const response = await apiClient.get<{ items: Question[]; total: number }>("/admin/questions", { params });
    return response.data;
  },

  getQuestionDetail: async (questionId: string): Promise<Question> => {
    const response = await apiClient.get<Question>(`/questions/${questionId}`);
    return response.data;
  },

  createQuestion: async (body: AdminQuestionCreateRequest): Promise<Question> => {
    const response = await apiClient.post<Question>("/admin/questions", body);
    return response.data;
  },

  updateQuestion: async (questionId: string, body: AdminQuestionUpdateRequest): Promise<Question> => {
    const response = await apiClient.patch<Question>(`/admin/questions/${questionId}`, body);
    return response.data;
  },

  publishQuestion: async (questionId: string): Promise<Question> => {
    const response = await apiClient.post<Question>(`/admin/questions/${questionId}/publish`);
    return response.data;
  },

  unpublishQuestion: async (questionId: string): Promise<Question> => {
    const response = await apiClient.post<Question>(`/admin/questions/${questionId}/unpublish`);
    return response.data;
  },

  archiveQuestion: async (questionId: string): Promise<Question> => {
    const response = await apiClient.post<Question>(`/admin/questions/${questionId}/archive`);
    return response.data;
  },

  bulkUpdateQuestionStatus: async (item_ids: string[], status: string): Promise<{ message: string }> => {
    const response = await apiClient.post<{ message: string }>("/admin/questions/bulk-status", {
      item_ids,
      status,
    });
    return response.data;
  },

  // Taxonomy Creation
  createExam: async (body: AdminExamCreateRequest): Promise<{ id: number; code: string; name: string }> => {
    const response = await apiClient.post<{ id: number; code: string; name: string }>("/admin/exams", body);
    return response.data;
  },

  createSubject: async (body: AdminSubjectCreateRequest): Promise<{ id: number; code: string; name: string }> => {
    const response = await apiClient.post<{ id: number; code: string; name: string }>("/admin/subjects", body);
    return response.data;
  },

  createTopic: async (body: AdminTopicCreateRequest): Promise<{ id: number; code: string; name: string }> => {
    const response = await apiClient.post<{ id: number; code: string; name: string }>("/admin/topics", body);
    return response.data;
  },

  // Quiz Management
  createQuiz: async (body: any): Promise<Quiz> => {
    const response = await apiClient.post<Quiz>("/quizzes", body);
    return response.data;
  },

  updateQuiz: async (quizId: number, body: any): Promise<Quiz> => {
    const response = await apiClient.patch<Quiz>(`/quizzes/${quizId}`, body);
    return response.data;
  },

  publishQuiz: async (quizId: number): Promise<Quiz> => {
    const response = await apiClient.post<Quiz>(`/admin/quizzes/${quizId}/publish`);
    return response.data;
  },

  archiveQuiz: async (quizId: number): Promise<Quiz> => {
    const response = await apiClient.post<Quiz>(`/admin/quizzes/${quizId}/archive`);
    return response.data;
  },

  inspectQuestionPool: async (quizId: number): Promise<QuestionPoolInfoResponse> => {
    const response = await apiClient.get<QuestionPoolInfoResponse>(`/admin/quizzes/${quizId}/question-pool`);
    return response.data;
  },

  // Ingestion & ETL Monitoring
  getImportJobs: async (params?: { page?: number; page_size?: number }): Promise<{ items: ContentImportJobItem[]; total: number }> => {
    const response = await apiClient.get<{ items: ContentImportJobItem[]; total: number }>("/admin/imports", { params });
    return response.data;
  },

  getImportJobDetail: async (jobId: number): Promise<ContentImportJobDetailResponse> => {
    const response = await apiClient.get<ContentImportJobDetailResponse>(`/admin/imports/${jobId}`);
    return response.data;
  },

  triggerImport: async (params: {
    source_path?: string;
    dry_run?: boolean;
    upsert?: boolean;
    subject?: string;
  }): Promise<ContentImportReport> => {
    const response = await apiClient.post<ContentImportReport>("/admin/import/questions", null, { params });
    return response.data;
  },

  // Content Quality & Health Scanning
  getContentHealthReport: async (): Promise<ContentHealthReport> => {
    const response = await apiClient.get<ContentHealthReport>("/admin/content/health");
    return response.data;
  },

  // Attempts & Audit Logs Monitoring
  getAdminAttempts: async (params?: {
    user_id?: string;
    quiz_id?: number;
    status?: string;
    page?: number;
    page_size?: number;
  }): Promise<{ items: Attempt[]; total: number }> => {
    const response = await apiClient.get<{ items: Attempt[]; total: number }>("/admin/attempts", { params });
    return response.data;
  },

  getAuditLogs: async (params?: {
    event_type?: string;
    user_id?: string;
    page?: number;
    page_size?: number;
  }): Promise<{ items: SecurityAuditLogItem[]; total: number }> => {
    const response = await apiClient.get<{ items: SecurityAuditLogItem[]; total: number }>("/admin/audit-logs", { params });
    return response.data;
  },
};
