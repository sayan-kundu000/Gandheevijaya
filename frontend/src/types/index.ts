// Common API & Domain Type Definitions matching Gandheevijaya FastAPI Backend

export type Role = "STUDENT" | "ADMIN";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: Role;
  is_active: boolean;
  target_exams?: string[];
  target_exam?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

// Exam, Subject, Topic Taxonomy
export interface Exam {
  id: number;
  code: string;
  name: string;
  description?: string | null;
  status: "ACTIVE" | "INACTIVE";
  subjects_count?: number;
}

export interface Subject {
  id: number;
  exam_id: number;
  code: string;
  name: string;
  description?: string | null;
  status: "ACTIVE" | "INACTIVE";
  exam_name?: string;
  topics_count?: number;
}

export interface Topic {
  id: number;
  subject_id: number;
  code: string;
  name: string;
  description?: string | null;
  status: "ACTIVE" | "INACTIVE";
  subject_name?: string;
  questions_count?: number;
}

// Question Bank
export type QuestionType = "MCQ" | "MSQ" | "NAT";
export type QuestionDifficulty = "EASY" | "MEDIUM" | "HARD";
export type QuestionStatus = "DRAFT" | "PUBLISHED" | "ARCHIVED";

export interface Question {
  id: string;
  topic_id: number;
  difficulty: QuestionDifficulty;
  type: QuestionType;
  question_text: string;
  options?: any; // List or Dict of options
  correct_answer?: string | null; // Sanitized for students on practice APIs, present for admin
  explanation?: string | null;
  status: QuestionStatus;
  topic_name?: string;
  subject_name?: string;
  exam_name?: string;
}

// Quiz
export interface Quiz {
  id: number;
  subject_id: number;
  topic_id?: number | null;
  title: string;
  description?: string | null;
  duration_minutes: number;
  pass_percentage?: float;
  passing_score?: float;
  negative_marking?: float;
  is_published: boolean;
  status: string;
  question_count?: number;
  total_marks?: number;
  subject_name?: string;
  topic_name?: string;
}

// Attempt & Timer
export type AttemptStatus = "IN_PROGRESS" | "SUBMITTED" | "EXPIRED";

export interface AttemptQuestionItem {
  id: string;
  type: QuestionType;
  question_text: string;
  options?: any; // Randomized option order provided by backend
  marks: number;
  negative_marks: number;
}

export interface AttemptAnswerState {
  question_id: string;
  selected_answer: string | null;
  marked_for_review: boolean;
  answered_at?: string;
}

export interface Attempt {
  id: string;
  user_id: string;
  quiz_id: number;
  status: AttemptStatus;
  started_at: string;
  expires_at: string;
  completed_at?: string | null;
  total_questions: number;
  attempted_count: number;
  correct_count: number;
  incorrect_count: number;
  unanswered_count: number;
  total_marks: number;
  score: number;
  percentage: number;
  accuracy: number;
  time_taken_seconds: number;
  passed: boolean;
  question_order?: string[];
}

export interface StartQuizResponse {
  message: string;
  attempt: Attempt;
  questions: AttemptQuestionItem[];
}

export interface AttemptResumeResponse {
  attempt: Attempt;
  questions: AttemptQuestionItem[];
  answers_map?: Record<string, string | null>;
  review_map?: Record<string, boolean>;
}

// Result & Solutions
export interface QuestionSolutionItem {
  question_id: string;
  question_text: string;
  type?: QuestionType;
  options?: any;
  user_answer?: string | null;
  selected_answer?: string | null;
  correct_answer: string;
  is_correct: boolean;
  marks_awarded: number;
  penalty_deducted: number;
  explanation?: string | null;
}

export interface Result {
  id: string;
  attempt_id: string;
  quiz_id: number;
  quiz_title: string;
  subject_name?: string;
  user_id: string;
  total_questions: number;
  attempted_count: number;
  correct_count: number;
  incorrect_count: number;
  unanswered_count: number;
  total_marks: number;
  score: number;
  percentage: number;
  accuracy: number;
  time_taken_seconds: number;
  passed: boolean;
  completed_at: string;
  solutions?: QuestionSolutionItem[];
  detailed_questions?: QuestionSolutionItem[];
}

// Dashboard & Performance Intelligence
export interface DashboardOverview {
  overall_accuracy: number;
  questions_attempted: number;
  quiz_attempts: number;
  total_study_time_seconds: number;
  active_streak_days: number;
  recent_score: number;
}

export interface SubjectProgressItem {
  subject_id: number;
  subject_name: string;
  questions_attempted: number;
  correct_answers: number;
  accuracy: number;
  total_available_questions: number;
}

export interface TopicProgressItem {
  topic_id: number;
  topic_name: string;
  subject_id: number;
  subject_name: string;
  questions_attempted: number;
  correct_answers: number;
  accuracy: number;
}

export interface WeakAreaItem {
  topic_id: number;
  topic_name: string;
  subject_name: string;
  accuracy: number;
  questions_attempted: number;
  priority: "HIGH" | "MEDIUM" | "LOW";
}

export interface PrescriptiveRecommendation {
  priority_rank: number;
  topic_id: number;
  topic_name: string;
  subject_id: number;
  subject_name: string;
  priority_score: number;
  accuracy: number;
  questions_attempted: number;
  coverage_percentage: number;
  recommended_action: string;
  explanation_reason: string;
}

