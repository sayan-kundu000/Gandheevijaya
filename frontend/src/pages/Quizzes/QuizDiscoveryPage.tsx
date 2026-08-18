import React, { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { useSearchParams, useNavigate } from "react-router-dom";
import { AppShell } from "../../components/layout/AppShell";
import { Card } from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";
import { Badge } from "../../components/ui/Badge";
import { Select } from "../../components/ui/Select";
import { Input } from "../../components/ui/Input";
import { Skeleton } from "../../components/ui/Skeleton";
import { EmptyState } from "../../components/ui/EmptyState";
import { ErrorState } from "../../components/ui/ErrorState";
import { quizApi } from "../../services/quizApi";
import { taxonomyApi } from "../../services/taxonomyApi";
import { useAuth } from "../../context/AuthContext";
import {
  Clock,
  HelpCircle,
  Award,
  Play,
  Filter,
  GraduationCap,
  Search,
  BookOpen,
  Sparkles,
  Layers,
} from "lucide-react";

export const QuizDiscoveryPage: React.FC = () => {
  const { user } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const examIdParam = searchParams.get("exam_id");
  const subjectIdParam = searchParams.get("subject_id");
  const topicIdParam = searchParams.get("topic_id");

  const [searchQuery, setSearchQuery] = useState("");

  const { data: exams } = useQuery({
    queryKey: ["exams"],
    queryFn: taxonomyApi.getExams,
  });

  const [selectedExamId, setSelectedExamId] = useState<number | undefined>(
    examIdParam ? parseInt(examIdParam, 10) : undefined
  );

  const [selectedSubjectId, setSelectedSubjectId] = useState<number | undefined>(
    subjectIdParam ? parseInt(subjectIdParam, 10) : undefined
  );

  const { data: subjects } = useQuery({
    queryKey: ["subjects", selectedExamId],
    queryFn: () => taxonomyApi.getSubjects(selectedExamId),
  });

  const {
    data: quizzes,
    isLoading: isQuizzesLoading,
    error: quizzesError,
    refetch,
  } = useQuery({
    queryKey: ["quizzes", selectedExamId, selectedSubjectId, topicIdParam],
    queryFn: () =>
      quizApi.getQuizzes({
        exam_id: selectedExamId,
        subject_id: selectedSubjectId,
        topic_id: topicIdParam ? parseInt(topicIdParam, 10) : undefined,
      }),
  });

  // Client-side text search filter
  const filteredQuizzes = useMemo(() => {
    if (!quizzes) return [];
    let list = quizzes;
    if (searchQuery.trim()) {
      const qLower = searchQuery.toLowerCase();
      list = list.filter(
        (q) =>
          q.title.toLowerCase().includes(qLower) ||
          (q.subject_name && q.subject_name.toLowerCase().includes(qLower)) ||
          (q.description && q.description.toLowerCase().includes(qLower))
      );
    }
    return list;
  }, [quizzes, searchQuery]);

  if (quizzesError) {
    return (
      <AppShell title="Quiz Catalog">
        <ErrorState onRetry={refetch} />
      </AppShell>
    );
  }

  return (
    <AppShell title="Quiz Catalog & Assessment Discovery">
      <div className="space-y-6">
        {/* Banner Section */}
        <div className="relative overflow-hidden rounded-2xl border border-brand-500/20 bg-gradient-to-r from-brand-950/40 via-slate-900 to-indigo-950/30 p-6 md:p-8">
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2 max-w-2xl">
              <div className="flex items-center gap-2 text-brand-400 font-semibold text-xs uppercase tracking-wider">
                <Sparkles className="w-4 h-4" />
                Live Examination Simulator & Practice Bank
              </div>
              <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight">
                Practice Quizzes & Assessments
              </h1>
              <p className="text-sm text-slate-300">
                Explore 3-hour GATE CS full subject simulations (20 MCQs, 20 MSQs & 20 NATs) and 30-minute speed drills for Banking & SSC exams.
              </p>
            </div>

            <div className="flex items-center gap-3 bg-slate-900/80 border border-slate-800 rounded-xl p-4">
              <div className="p-3 bg-brand-500/10 rounded-lg text-brand-400">
                <BookOpen className="w-6 h-6" />
              </div>
              <div>
                <div className="text-2xl font-black text-slate-100">
                  {quizzes?.length || 440}+
                </div>
                <div className="text-xs text-slate-400 font-medium">Active Assessments</div>
              </div>
            </div>
          </div>
        </div>

        {/* Controls and Filters */}
        <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4 p-5 rounded-2xl border border-slate-800 bg-slate-900/70 shadow-sm">
          {/* Search bar */}
          <div className="relative flex-1 min-w-[240px]">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search quizzes by title or subject..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-colors"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full lg:w-auto">
            {/* Exam Category Filter */}
            <div className="w-full sm:w-56">
              <Select
                options={[
                  { value: "", label: "All Exam Streams" },
                  ...(exams?.map((e) => ({
                    value: e.id,
                    label: e.name,
                  })) || []),
                ]}
                value={selectedExamId || ""}
                onChange={(e) => {
                  const val = e.target.value ? parseInt(e.target.value, 10) : undefined;
                  setSelectedExamId(val);
                  setSelectedSubjectId(undefined);
                  const newParams: Record<string, string> = {};
                  if (val) newParams.exam_id = val.toString();
                  setSearchParams(newParams);
                }}
              />
            </div>

            {/* Subject Filter */}
            <div className="w-full sm:w-60">
              <Select
                options={[
                  { value: "", label: "All Subjects" },
                  ...(subjects?.map((s) => ({ value: s.id, label: `${s.name} (${s.code})` })) || []),
                ]}
                value={selectedSubjectId || ""}
                onChange={(e) => {
                  const val = e.target.value ? parseInt(e.target.value, 10) : undefined;
                  setSelectedSubjectId(val);
                  const newParams: Record<string, string> = {};
                  if (selectedExamId) newParams.exam_id = selectedExamId.toString();
                  if (val) newParams.subject_id = val.toString();
                  setSearchParams(newParams);
                }}
              />
            </div>
          </div>
        </div>

        {/* Quizzes Grid */}
        {isQuizzesLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Skeleton className="h-52 w-full" />
            <Skeleton className="h-52 w-full" />
            <Skeleton className="h-52 w-full" />
            <Skeleton className="h-52 w-full" />
            <Skeleton className="h-52 w-full" />
            <Skeleton className="h-52 w-full" />
          </div>
        ) : filteredQuizzes && filteredQuizzes.length > 0 ? (
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Showing {filteredQuizzes.length} Available Quizzes
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredQuizzes.map((quiz) => (
                <Card
                  key={quiz.id}
                  className="p-5 flex flex-col justify-between hover:border-slate-700 transition-all bg-slate-900/60 group hover:shadow-lg hover:shadow-brand-950/20"
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between gap-2">
                      <Badge variant="brand" className="truncate max-w-[180px]">
                        {quiz.subject_name || (quiz as any).subject?.name || "Core Subject"}
                      </Badge>
                      <Badge variant="neutral" className="flex items-center gap-1 shrink-0">
                        <Clock className="w-3 h-3 text-slate-400" />
                        {quiz.duration_minutes} Mins
                      </Badge>
                    </div>

                    <h3 className="text-base font-bold text-slate-100 group-hover:text-brand-300 transition-colors line-clamp-2">
                      {quiz.title}
                    </h3>
                    <p className="text-xs text-slate-400 line-clamp-2">
                      {quiz.description || "Timed practice assessment based on standard examination question patterns."}
                    </p>
                  </div>

                  <div className="mt-5 pt-3 border-t border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-3 text-xs text-slate-400">
                      <span className="flex items-center gap-1">
                        <HelpCircle className="w-3.5 h-3.5 text-brand-400" />
                        {quiz.question_count || 60} Qs
                      </span>
                      <span className="flex items-center gap-1">
                        <Award className="w-3.5 h-3.5 text-amber-400" />
                        {quiz.total_marks || 100} Pts
                      </span>
                    </div>

                    <Button
                      variant="primary"
                      size="sm"
                      rightIcon={<Play className="w-3.5 h-3.5" />}
                      onClick={() => navigate(`/quizzes/${quiz.id}`)}
                    >
                      Start Quiz
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        ) : (
          <EmptyState
            icon={<HelpCircle className="w-12 h-12 text-slate-600" />}
            title="No Quizzes Found"
            description="There are currently no active quizzes matching the selected exam stream, subject, or search filters."
            actionText="Clear Filters"
            onAction={() => {
              setSelectedExamId(undefined);
              setSelectedSubjectId(undefined);
              setSearchQuery("");
              setSearchParams({});
            }}
          />
        )}
      </div>
    </AppShell>
  );
};
