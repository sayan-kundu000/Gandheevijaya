import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { AppShell } from "../../components/layout/AppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";
import { Badge } from "../../components/ui/Badge";
import { Skeleton } from "../../components/ui/Skeleton";
import { EmptyState } from "../../components/ui/EmptyState";
import { ErrorState } from "../../components/ui/ErrorState";
import { dashboardApi } from "../../services/dashboardApi";
import { intelligenceApi } from "../../services/intelligenceApi";
import { attemptApi } from "../../services/attemptApi";
import { useAuth } from "../../context/AuthContext";
import {
  Target,
  Flame,
  Clock,
  BookOpen,
  ArrowRight,
  Sparkles,
  AlertCircle,
  Play,
  RotateCcw,
  Award,
  BarChart3,
  CheckCircle2,
} from "lucide-react";

export const StudentDashboardPage: React.FC = () => {
  const { user } = useAuth();

  const {
    data: overview,
    isLoading: isOverviewLoading,
    error: overviewError,
    refetch: refetchOverview,
  } = useQuery({
    queryKey: ["dashboard", "overview"],
    queryFn: dashboardApi.getOverview,
  });

  const {
    data: recommendations,
    isLoading: isRecsLoading,
  } = useQuery({
    queryKey: ["intelligence", "recommendations"],
    queryFn: () => intelligenceApi.getRecommendations(3),
  });

  const {
    data: weakAreas,
    isLoading: isWeakLoading,
  } = useQuery({
    queryKey: ["dashboard", "weak-areas"],
    queryFn: dashboardApi.getWeakAreas,
  });

  const {
    data: attemptsData,
  } = useQuery({
    queryKey: ["attempts", "active"],
    queryFn: () => attemptApi.getAttempt ? attemptApi.getAttempt("") : Promise.resolve(null),
    enabled: false, // Optional check
  });

  if (overviewError) {
    return (
      <AppShell title="Dashboard">
        <ErrorState onRetry={refetchOverview} />
      </AppShell>
    );
  }

  const isZeroState = overview && overview.quiz_attempts === 0;

  // Time of day greeting
  const hour = new Date().getHours();
  const timeGreeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";

  return (
    <AppShell title="Student Dashboard">
      <div className="space-y-6">
        {/* Dashboard Header Greeting */}
        <div className="rounded-2xl bg-gradient-to-r from-brand-950/70 via-slate-900 to-slate-900 border border-brand-500/20 p-6 shadow-xl relative overflow-hidden">
          <div className="absolute right-0 top-0 translate-x-12 -translate-y-6 w-64 h-64 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-2">
              <div className="flex flex-wrap items-center gap-2">
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-brand-500/20 text-brand-300 text-xs font-semibold">
                  <Sparkles className="w-3.5 h-3.5" />
                  Target Streams:
                </span>
                {user?.target_exams && user.target_exams.length > 0 ? (
                  user.target_exams.map((ex) => (
                    <Badge key={ex} variant="brand">
                      {ex === "GATE_CS"
                        ? "GATE CS"
                        : ex === "SSC_GK"
                        ? "SSC CGL"
                        : ex === "BANKING"
                        ? "Banking / PO"
                        : ex}
                    </Badge>
                  ))
                ) : (
                  <Badge variant="brand">GATE CS</Badge>
                )}
                <Link
                  to="/profile"
                  className="text-[11px] text-brand-400 hover:text-brand-300 hover:underline font-medium ml-1"
                >
                  Edit Streams →
                </Link>
              </div>

              <h1 className="text-xl md:text-2xl font-bold text-white tracking-tight">
                {timeGreeting}, {user?.full_name || "Student"}.
              </h1>
              <p className="text-sm text-slate-300 max-w-xl">
                Ready for your next practice? Focus on high-priority weak concepts across your enrolled exam streams to boost overall accuracy.
              </p>
            </div>

            <div className="flex items-center gap-3">
              <Link to="/exams">
                <Button variant="secondary" size="md">
                  View Syllabus
                </Button>
              </Link>
              <Link to="/quizzes">
                <Button variant="primary" size="md" rightIcon={<Play className="w-4 h-4" />}>
                  Start Practice Quiz
                </Button>
              </Link>
            </div>
          </div>
        </div>

        {/* Quick Action Navigation Buttons */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <Link to="/quizzes">
            <Card className="p-3.5 flex items-center gap-3 hover:border-brand-500/40 transition-colors">
              <div className="p-2 rounded-lg bg-brand-500/10 text-brand-400">
                <Play className="w-4 h-4" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-100">Start Quiz</p>
                <p className="text-[11px] text-slate-500">Explore quizzes</p>
              </div>
            </Card>
          </Link>

          <Link to="/analytics">
            <Card className="p-3.5 flex items-center gap-3 hover:border-amber-500/40 transition-colors">
              <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
                <AlertCircle className="w-4 h-4" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-100">Weak Topics</p>
                <p className="text-[11px] text-slate-500">Targeted practice</p>
              </div>
            </Card>
          </Link>

          <Link to="/results">
            <Card className="p-3.5 flex items-center gap-3 hover:border-emerald-500/40 transition-colors">
              <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                <Award className="w-4 h-4" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-100">Review Results</p>
                <p className="text-[11px] text-slate-500">View solutions</p>
              </div>
            </Card>
          </Link>

          <Link to="/analytics">
            <Card className="p-3.5 flex items-center gap-3 hover:border-sky-500/40 transition-colors">
              <div className="p-2 rounded-lg bg-sky-500/10 text-sky-400">
                <BarChart3 className="w-4 h-4" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-100">Analytics</p>
                <p className="text-[11px] text-slate-500">Track progress</p>
              </div>
            </Card>
          </Link>
        </div>

        {/* Quick Performance KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Target className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Overall Accuracy</p>
              {isOverviewLoading ? (
                <Skeleton className="h-6 w-16 mt-1" />
              ) : (
                <p className="text-lg font-bold text-slate-100">{overview?.overall_accuracy}%</p>
              )}
            </div>
          </Card>

          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 rounded-xl bg-brand-500/10 text-brand-400 border border-brand-500/20">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Questions Solved</p>
              {isOverviewLoading ? (
                <Skeleton className="h-6 w-16 mt-1" />
              ) : (
                <p className="text-lg font-bold text-slate-100">{overview?.questions_attempted}</p>
              )}
            </div>
          </Card>

          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <Flame className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Active Streak</p>
              {isOverviewLoading ? (
                <Skeleton className="h-6 w-16 mt-1" />
              ) : (
                <p className="text-lg font-bold text-slate-100">{overview?.active_streak_days} Days</p>
              )}
            </div>
          </Card>

          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <Clock className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Study Time</p>
              {isOverviewLoading ? (
                <Skeleton className="h-6 w-16 mt-1" />
              ) : (
                <p className="text-lg font-bold text-slate-100">
                  {Math.round((overview?.total_study_time_seconds || 0) / 60)} mins
                </p>
              )}
            </div>
          </Card>
        </div>

        {/* Zero State for New Students */}
        {isZeroState ? (
          <EmptyState
            icon={<Play className="w-12 h-12 text-brand-400" />}
            title="Start Your First Quiz"
            description="Your performance profile, weak topic analysis, and adaptive learning recommendations will appear here after your first quiz."
            actionText="Start Your First Quiz"
            onAction={() => (window.location.href = "/quizzes")}
          />
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Recommended Next Practice */}
            <div className="lg:col-span-2 space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-brand-400" />
                    Recommended Next Practice
                  </CardTitle>
                </CardHeader>

                <div className="space-y-3">
                  {isRecsLoading ? (
                    <div className="space-y-3">
                      <Skeleton className="h-16 w-full" />
                      <Skeleton className="h-16 w-full" />
                    </div>
                  ) : recommendations?.items && recommendations.items.length > 0 ? (
                    recommendations.items.map((rec) => (
                      <div
                        key={rec.topic_id}
                        className="p-4 rounded-xl border border-slate-800 bg-slate-800/40 hover:border-slate-700 transition-colors flex flex-col md:flex-row md:items-center justify-between gap-3"
                      >
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-slate-100 text-sm">
                              {rec.topic_name}
                            </span>
                            <Badge variant="neutral">{rec.subject_name}</Badge>
                            <Badge variant="brand">Accuracy: {rec.accuracy}%</Badge>
                          </div>
                          <p className="text-xs text-slate-400">{rec.explanation_reason}</p>
                        </div>

                        <Link to={`/quizzes?topic_id=${rec.topic_id}`}>
                          <Button variant="primary" size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
                            Practice Topic
                          </Button>
                        </Link>
                      </div>
                    ))
                  ) : (
                    <p className="text-xs text-slate-500 py-4 text-center">
                      All topics are in good health. Keep practicing to maintain high performance!
                    </p>
                  )}
                </div>
              </Card>
            </div>

            {/* Weak Areas Priorities */}
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertCircle className="w-5 h-5 text-amber-400" />
                    Weak Areas to Focus
                  </CardTitle>
                </CardHeader>

                <div className="space-y-3">
                  {isWeakLoading ? (
                    <Skeleton className="h-32 w-full" />
                  ) : weakAreas?.items && weakAreas.items.length > 0 ? (
                    weakAreas.items.slice(0, 4).map((weak) => (
                      <div
                        key={weak.topic_id}
                        className="p-3 rounded-lg bg-slate-800/50 border border-slate-800 flex items-center justify-between"
                      >
                        <div>
                          <p className="text-xs font-semibold text-slate-200">{weak.topic_name}</p>
                          <p className="text-[11px] text-slate-400">{weak.subject_name}</p>
                        </div>
                        <Badge
                          variant={
                            weak.accuracy < 50 ? "error" : weak.accuracy < 65 ? "warning" : "info"
                          }
                        >
                          {weak.accuracy}% Acc
                        </Badge>
                      </div>
                    ))
                  ) : (
                    <p className="text-xs text-slate-500 py-4 text-center">No weak topics detected.</p>
                  )}
                </div>
              </Card>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
};
