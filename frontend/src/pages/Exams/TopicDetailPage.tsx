import React from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "../../components/layout/AppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Skeleton } from "../../components/ui/Skeleton";
import { ErrorState } from "../../components/ui/ErrorState";
import { quizApi } from "../../services/quizApi";
import { dashboardApi } from "../../services/dashboardApi";
import { QuizCard } from "../../features/quizzes/components/QuizCard";
import { BookOpen, Target, ArrowLeft, Play, AlertCircle, Sparkles } from "lucide-react";

export const TopicDetailPage: React.FC = () => {
  const { topicId } = useParams<{ topicId: string }>();
  const idNum = Number(topicId);

  const {
    data: topicProgressData,
    isLoading: isProgressLoading,
    error: progressError,
    refetch,
  } = useQuery({
    queryKey: ["dashboard", "topic-progress"],
    queryFn: dashboardApi.getTopicProgress,
  });

  const {
    data: quizzes,
    isLoading: isQuizzesLoading,
  } = useQuery({
    queryKey: ["quizzes", "topic", idNum],
    queryFn: () => quizApi.getQuizzes({ topic_id: idNum }),
    enabled: !!idNum,
  });

  const topicProgress = topicProgressData?.items?.find((t) => t.topic_id === idNum);
  const topicName = topicProgress?.topic_name || `Topic #${idNum}`;

  if (progressError) {
    return (
      <AppShell title="Topic Details">
        <ErrorState onRetry={refetch} />
      </AppShell>
    );
  }

  return (
    <AppShell title={topicName}>
      <div className="space-y-6">
        {/* Back Link */}
        <Link
          to="/exams"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Curriculum
        </Link>

        {/* Hero Card */}
        <Card className="p-6 bg-gradient-to-r from-brand-950/40 via-slate-900 to-slate-900 border border-brand-500/20">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Badge variant="brand">{topicProgress?.subject_name || "Topic Practice"}</Badge>
                {topicProgress && topicProgress.accuracy < 60 && (
                  <Badge variant="warning" className="flex items-center gap-1">
                    <AlertCircle className="w-3 h-3" /> Focus Area
                  </Badge>
                )}
              </div>
              <h1 className="text-2xl font-bold text-white">{topicName}</h1>
              <p className="text-sm text-slate-300">
                Targeted topic practice questions to build concept mastery and eliminate calculation mistakes.
              </p>
            </div>

            <div className="flex items-center gap-4">
              <Link to={`/quizzes?topic_id=${idNum}`}>
                <Button variant="primary" size="md" rightIcon={<Play className="w-4 h-4" />}>
                  Start Practice Quiz
                </Button>
              </Link>
            </div>
          </div>
        </Card>

        {/* Performance Metrics */}
        {topicProgress && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="p-4 flex items-center gap-3">
              <div className="p-3 rounded-xl bg-brand-500/10 text-brand-400 border border-brand-500/20">
                <BookOpen className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400">Questions Solved</p>
                <p className="text-lg font-bold text-slate-100">{topicProgress.questions_attempted}</p>
              </div>
            </Card>

            <Card className="p-4 flex items-center gap-3">
              <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <Target className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400">Correct Solves</p>
                <p className="text-lg font-bold text-slate-100">{topicProgress.correct_answers}</p>
              </div>
            </Card>

            <Card className="p-4 flex items-center gap-3">
              <div className="p-3 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400">Topic Accuracy</p>
                <p className="text-lg font-bold text-emerald-400">{topicProgress.accuracy}%</p>
              </div>
            </Card>
          </div>
        )}

        {/* Quizzes for this Topic */}
        <div className="space-y-4 pt-4">
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-400" />
            Available Quizzes
          </h3>

          {isQuizzesLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
              No specific quizzes found for this topic. Use the button above to launch dynamic topic practice!
            </Card>
          )}
        </div>
      </div>
    </AppShell>
  );
};
