import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { AdminAppShell } from "../../components/layout/AdminAppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Skeleton } from "../../components/ui/Skeleton";
import { ErrorState } from "../../components/ui/ErrorState";
import { adminApi } from "../../services/adminApi";
import { ContentHealthIssue } from "../../types";
import { ShieldCheck, ShieldAlert, AlertCircle, RefreshCw, CheckCircle2, FileQuestion, Layers } from "lucide-react";

export const AdminContentQualityPage: React.FC = () => {
  const {
    data: report,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["admin", "content-health"],
    queryFn: adminApi.getContentHealthReport,
  });

  if (error) {
    return (
      <AdminAppShell title="Content Quality Control">
        <ErrorState onRetry={refetch} />
      </AdminAppShell>
    );
  }

  return (
    <AdminAppShell title="Content Quality & Health Control">
      <div className="space-y-6">
        {/* Header Controls */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              Content Quality & Health Scan System
            </h2>
            <p className="text-xs text-slate-400">
              Automated database health scanning for orphan questions, inactive taxonomy references, or missing solution content.
            </p>
          </div>

          <Button
            variant="outline"
            size="sm"
            leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
            onClick={() => refetch()}
            isLoading={isLoading}
          >
            Re-scan Database
          </Button>
        </div>

        {/* Overview Health Metrics */}
        {isLoading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
            <Skeleton className="h-24" />
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card className="p-4 flex items-center gap-3">
              <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <FileQuestion className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400">Total Questions</p>
                <p className="text-lg font-bold text-slate-100">{report?.total_questions || 0}</p>
              </div>
            </Card>

            <Card className="p-4 flex items-center gap-3">
              <div className="p-3 rounded-xl bg-brand-500/10 text-brand-400 border border-brand-500/20">
                <Layers className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400">Total Topics</p>
                <p className="text-lg font-bold text-slate-100">{report?.total_topics || 0}</p>
              </div>
            </Card>

            <Card className="p-4 flex items-center gap-3">
              <div className="p-3 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400">Quality Issues</p>
                <p className="text-lg font-bold text-amber-400">{report?.issue_count || 0}</p>
              </div>
            </Card>

            <Card className="p-4 flex items-center gap-3">
              <div className="p-3 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
                <CheckCircle2 className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400">Health Scan Status</p>
                <p className="text-sm font-bold text-emerald-400">
                  {report?.issue_count === 0 ? "100% Healthy" : "Action Needed"}
                </p>
              </div>
            </Card>
          </div>
        )}

        {/* Quality Issues List */}
        <Card className="p-6 space-y-4">
          <CardHeader>
            <CardTitle className="text-base font-bold text-slate-100 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-amber-400" />
              Detected Database Quality Issues
            </CardTitle>
          </CardHeader>

          {isLoading ? (
            <Skeleton className="h-48 w-full" />
          ) : report?.issues && report.issues.length > 0 ? (
            <div className="space-y-3">
              {report.issues.map((issue: ContentHealthIssue, idx: number) => (
                <div
                  key={idx}
                  className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 flex flex-col md:flex-row md:items-center justify-between gap-3"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <Badge variant={issue.severity === "ERROR" ? "error" : "warning"}>
                        {issue.severity}
                      </Badge>
                      <Badge variant="neutral">{issue.type}</Badge>
                      <span className="font-mono text-xs text-slate-400">ID: {issue.entity_id}</span>
                    </div>
                    <p className="text-xs text-slate-300">{issue.details}</p>
                  </div>

                  <Link to={`/admin/questions/${issue.entity_id}`}>
                    <Button variant="outline" size="sm">
                      Inspect & Fix Record
                    </Button>
                  </Link>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-8 text-center space-y-2">
              <CheckCircle2 className="w-10 h-10 text-emerald-400 mx-auto" />
              <p className="text-sm font-semibold text-slate-100">Zero Content Quality Issues Detected</p>
              <p className="text-xs text-slate-400 max-w-md mx-auto">
                All questions, subjects, and topics are properly assigned, linked, and verified.
              </p>
            </div>
          )}
        </Card>
      </div>
    </AdminAppShell>
  );
};
