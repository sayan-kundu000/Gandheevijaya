import React from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "../../components/layout/AppShell";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Skeleton } from "../../components/ui/Skeleton";
import { ErrorState } from "../../components/ui/ErrorState";
import { taxonomyApi } from "../../services/taxonomyApi";
import { quizApi } from "../../services/quizApi";
import { dashboardApi } from "../../services/dashboardApi";
import { QuizCard } from "../../features/quizzes/components/QuizCard";
import { BookOpen, Layers, ArrowLeft, ArrowRight, Target, CheckCircle2 } from "lucide-react";

export const SubjectDetailPage: React.FC = () => {
  const { subjectId } = useParams<{ subjectId: string }>();
  const idNum = Number(subjectId);

  const {
    data: topics,
    isLoading: isTopicsLoading,
    error: topicsError,
    refetch: refetchTopics,
  } = useQuery({
    queryKey: ["topics", idNum],
    queryFn: () => taxonomyApi.getTopics(idNum),
    enabled: !!idNum,
  });

  const {
    data: quizzes,
    isLoading: isQuizzesLoading,
  } = useQuery({
    queryKey: ["quizzes", "subject", idNum],
    queryFn: () => quizApi.getQuizzes({ subject_id: idNum }),
    enabled: !!idNum,
  });

  const {
    data: subjectProgressData,
  } = useQuery({
    queryKey: ["dashboard", "subject-progress"],
    queryFn: dashboardApi.getSubjectProgress,
  });

  const currentProgress = subjectProgressData?.items?.find((s) => s.subject_id === idNum);
  const subjectName = topics?.[0]?.subject_name || currentProgress?.subject_name || "Subject Details";

  if (topicsError) {
    return (
      <AppShell title="Subject Details">
        <ErrorState onRetry={refetchTopics} />
      </AppShell>
    );
  }

  return (
    <AppShell title={subjectName}>
      <div className="space-y-6">
        {/* Back Link */}
        <Link
          to="/exams"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Curriculum
        </Link>

        {/* Hero Card */}
        <Card className="p-6 bg-gradient-to-r from-slate-900 via-slate-900 to-brand-950/40 border border-slate-800">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-2">
              <Badge variant="brand">Subject Module</Badge>
              <h1 className="text-2xl font-bold text-white">{subjectName}</h1>
              <p className="text-sm text-slate-300">
                Master individual topic concepts, analyze practice performance, and take targeted topic tests.
              </p>
            </div>

            {currentProgress && (
              <div className="flex items-center gap-4 bg-slate-800/80 p-4 rounded-xl border border-slate-700">
                <div>
                  <p className="text-xs text-slate-400">Questions Solved</p>
                  <p className="text-lg font-bold text-slate-100">{currentProgress.questions_attempted}</p>
                </div>
                <div className="border-l border-slate-700 pl-4">
                  <p className="text-xs text-slate-400">Accuracy</p>
                  <p className="text-lg font-bold text-emerald-400">{currentProgress.accuracy}%</p>
                </div>
              </div>
            )}
          </div>
        </Card>

        {/* Topics List */}
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Layers className="w-5 h-5 text-brand-400" />
            Subject Topics
          </h3>

          {isTopicsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Skeleton className="h-28" />
              <Skeleton className="h-28" />
            </div>
          ) : topics && topics.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {topics.map((t) => (
                <Card
                  key={t.id}
                  className="p-5 flex flex-col justify-between hover:border-slate-700 transition-colors"
                >
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Badge variant="neutral">{t.code || `TOPIC-${t.id}`}</Badge>
                      <span className="text-xs text-slate-400">{t.questions_count || 0} Questions</span>
                    </div>
                    <h4 className="text-base font-bold text-slate-100">{t.name}</h4>
                    <p className="text-xs text-slate-400 line-clamp-2">
                      {t.description || "Targeted practice questions and concept evaluations."}
                    </p>
                  </div>

                  <div className="pt-4 mt-4 border-t border-slate-800 flex items-center justify-between">
                    <Link to={`/topics/${t.id}`}>
                      <Button variant="outline" size="sm">
                        View Topic
                      </Button>
                    </Link>
                    <Link to={`/quizzes?topic_id=${t.id}`}>
                      <Button variant="primary" size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
                        Practice
                      </Button>
                    </Link>
                  </div>
                </Card>
              ))}
            </div>
          ) : (
            <Card className="p-6 text-center text-xs text-slate-500">
              No topics published for this subject yet.
            </Card>
          )}
        </div>

        {/* Quizzes List */}
        <div className="space-y-4 pt-4">
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-400" />
            Subject Practice Quizzes
          </h3>

          {isQuizzesLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Skeleton className="h-44" />
              <Skeleton className="h-44" />
            </div>
          ) : quizzes && quizzes.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {quizzes.map((quiz) => (
                <QuizCard key={quiz.id} quiz={quiz} />
              ))}
            </div>
          ) : (
            <Card className="p-6 text-center text-xs text-slate-500">
              No active quizzes for this subject currently.
            </Card>
          )}
        </div>
      </div>
    </AppShell>
  );
};
