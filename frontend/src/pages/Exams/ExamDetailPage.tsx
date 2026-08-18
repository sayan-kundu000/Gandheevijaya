import React from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "../../components/layout/AppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Skeleton } from "../../components/ui/Skeleton";
import { ErrorState } from "../../components/ui/ErrorState";
import { taxonomyApi } from "../../services/taxonomyApi";
import { quizApi } from "../../services/quizApi";
import { QuizCard } from "../../features/quizzes/components/QuizCard";
import { BookOpen, Layers, ArrowLeft, ArrowRight, Sparkles } from "lucide-react";

export const ExamDetailPage: React.FC = () => {
  const { examId } = useParams<{ examId: string }>();
  const idNum = Number(examId);

  const {
    data: exams,
    isLoading: isExamsLoading,
    error: examsError,
    refetch: refetchExams,
  } = useQuery({
    queryKey: ["exams"],
    queryFn: taxonomyApi.getExams,
  });

  const {
    data: subjects,
    isLoading: isSubjectsLoading,
  } = useQuery({
    queryKey: ["subjects", idNum],
    queryFn: () => taxonomyApi.getSubjects(idNum),
    enabled: !!idNum,
  });

  const {
    data: quizzes,
    isLoading: isQuizzesLoading,
  } = useQuery({
    queryKey: ["quizzes", "exam", idNum],
    queryFn: () => quizApi.getQuizzes(),
    enabled: !!idNum,
  });

  const currentExam = exams?.find((e) => e.id === idNum);

  if (examsError) {
    return (
      <AppShell title="Exam Detail">
        <ErrorState onRetry={refetchExams} />
      </AppShell>
    );
  }

  return (
    <AppShell title={currentExam ? currentExam.name : "Exam Details"}>
      <div className="space-y-6">
        {/* Back Link */}
        <Link
          to="/exams"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to All Exams
        </Link>

        {/* Hero Banner */}
        <Card className="p-6 bg-gradient-to-r from-brand-950/60 via-slate-900 to-slate-900 border border-brand-500/20 relative overflow-hidden">
          <div className="absolute right-0 top-0 translate-x-12 -translate-y-6 w-64 h-64 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />
          {isExamsLoading ? (
            <div className="space-y-3">
              <Skeleton className="h-8 w-48" />
              <Skeleton className="h-4 w-96" />
            </div>
          ) : (
            <div className="relative z-10 space-y-3">
              <div className="flex items-center gap-2">
                <Badge variant="brand">{currentExam?.code || "EXAM"}</Badge>
                <Badge variant="success">Active Syllabus</Badge>
              </div>
              <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight">
                {currentExam?.name}
              </h1>
              <p className="text-sm text-slate-300 max-w-2xl">
                {currentExam?.description ||
                  "Structured exam preparation syllabus featuring comprehensive subject modules, topic drills, and timed practice tests."}
              </p>
            </div>
          )}
        </Card>

        {/* Subjects Module Grid */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Layers className="w-5 h-5 text-brand-400" />
              Subjects & Curriculum
            </h3>
            <span className="text-xs text-slate-400">
              {subjects?.length || 0} Available Subjects
            </span>
          </div>

          {isSubjectsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Skeleton className="h-32" />
              <Skeleton className="h-32" />
            </div>
          ) : subjects && subjects.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {subjects.map((sub) => (
                <Card
                  key={sub.id}
                  className="p-5 flex flex-col justify-between hover:border-brand-500/50 transition-all group"
                >
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Badge variant="neutral">{sub.code}</Badge>
                      <span className="text-xs text-slate-500">{sub.topics_count || 0} Topics</span>
                    </div>
                    <h4 className="text-base font-bold text-slate-100 group-hover:text-brand-300 transition-colors">
                      {sub.name}
                    </h4>
                    <p className="text-xs text-slate-400 line-clamp-2">
                      {sub.description || "Master core concepts and problem solving."}
                    </p>
                  </div>

                  <div className="pt-4 mt-4 border-t border-slate-800 flex items-center justify-between">
                    <Link to={`/subjects/${sub.id}`}>
                      <Button
                        variant="secondary"
                        size="sm"
                        rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
                      >
                        Explore Topics
                      </Button>
                    </Link>
                  </div>
                </Card>
              ))}
            </div>
          ) : (
            <Card className="p-8 text-center space-y-2">
              <p className="text-sm font-semibold text-slate-300">No subjects available yet.</p>
              <p className="text-xs text-slate-500">Check back soon as new topics are ingested.</p>
            </Card>
          )}
        </div>

        {/* Quizzes Available */}
        <div className="space-y-4 pt-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-emerald-400" />
              Exam Quizzes & Practice Tests
            </h3>
            <Link to="/quizzes" className="text-xs font-semibold text-brand-400 hover:underline">
              View All Quizzes
            </Link>
          </div>

          {isQuizzesLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Skeleton className="h-44" />
              <Skeleton className="h-44" />
              <Skeleton className="h-44" />
            </div>
          ) : quizzes && quizzes.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {quizzes.slice(0, 6).map((quiz) => (
                <QuizCard key={quiz.id} quiz={quiz} />
              ))}
            </div>
          ) : (
            <Card className="p-6 text-center text-xs text-slate-500">
              No quizzes published specifically for this exam yet.
            </Card>
          )}
        </div>
      </div>
    </AppShell>
  );
};
