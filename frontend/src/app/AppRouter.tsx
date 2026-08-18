import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "../context/AuthContext";
import { ToastProvider } from "../components/feedback/ToastProvider";
import { ErrorBoundary } from "../components/common/ErrorBoundary";
import { ProtectedRoute } from "../components/common/ProtectedRoute";

import { LoginPage } from "../pages/Auth/LoginPage";
import { RegisterPage } from "../pages/Auth/RegisterPage";
import { ProfilePage } from "../pages/Auth/ProfilePage";
import { StudentDashboardPage } from "../pages/Dashboard/StudentDashboardPage";
import { ExamExplorerPage } from "../pages/Exams/ExamExplorerPage";
import { ExamDetailPage } from "../pages/Exams/ExamDetailPage";
import { SubjectDetailPage } from "../pages/Exams/SubjectDetailPage";
import { TopicDetailPage } from "../pages/Exams/TopicDetailPage";
import { TopicExplorerPage } from "../pages/Exams/TopicExplorerPage";
import { QuizDiscoveryPage } from "../pages/Quizzes/QuizDiscoveryPage";
import { QuizStartPage } from "../pages/Quizzes/QuizStartPage";
import { QuizPlayerPage } from "../pages/Attempt/QuizPlayerPage";
import { ResultPage } from "../pages/Results/ResultPage";
import { ResultsHistoryPage } from "../pages/Results/ResultsHistoryPage";
import { PerformanceAnalyticsPage } from "../pages/Analytics/PerformanceAnalyticsPage";
import { BhagavadGeetaPortalPage } from "../pages/Gita/BhagavadGeetaPortalPage";

// Admin Pages
import { AdminDashboardPage } from "../pages/Admin/AdminDashboardPage";
import { AdminExamsPage } from "../pages/Admin/AdminExamsPage";
import { AdminSubjectsPage } from "../pages/Admin/AdminSubjectsPage";
import { AdminTopicsPage } from "../pages/Admin/AdminTopicsPage";
import { AdminQuestionBankPage } from "../pages/Admin/AdminQuestionBankPage";
import { AdminQuestionDetailPage } from "../pages/Admin/AdminQuestionDetailPage";
import { AdminQuizManagementPage } from "../pages/Admin/AdminQuizManagementPage";
import { AdminIngestionPage } from "../pages/Admin/AdminIngestionPage";
import { AdminContentQualityPage } from "../pages/Admin/AdminContentQualityPage";
import { AdminAnalyticsPage } from "../pages/Admin/AdminAnalyticsPage";
import { AdminUserManagementPage } from "../pages/Admin/AdminUserManagementPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes cache
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export const AppRouter: React.FC = () => {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <ToastProvider>
            <BrowserRouter>
              <Routes>
                {/* Public Routes */}
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />

                {/* Protected Student Routes */}
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <StudentDashboardPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/gita"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <BhagavadGeetaPortalPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/bhagavad-gita"
                  element={<Navigate to="/gita" replace />}
                />
                <Route
                  path="/exams"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <ExamExplorerPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/exams/:examId"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <ExamDetailPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/subjects/:subjectId"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <SubjectDetailPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/topics/:topicId"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <TopicDetailPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/topics/legacy/:subjectId"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <TopicExplorerPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/quizzes"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <QuizDiscoveryPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/quizzes/:quizId"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <QuizStartPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/quiz/:attemptId"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <QuizPlayerPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/results/:resultId"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <ResultPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/results"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <ResultsHistoryPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/analytics"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <PerformanceAnalyticsPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute allowedRoles={["STUDENT", "ADMIN"]}>
                      <ProfilePage />
                    </ProtectedRoute>
                  }
                />

                {/* Protected Admin Governance Routes */}
                <Route
                  path="/admin"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminDashboardPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/exams"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminExamsPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/subjects"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminSubjectsPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/topics"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminTopicsPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/questions"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminQuestionBankPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/questions/:questionId"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminQuestionDetailPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/quizzes"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminQuizManagementPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/ingestion"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminIngestionPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/content-quality"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminContentQualityPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/analytics"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminAnalyticsPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin/users"
                  element={
                    <ProtectedRoute allowedRoles={["ADMIN"]}>
                      <AdminUserManagementPage />
                    </ProtectedRoute>
                  }
                />

                {/* Fallback */}
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </BrowserRouter>
          </ToastProvider>
        </AuthProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
};
