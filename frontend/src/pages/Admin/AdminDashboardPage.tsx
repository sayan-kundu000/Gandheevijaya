import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { AdminAppShell } from "../../components/layout/AdminAppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { StatCard } from "../../components/ui/StatCard";
import { Table, Column } from "../../components/ui/Table";
import { Tabs, TabItem } from "../../components/ui/Tabs";
import { ErrorState } from "../../components/ui/ErrorState";
import { adminApi } from "../../services/adminApi";
import { taxonomyApi } from "../../services/taxonomyApi";
import { quizApi } from "../../services/quizApi";
import { User, Exam, Question, Quiz } from "../../types";
import {
  ShieldAlert,
  Users,
  FileQuestion,
  BookOpen,
  CheckCircle2,
  Database,
  ShieldCheck,
  Plus,
  Layers,
  Tag,
  ArrowRight,
} from "lucide-react";

export const AdminDashboardPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState("users");

  const {
    data: overview,
    isLoading: isOverviewLoading,
    error: overviewError,
    refetch: refetchOverview,
  } = useQuery({
    queryKey: ["admin", "dashboard"],
    queryFn: adminApi.getOverview,
  });

  const {
    data: healthReport,
    isLoading: isHealthLoading,
  } = useQuery({
    queryKey: ["admin", "content-health"],
    queryFn: adminApi.getContentHealthReport,
  });

  const { data: usersData, isLoading: isUsersLoading } = useQuery({
    queryKey: ["admin", "users"],
    queryFn: () => adminApi.getUsers(),
  });

  const { data: questionsData, isLoading: isQuestionsLoading } = useQuery({
    queryKey: ["admin", "questions"],
    queryFn: () => adminApi.getQuestions({ page_size: 10 }),
    enabled: activeTab === "questions",
  });

  const { data: examsData, isLoading: isExamsLoading } = useQuery({
    queryKey: ["admin", "exams"],
    queryFn: () => taxonomyApi.getExams(),
    enabled: activeTab === "taxonomy",
  });

  const { data: quizzesData, isLoading: isQuizzesLoading } = useQuery({
    queryKey: ["admin", "quizzes"],
    queryFn: () => quizApi.getQuizzes(),
    enabled: activeTab === "quizzes",
  });

  if (overviewError) {
    return (
      <AdminAppShell title="Governance Overview">
        <ErrorState message="Administrator privileges required or server connection error." onRetry={refetchOverview} />
      </AdminAppShell>
    );
  }

  const userColumns: Column<User>[] = [
    {
      key: "full_name",
      header: "User Name",
      cell: (row) => <span className="font-semibold text-slate-100">{row.full_name}</span>,
    },
    {
      key: "email",
      header: "Email Address",
      cell: (row) => <span className="text-slate-400">{row.email}</span>,
    },
    {
      key: "role",
      header: "Role",
      cell: (row) => (
        <Badge variant={row.role === "ADMIN" ? "error" : "brand"}>{row.role}</Badge>
      ),
    },
    {
      key: "target_exam",
      header: "Target Stream",
      cell: (row) => <span className="text-slate-300">{row.target_exam || "GATE CS"}</span>,
    },
    {
      key: "status",
      header: "Account Status",
      cell: (row) => (
        <Badge variant={row.is_active ? "success" : "neutral"}>
          {row.is_active ? "Active" : "Disabled"}
        </Badge>
      ),
    },
  ];

  const questionColumns: Column<Question>[] = [
    {
      key: "id",
      header: "ID",
      cell: (row) => <span className="font-mono text-slate-400 text-[11px]">{row.id.substring(0, 8)}...</span>,
    },
    {
      key: "question_text",
      header: "Question Prompt",
      cell: (row) => <span className="text-slate-200 line-clamp-1">{row.question_text}</span>,
    },
    {
      key: "type",
      header: "Type",
      cell: (row) => <Badge variant="neutral">{row.type}</Badge>,
    },
    {
      key: "difficulty",
      header: "Difficulty",
      cell: (row) => (
        <Badge
          variant={
            row.difficulty === "HARD"
              ? "error"
              : row.difficulty === "MEDIUM"
              ? "warning"
              : "success"
          }
        >
          {row.difficulty}
        </Badge>
      ),
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => (
        <Badge variant={row.status === "PUBLISHED" ? "success" : "neutral"}>{row.status}</Badge>
      ),
    },
  ];

  const examColumns: Column<Exam>[] = [
    {
      key: "code",
      header: "Code",
      cell: (row) => <Badge variant="brand">{row.code}</Badge>,
    },
    {
      key: "name",
      header: "Stream Name",
      cell: (row) => <span className="font-bold text-slate-100">{row.name}</span>,
    },
    {
      key: "subjects_count",
      header: "Subjects",
      cell: (row) => <span className="text-slate-300">{row.subjects_count ?? 0}</span>,
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => (
        <Badge variant={row.status === "ACTIVE" ? "success" : "neutral"}>{row.status}</Badge>
      ),
    },
  ];

  const quizColumns: Column<Quiz>[] = [
    {
      key: "title",
      header: "Quiz Title",
      cell: (row) => <span className="font-semibold text-slate-100">{row.title}</span>,
    },
    {
      key: "subject",
      header: "Subject / Topic",
      cell: (row) => <span className="text-slate-400">{row.subject_name || "General"}</span>,
    },
    {
      key: "duration",
      header: "Duration",
      cell: (row) => <span className="text-slate-300 font-mono">{row.duration_minutes} mins</span>,
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => (
        <Badge variant={row.is_published ? "success" : "neutral"}>
          {row.is_published ? "Published" : "Draft"}
        </Badge>
      ),
    },
  ];

  const tabs: TabItem[] = [
    { id: "users", label: "User Directory" },
    { id: "questions", label: "Question Bank" },
    { id: "taxonomy", label: "Exam Streams" },
    { id: "quizzes", label: "Quiz Catalog" },
  ];

  return (
    <AdminAppShell title="Control Dashboard">
      <div className="space-y-6">
        {/* Banner Alert Header */}
        <div className="p-5 rounded-2xl border border-rose-500/30 bg-gradient-to-r from-rose-950/40 via-slate-900 to-slate-900 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <ShieldAlert className="w-8 h-8 text-rose-400 shrink-0" />
            <div>
              <h2 className="text-base font-bold text-rose-200">System Operations & Control Center</h2>
              <p className="text-xs text-slate-300">
                Manage exam taxonomies, monitor ETL ingestion pipelines, enforce content quality, and govern student accounts.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Link to="/admin/content-quality">
              <Button variant="secondary" size="sm" rightIcon={<ShieldCheck className="w-3.5 h-3.5" />}>
                Content Quality ({healthReport?.issue_count || 0})
              </Button>
            </Link>
          </div>
        </div>

        {/* System Stats KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard
            title="Total Platform Users"
            value={overview?.users_count ?? 0}
            icon={<Users className="w-5 h-5 text-brand-400" />}
            isLoading={isOverviewLoading}
          />
          <StatCard
            title="Published Questions"
            value={overview?.published_questions_count ?? 0}
            icon={<FileQuestion className="w-5 h-5 text-emerald-400" />}
            isLoading={isOverviewLoading}
          />
          <StatCard
            title="Active Quizzes"
            value={overview?.published_quizzes_count ?? 0}
            icon={<BookOpen className="w-5 h-5 text-amber-400" />}
            isLoading={isOverviewLoading}
          />
          <StatCard
            title="Completed Attempts"
            value={overview?.completed_attempts_count ?? 0}
            icon={<CheckCircle2 className="w-5 h-5 text-sky-400" />}
            isLoading={isOverviewLoading}
          />
        </div>

        {/* Quick Admin Action Toolbar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3">
          <Link to="/admin/exams">
            <Card className="p-3 flex items-center gap-2.5 hover:border-brand-500/40 transition-colors">
              <Plus className="w-4 h-4 text-brand-400" />
              <span className="text-xs font-bold text-slate-200">Exams</span>
            </Card>
          </Link>
          <Link to="/admin/subjects">
            <Card className="p-3 flex items-center gap-2.5 hover:border-brand-500/40 transition-colors">
              <Layers className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-bold text-slate-200">Subjects</span>
            </Card>
          </Link>
          <Link to="/admin/topics">
            <Card className="p-3 flex items-center gap-2.5 hover:border-brand-500/40 transition-colors">
              <Tag className="w-4 h-4 text-amber-400" />
              <span className="text-xs font-bold text-slate-200">Topics</span>
            </Card>
          </Link>
          <Link to="/admin/questions">
            <Card className="p-3 flex items-center gap-2.5 hover:border-brand-500/40 transition-colors">
              <FileQuestion className="w-4 h-4 text-sky-400" />
              <span className="text-xs font-bold text-slate-200">Question Bank</span>
            </Card>
          </Link>
          <Link to="/admin/quizzes">
            <Card className="p-3 flex items-center gap-2.5 hover:border-brand-500/40 transition-colors">
              <BookOpen className="w-4 h-4 text-rose-400" />
              <span className="text-xs font-bold text-slate-200">Quizzes</span>
            </Card>
          </Link>
          <Link to="/admin/ingestion">
            <Card className="p-3 flex items-center gap-2.5 hover:border-brand-500/40 transition-colors">
              <Database className="w-4 h-4 text-purple-400" />
              <span className="text-xs font-bold text-slate-200">Ingestion</span>
            </Card>
          </Link>
        </div>

        {/* Tabbed Data Directory Preview */}
        <Card className="p-6 space-y-4">
          <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />

          {activeTab === "users" && (
            <Table
              columns={userColumns}
              data={usersData?.items || []}
              keyExtractor={(r) => r.id}
              isLoading={isUsersLoading}
              emptyTitle="No Users Found"
              emptyDescription="No registered user accounts match the current query."
            />
          )}

          {activeTab === "questions" && (
            <Table
              columns={questionColumns}
              data={questionsData?.items || []}
              keyExtractor={(r) => r.id}
              isLoading={isQuestionsLoading}
              emptyTitle="No Questions Found"
              emptyDescription="No question bank records exist yet."
            />
          )}

          {activeTab === "taxonomy" && (
            <Table
              columns={examColumns}
              data={examsData || []}
              keyExtractor={(r) => r.id}
              isLoading={isExamsLoading}
              emptyTitle="No Exam Taxonomy Found"
              emptyDescription="No exam categories registered in database."
            />
          )}

          {activeTab === "quizzes" && (
            <Table
              columns={quizColumns}
              data={quizzesData || []}
              keyExtractor={(r) => r.id}
              isLoading={isQuizzesLoading}
              emptyTitle="No Quizzes Configured"
              emptyDescription="No quizzes found in active catalog."
            />
          )}
        </Card>
      </div>
    </AdminAppShell>
  );
};
