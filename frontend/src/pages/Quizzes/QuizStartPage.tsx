import React from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useQuery, useMutation } from "@tanstack/react-query";
import { AppShell } from "../../components/layout/AppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Skeleton } from "../../components/ui/Skeleton";
import { ErrorState } from "../../components/ui/ErrorState";
import { quizApi } from "../../services/quizApi";
import { BookOpen, Clock, AlertCircle, ArrowLeft, Play, ShieldAlert, Award } from "lucide-react";

export const QuizStartPage: React.FC = () => {
  const { quizId } = useParams<{ quizId: string }>();
  const navigate = useNavigate();
  const idNum = Number(quizId);

  const {
    data: quiz,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["quiz", idNum],
    queryFn: () => quizApi.getQuizDetails(idNum),
    enabled: !!idNum,
  });

  const startMutation = useMutation({
    mutationFn: () => quizApi.startQuiz(idNum),
    onSuccess: (data) => {
      navigate(`/quiz/${data.attempt.id}`, { state: { quizData: data } });
    },
  });

  if (error) {
    return (
      <AppShell title="Quiz Instructions">
        <ErrorState onRetry={refetch} />
      </AppShell>
    );
  }

  if (isLoading || !quiz) {
    return (
      <AppShell title="Quiz Instructions">
        <Skeleton className="h-96 w-full" />
      </AppShell>
    );
  }

  return (
    <AppShell title="Quiz Instructions & Rules">
      <div className="max-w-3xl mx-auto space-y-6">
        {/* Back Link */}
        <Link
          to="/quizzes"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Quizzes
        </Link>

        {/* Hero Card */}
        <Card className="p-6 bg-gradient-to-r from-brand-950/50 via-slate-900 to-slate-900 border border-brand-500/30">
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <Badge variant="brand">{quiz.subject_name || "Subject Test"}</Badge>
              {quiz.topic_name && <Badge variant="neutral">{quiz.topic_name}</Badge>}
              <Badge variant="info">Passing: {quiz.pass_percentage || quiz.passing_score || 50}%</Badge>
            </div>

            <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight">
              {quiz.title}
            </h1>

            <p className="text-sm text-slate-300">
              {quiz.description ||
                "Test your topic conceptual understanding under strict exam-style conditions."}
            </p>
          </div>
        </Card>

        {/* Quiz Specifications Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="p-4 text-center space-y-1">
            <BookOpen className="w-5 h-5 text-brand-400 mx-auto" />
            <p className="text-xs text-slate-400">Total Questions</p>
            <p className="text-lg font-bold text-slate-100">{quiz.question_count || 10}</p>
          </Card>

          <Card className="p-4 text-center space-y-1">
            <Clock className="w-5 h-5 text-amber-400 mx-auto" />
            <p className="text-xs text-slate-400">Duration</p>
            <p className="text-lg font-bold text-slate-100">{quiz.duration_minutes} Mins</p>
          </Card>

          <Card className="p-4 text-center space-y-1">
            <Award className="w-5 h-5 text-emerald-400 mx-auto" />
            <p className="text-xs text-slate-400">Total Marks</p>
            <p className="text-lg font-bold text-slate-100">{quiz.total_marks || 10}</p>
          </Card>

          <Card className="p-4 text-center space-y-1">
            <ShieldAlert className="w-5 h-5 text-rose-400 mx-auto" />
            <p className="text-xs text-slate-400">Negative Marking</p>
            <p className="text-lg font-bold text-slate-100">
              {quiz.negative_marking ? `-${quiz.negative_marking}` : "0.25"} Per Incorrect
            </p>
          </Card>
        </div>

        {/* Instructions Rules List */}
        <Card className="p-6 space-y-4">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <AlertCircle className="w-4 h-4 text-amber-400" />
              Important Attempt Guidelines
            </CardTitle>
          </CardHeader>

          <ul className="space-y-3 text-xs md:text-sm text-slate-300 list-disc list-inside leading-relaxed">
            <li>Ensure a stable internet connection. Answers are automatically saved on selection.</li>
            <li>The countdown timer starts immediately once you click "START QUIZ".</li>
            <li>Use the Question Palette to jump between questions or mark questions for review.</li>
            <li>Keyboard shortcuts: 1-4 for option selection, N for next question, P for previous, M for mark for review.</li>
            <li>The quiz will automatically submit when the timer expires.</li>
          </ul>

          <div className="pt-4 border-t border-slate-800 flex items-center justify-end gap-4">
            <Link to="/quizzes">
              <Button variant="ghost">Cancel</Button>
            </Link>
            <Button
              variant="primary"
              size="lg"
              isLoading={startMutation.isPending}
              rightIcon={<Play className="w-4 h-4" />}
              onClick={() => startMutation.mutate()}
            >
              START QUIZ NOW
            </Button>
          </div>
        </Card>
      </div>
    </AppShell>
  );
};
