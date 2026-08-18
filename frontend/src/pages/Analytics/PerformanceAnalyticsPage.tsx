import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { AppShell } from "../../components/layout/AppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Skeleton } from "../../components/ui/Skeleton";
import { ErrorState } from "../../components/ui/ErrorState";
import { EmptyState } from "../../components/ui/EmptyState";
import { intelligenceApi } from "../../services/intelligenceApi";
import { dashboardApi } from "../../services/dashboardApi";
import {
  BarChart3,
  Target,
  Clock,
  Zap,
  Sparkles,
  TrendingUp,
  AlertCircle,
  ArrowRight,
  Play,
  Award,
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

export const PerformanceAnalyticsPage: React.FC = () => {
  const {
    data: profile,
    isLoading: isProfileLoading,
    error: profileError,
    refetch,
  } = useQuery({
    queryKey: ["intelligence", "profile"],
    queryFn: intelligenceApi.getProfile,
  });

  const {
    data: speedAccuracy,
    isLoading: isSpeedLoading,
  } = useQuery({
    queryKey: ["intelligence", "speed-accuracy"],
    queryFn: intelligenceApi.getSpeedAccuracy,
  });

  const {
    data: performanceDelta,
    isLoading: isDeltaLoading,
  } = useQuery({
    queryKey: ["intelligence", "performance-delta"],
    queryFn: () => intelligenceApi.getPerformanceDelta(7),
  });

  const {
    data: topicMatrix,
    isLoading: isMatrixLoading,
  } = useQuery({
    queryKey: ["intelligence", "topic-matrix"],
    queryFn: intelligenceApi.getTopicMatrix,
  });

  const {
    data: subjectProgress,
    isLoading: isSubjectsLoading,
  } = useQuery({
    queryKey: ["dashboard", "subject-progress"],
    queryFn: dashboardApi.getSubjectProgress,
  });

  if (profileError) {
    return (
      <AppShell title="Learning Analytics">
        <ErrorState onRetry={refetch} />
      </AppShell>
    );
  }

  const isZeroState = profile && profile.total_questions_attempted === 0;

  return (
    <AppShell title="Student Performance Intelligence">
      <div className="space-y-6">
        {/* Banner */}
        <div className="rounded-2xl bg-gradient-to-r from-brand-950/60 via-slate-900 to-slate-900 border border-brand-500/20 p-6 shadow-xl relative overflow-hidden">
          <div className="absolute right-0 top-0 translate-x-12 -translate-y-6 w-64 h-64 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="relative z-10 space-y-2">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-brand-500/20 text-brand-300 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5" /> Prescriptive Analytics
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight">
              Evidence-Based Learning Intelligence
            </h1>
            <p className="text-xs text-slate-300 max-w-2xl">
              Track accuracy velocity, speed quadrant positioning, subject coverage, and targeted topic weakness priorities.
            </p>
          </div>
        </div>

        {isZeroState ? (
          <EmptyState
            icon={<BarChart3 className="w-12 h-12 text-brand-400" />}
            title="Build Your Analytics Profile"
            description="Complete your first quiz attempt to generate speed-accuracy quadrant positioning, accuracy velocity trends, and topic mastery matrices."
            actionText="Start Practice Quiz"
            onAction={() => (window.location.href = "/quizzes")}
          />
        ) : (
          <>
            {/* KPI Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Card className="p-4 flex items-center gap-3">
                <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  <Target className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs text-slate-400">Overall Accuracy</p>
                  {isProfileLoading ? (
                    <Skeleton className="h-6 w-16 mt-1" />
                  ) : (
                    <p className="text-lg font-bold text-slate-100">{profile?.overall_accuracy}%</p>
                  )}
                </div>
              </Card>

              <Card className="p-4 flex items-center gap-3">
                <div className="p-3 rounded-xl bg-brand-500/10 text-brand-400 border border-brand-500/20">
                  <Zap className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs text-slate-400">Solved Questions</p>
                  {isProfileLoading ? (
                    <Skeleton className="h-6 w-16 mt-1" />
                  ) : (
                    <p className="text-lg font-bold text-slate-100">{profile?.total_questions_attempted}</p>
                  )}
                </div>
              </Card>

              <Card className="p-4 flex items-center gap-3">
                <div className="p-3 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
                  <Clock className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs text-slate-400">Avg Speed / Q</p>
                  {isSpeedLoading ? (
                    <Skeleton className="h-6 w-16 mt-1" />
                  ) : (
                    <p className="text-lg font-bold text-slate-100">
                      {speedAccuracy?.average_speed_seconds_per_question || 45}s
                    </p>
                  )}
                </div>
              </Card>

              <Card className="p-4 flex items-center gap-3">
                <div className="p-3 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
                  <TrendingUp className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs text-slate-400">7d Accuracy Delta</p>
                  {isDeltaLoading ? (
                    <Skeleton className="h-6 w-16 mt-1" />
                  ) : (
                    <p className="text-lg font-bold text-emerald-400">
                      {performanceDelta?.accuracy_delta && performanceDelta.accuracy_delta > 0
                        ? `+${performanceDelta.accuracy_delta}%`
                        : `${performanceDelta?.accuracy_delta || 0}%`}
                    </p>
                  )}
                </div>
              </Card>
            </div>

            {/* Recharts Visualizations Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Subject Performance Bar Chart */}
              <Card className="p-6 space-y-4">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-base">
                    <BarChart3 className="w-5 h-5 text-brand-400" />
                    Subject Accuracy Breakdown
                  </CardTitle>
                </CardHeader>

                {isSubjectsLoading ? (
                  <Skeleton className="h-64 w-full" />
                ) : subjectProgress?.items && subjectProgress.items.length > 0 ? (
                  <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={subjectProgress.items} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="subject_name" stroke="#94a3b8" fontSize={11} tickLine={false} />
                        <YAxis stroke="#94a3b8" fontSize={11} domain={[0, 100]} />
                        <Tooltip
                          contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px" }}
                        />
                        <Bar dataKey="accuracy" fill="#6366f1" radius={[4, 4, 0, 0]} name="Accuracy %" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 py-12 text-center">
                    Complete subject quizzes to generate accuracy breakdown charts.
                  </p>
                )}
              </Card>

              {/* Speed & Accuracy Quadrant Analysis */}
              <Card className="p-6 space-y-4">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-base">
                    <Zap className="w-5 h-5 text-amber-400" />
                    Speed vs Accuracy Positioning
                  </CardTitle>
                </CardHeader>

                {isSpeedLoading ? (
                  <Skeleton className="h-64 w-full" />
                ) : speedAccuracy?.topics && speedAccuracy.topics.length > 0 ? (
                  <div className="space-y-3 max-h-64 overflow-y-auto pr-1">
                    {speedAccuracy.topics.map((item) => (
                      <div
                        key={item.topic_id}
                        className="p-3 rounded-lg bg-slate-800/50 border border-slate-800 flex items-center justify-between"
                      >
                        <div>
                          <p className="text-xs font-semibold text-slate-200">{item.topic_name}</p>
                          <p className="text-[11px] text-slate-400">{item.subject_name}</p>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge
                            variant={
                              item.quadrant === "FAST_ACCURATE"
                                ? "success"
                                : item.quadrant === "FAST_INACCURATE"
                                ? "warning"
                                : "info"
                            }
                          >
                            {item.quadrant.replace("_", " ")}
                          </Badge>
                          <span className="text-xs font-bold text-slate-300">{item.accuracy}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 py-12 text-center">
                    Solve more timed questions to populate your speed-accuracy matrix.
                  </p>
                )}
              </Card>
            </div>

            {/* Topic Mastery Matrix Table */}
            <Card className="p-6 space-y-4">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <Award className="w-5 h-5 text-emerald-400" />
                  Topic Mastery Matrix
                </CardTitle>
              </CardHeader>

              {isMatrixLoading ? (
                <Skeleton className="h-48 w-full" />
              ) : topicMatrix?.items && topicMatrix.items.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-800/60 text-slate-400 uppercase font-semibold">
                      <tr>
                        <th className="p-3 rounded-l-lg">Topic</th>
                        <th className="p-3">Subject</th>
                        <th className="p-3">Questions Solved</th>
                        <th className="p-3">Accuracy</th>
                        <th className="p-3">Health Status</th>
                        <th className="p-3 rounded-r-lg text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800 text-slate-200">
                      {topicMatrix.items.map((row) => (
                        <tr key={row.topic_id} className="hover:bg-slate-800/40">
                          <td className="p-3 font-semibold text-slate-100">{row.topic_name}</td>
                          <td className="p-3 text-slate-400">{row.subject_name}</td>
                          <td className="p-3">{row.questions_attempted}</td>
                          <td className="p-3 font-bold text-emerald-400">{row.accuracy}%</td>
                          <td className="p-3">
                            <Badge
                              variant={
                                row.health_status === "STRONG" || row.health_status === "IMPROVING"
                                  ? "success"
                                  : row.health_status === "WEAK" || row.health_status === "DECLINING"
                                  ? "error"
                                  : "warning"
                              }
                            >
                              {row.health_status}
                            </Badge>
                          </td>
                          <td className="p-3 text-right">
                            <Link to={`/quizzes?topic_id=${row.topic_id}`}>
                              <Button variant="ghost" size="sm">
                                Practice
                              </Button>
                            </Link>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-xs text-slate-500 py-6 text-center">No topic matrix data available.</p>
              )}
            </Card>
          </>
        )}
      </div>
    </AppShell>
  );
};
