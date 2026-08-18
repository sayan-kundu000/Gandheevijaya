import React from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "../../components/layout/AppShell";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Skeleton } from "../../components/ui/Skeleton";
import { EmptyState } from "../../components/ui/EmptyState";
import { ErrorState } from "../../components/ui/ErrorState";
import { resultsApi } from "../../services/resultsApi";
import { Award, Calendar, Clock, ArrowRight, BookOpen, CheckCircle2, Play } from "lucide-react";

export const ResultsHistoryPage: React.FC = () => {
  const {
    data: history,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["results", "history"],
    queryFn: resultsApi.getUserHistory,
  });

  if (error) {
    return (
      <AppShell title="Quiz Attempt History">
        <ErrorState onRetry={refetch} />
      </AppShell>
    );
  }

  return (
    <AppShell title="Quiz Attempt History">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">Your Quiz Performance History</h2>
            <p className="text-xs text-slate-400">
              Review your past test scores, detailed answer evaluations, and solution explanations.
            </p>
          </div>
          <Link to="/quizzes">
            <Button variant="primary" size="sm" rightIcon={<Play className="w-3.5 h-3.5" />}>
              Take a New Quiz
            </Button>
          </Link>
        </div>

        {/* History Table or List */}
        {isLoading ? (
          <div className="space-y-3">
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-20 w-full" />
          </div>
        ) : history && history.length > 0 ? (
          <div className="space-y-3">
            {history.map((res) => (
              <Card
                key={res.id || res.attempt_id}
                className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-slate-700 transition-colors"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2">
                    <Badge variant={res.passed ? "success" : "error"}>
                      {res.passed ? "Passed" : "Needs Practice"}
                    </Badge>
                    <Badge variant="brand">{res.subject_name || "General"}</Badge>
                    <span className="text-xs text-slate-500 flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {new Date(res.completed_at).toLocaleDateString()}
                    </span>
                  </div>
                  <h3 className="text-base font-bold text-slate-100">{res.quiz_title}</h3>
                </div>

                <div className="flex items-center gap-6 border-t md:border-t-0 md:border-l border-slate-800 pt-3 md:pt-0 md:pl-6">
                  <div>
                    <p className="text-[11px] text-slate-400">Score</p>
                    <p className="text-base font-bold text-brand-400">
                      {res.score} / {res.total_marks}
                    </p>
                  </div>

                  <div>
                    <p className="text-[11px] text-slate-400">Accuracy</p>
                    <p className="text-base font-bold text-emerald-400">{res.accuracy}%</p>
                  </div>

                  <div>
                    <p className="text-[11px] text-slate-400">Time</p>
                    <p className="text-sm font-semibold text-slate-200">
                      {Math.round(res.time_taken_seconds / 60)}m
                    </p>
                  </div>

                  <Link to={`/results/${res.id || res.attempt_id}`}>
                    <Button
                      variant="secondary"
                      size="sm"
                      rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
                    >
                      Review
                    </Button>
                  </Link>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <EmptyState
            icon={<Award className="w-12 h-12 text-slate-500" />}
            title="No Completed Quizzes Yet"
            description="Your completed quiz results, scores, accuracy analytics, and detailed solution reviews will appear here after your first quiz attempt."
            actionText="Explore Quizzes"
            onAction={() => (window.location.href = "/quizzes")}
          />
        )}
      </div>
    </AppShell>
  );
};