export interface SpeedAccuracyTopicItem {
  topic_id: number;
  topic_name: string;
  subject_id: number;
  subject_name: string;
  accuracy: number;
  questions_attempted: number;
  average_time_per_question_seconds: number;
  quadrant: "FAST_ACCURATE" | "FAST_INACCURATE" | "SLOW_ACCURATE" | "SLOW_INACCURATE";
}

export interface SpeedAccuracyResponse {
  overall_quadrant: string;
  average_speed_seconds_per_question: number;
  overall_accuracy: number;
  topics: SpeedAccuracyTopicItem[];
}

export interface PerformanceDelta {
  window_days: number;
  current_period_attempts: number;
  current_period_questions: number;
  current_period_accuracy: number;
  current_period_avg_score: number;
  prior_period_accuracy: number;
  prior_period_avg_score: number;
  accuracy_delta: number;
  score_delta: number;
  attempts_delta: number;
  velocity_status: "IMPROVING" | "STABLE" | "DECLINING" | "INSUFFICIENT_DATA";
}

export interface StudentIntelligenceProfile {
  user_id: string;
  overall_accuracy: number;
  syllabus_coverage_percentage: number;
  total_questions_attempted: number;
  unique_questions_covered: number;
  total_study_time_seconds: number;
  active_study_days: number;
  current_streak_days: number;
  quadrant_status: string;
  delta_7d: PerformanceDelta;
}

export interface TopicMatrixItem {
  topic_id: number;
  topic_name: string;
  subject_id: number;
  subject_name: string;
  questions_attempted: number;
  correct_answers: number;
  accuracy: number;
  unique_coverage_percentage: number;
  average_time_per_question_seconds: number;
  quadrant: string;
  health_status: "STRONG" | "STABLE" | "WEAK" | "DECLINING" | "IMPROVING" | "NOT_STARTED" | "INSUFFICIENT_DATA";
  priority_score: number;
}

// Admin
export interface AdminDashboardOverview {
  users_count: number;
  students_count: number;
  admins_count: number;
  active_students_count: number;
  disabled_users_count: number;
  exams_count: number;
  subjects_count: number;
  topics_count: number;
  questions_count: number;
  published_questions_count: number;
  quizzes_count: number;
  published_quizzes_count: number;
  attempts_count: number;
  completed_attempts_count: number;
  global_average_score: number;
  global_accuracy: number;
  etl_jobs_count: number;
}

export interface AdminUserItem {
  id: string;
  email: string;
  full_name: string;
  role: Role;
  is_active: boolean;
  target_exam?: string | null;
  created_at: string;

  updated_at?: string;
  total_attempts_count?: number;
  completed_attempts_count?: number;
  average_accuracy?: number;
}

export interface AdminUserDetailResponse {
  user: AdminUserItem;
  recent_attempts: Attempt[];
}

export interface ContentImportJobItem {
  id: number;
  source_path: string;
  file_name?: string;
  status: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED" | "COMPLETED_WITH_WARNINGS";
  total_found: number;
  total_imported: number;
  total_skipped: number;
  total_errors: number;
  started_at: string;
  completed_at?: string | null;
}

export interface ContentImportJobDetailResponse {
  job: ContentImportJobItem;
  error_logs?: { item_id?: string; error_type: string; message: string }[];
}

export interface ContentImportReport {
  job_id: number;
  status: string;
  total_questions_found: number;
  total_questions_imported: number;
  total_questions_skipped: number;
  total_errors: number;
  validation_errors?: any[];
}

export interface ContentHealthIssue {
  type: string;
  severity: "ERROR" | "WARNING";
  entity_id: string;
  details: string;
}

export interface ContentHealthReport {
  generated_at: string;
  total_exams: number;
  total_subjects: number;
  total_topics: number;
  total_questions: number;
  total_materials: number;
  issue_count: number;
  issues: ContentHealthIssue[];
}

export interface SecurityAuditLogItem {
  id: number;
  user_id?: string | null;
  event_type: string;
  ip_address?: string | null;
  user_agent?: string | null;
  details?: any;
  created_at: string;
}

export interface QuestionPoolInfoResponse {
  quiz_id: number;
  exam_id?: number | null;
  subject_id: number;
  topic_id?: number | null;
  requested_count: number;
  available_published_questions: number;
  has_sufficient_pool: boolean;
  details?: Record<string, any>;
}

export interface AdminExamCreateRequest {
  category_id: number;
  name: string;
  code: string;
  description?: string;
  status?: "ACTIVE" | "INACTIVE";
  display_order?: number;
}

export interface AdminSubjectCreateRequest {
  exam_id: number;
  name: string;
  code: string;
  description?: string;
  status?: "ACTIVE" | "INACTIVE";
  display_order?: number;
}

export interface AdminTopicCreateRequest {
  subject_id: number;
  name: string;
  code?: string;
  description?: string;
  status?: "ACTIVE" | "INACTIVE";
  display_order?: number;
}

export interface AdminQuestionCreateRequest {
  id?: string;
  topic_id: number;
  subtopic_id?: number;
  difficulty: QuestionDifficulty;
  type: QuestionType;
  question_text: string;
  options?: any;
  correct_answer: string;
  explanation: string;
  tags?: string[];
  status?: QuestionStatus;
}

export interface AdminQuestionUpdateRequest {
  topic_id?: number;
  subtopic_id?: number;
  difficulty?: QuestionDifficulty;
  type?: QuestionType;
  question_text?: string;
  options?: any;
  correct_answer?: string;
  explanation?: string;
  tags?: string[];
  status?: QuestionStatus;
}

// Helper float alias
type float = number;
