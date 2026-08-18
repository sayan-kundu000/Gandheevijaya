import React from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "../../components/layout/AppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Skeleton } from "../../components/ui/Skeleton";
import { ErrorState } from "../../components/ui/ErrorState";
import { resultsApi } from "../../services/resultsApi";
import { SolutionSlideViewer } from "../../features/attempts/components/SolutionSlideViewer";
import {
  Award,
  CheckCircle2,
  XCircle,
  Clock,
  Target,
  ArrowRight,
  BookOpen,
  RotateCcw,
  Sparkles,
} from "lucide-react";

export const ResultPage: React.FC = () => {
  const { resultId } = useParams<{ resultId: string }>();

  const {
    data: result,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["result", resultId],
    queryFn: () => resultsApi.getResult(resultId || ""),
    enabled: !!resultId,
  });

  if (error) {
    return (
      <AppShell title="Quiz Result">
        <ErrorState onRetry={refetch} />
      </AppShell>
    );
  }

  if (isLoading || !result) {
    return (
      <AppShell title="Quiz Result">
        <Skeleton className="h-96 w-full" />
      </AppShell>
    );
  }

  return (
    <AppShell title="Quiz Performance & Solution Review">
      <div className="space-y-6">
        {/* Top Result Banner */}
        <Card className="p-6 bg-gradient-to-r from-brand-950/60 via-slate-900 to-slate-900 border border-brand-500/20 shadow-xl">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Badge variant={result.passed ? "success" : "error"}>
                  {result.passed ? "Passed Threshold" : "Needs Focused Practice"}
                </Badge>
                <Badge variant="brand">{result.subject_name || "General Subject"}</Badge>
              </div>
              <h1 className="text-2xl md:text-3xl font-bold text-white tracking-tight">
                {result.quiz_title}
              </h1>
              <p className="text-xs text-slate-400">
                Attempt completed on {new Date(result.completed_at || Date.now()).toLocaleDateString()}
              </p>
            </div>

            {/* Score & Accuracy Hero */}
            <div className="flex items-center gap-6 border-l border-slate-800 pl-6">
              <div className="text-center">
                <p className="text-xs text-slate-400">Official Score</p>
                <p className="text-2xl md:text-3xl font-extrabold text-brand-400">
                  {result.score} <span className="text-sm font-normal text-slate-400">/ {result.total_marks}</span>
                </p>
              </div>

              <div className="text-center border-l border-slate-800 pl-6">
                <p className="text-xs text-slate-400 font-medium">Accuracy</p>
                <p className="text-2xl md:text-3xl font-extrabold text-emerald-400">
                  {result.accuracy}%
                </p>
              </div>
            </div>
          </div>
        </Card>

        {/* Breakdown Metric Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-400">Correct Solves</p>
              <p className="text-lg font-bold text-slate-100">{result.correct_count}</p>
            </div>
          </Card>

          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
              <XCircle className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-400">Incorrect</p>
              <p className="text-lg font-bold text-slate-100">{result.incorrect_count}</p>
            </div>
          </Card>

          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 rounded-xl bg-slate-800 text-slate-400 border border-slate-700">
              <Target className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-400">Unanswered</p>
              <p className="text-lg font-bold text-slate-100">{result.unanswered_count}</p>
            </div>
          </Card>

          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <Clock className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-400">Time Taken</p>
              <p className="text-lg font-bold text-slate-100">
                {Math.round((result.time_taken_seconds || 0) / 60)} Mins
              </p>
            </div>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-brand-400" />
            <span className="text-xs font-semibold text-slate-300">
              Ready to reinforce weak concepts?
            </span>
          </div>

          <div className="flex items-center gap-3">
            <Link to="/quizzes">
              <Button variant="outline" size="sm" leftIcon={<RotateCcw className="w-3.5 h-3.5" />}>
                Try Another Quiz
              </Button>
            </Link>
            <Link to="/analytics">
              <Button variant="primary" size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
                View Weakness Analytics
              </Button>
            </Link>
          </div>
        </div>

        {/* Interactive Question Solutions Slide Viewer */}
        <SolutionSlideViewer solutions={result.detailed_questions || result.solutions || []} />
      </div>
    </AppShell>
  );
};
