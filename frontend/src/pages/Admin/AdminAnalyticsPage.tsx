import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { AdminAppShell } from "../../components/layout/AdminAppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Table, Column } from "../../components/ui/Table";
import { Tabs, TabItem } from "../../components/ui/Tabs";
import { ErrorState } from "../../components/ui/ErrorState";
import { adminApi } from "../../services/adminApi";
import { Attempt, SecurityAuditLogItem } from "../../types";
import { BarChart3, ShieldCheck, Clock, CheckCircle2, User, Key } from "lucide-react";

export const AdminAnalyticsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState("attempts");

  const {
    data: attemptsData,
    isLoading: isAttemptsLoading,
    error: attemptsError,
    refetch,
  } = useQuery({
    queryKey: ["admin", "attempts"],
    queryFn: () => adminApi.getAdminAttempts({ page_size: 20 }),
  });

  const {
    data: auditData,
    isLoading: isAuditLoading,
  } = useQuery({
    queryKey: ["admin", "audit-logs"],
    queryFn: () => adminApi.getAuditLogs({ page_size: 20 }),
    enabled: activeTab === "audit",
  });

  const attemptColumns: Column<Attempt>[] = [
    {
      key: "id",
      header: "Attempt ID",
      cell: (row) => <span className="font-mono text-xs text-brand-300">{row.id}</span>,
    },
    {
      key: "user_id",
      header: "Student ID",
      cell: (row) => <span className="font-mono text-xs text-slate-400">{row.user_id}</span>,
    },
    {
      key: "quiz_id",
      header: "Quiz ID",
      cell: (row) => <Badge variant="neutral">Quiz #{row.quiz_id}</Badge>,
    },
    {
      key: "score",
      header: "Score / Marks",
      cell: (row) => (
        <span className="font-bold text-brand-400">
          {row.score} / {row.total_marks}
        </span>
      ),
    },
    {
      key: "accuracy",
      header: "Accuracy",
      cell: (row) => <span className="font-bold text-emerald-400">{row.accuracy}%</span>,
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => (
        <Badge
          variant={
            row.status === "SUBMITTED"
              ? "success"
              : row.status === "EXPIRED"
              ? "error"
              : "warning"
          }
        >
          {row.status}
        </Badge>
      ),
    },
    {
      key: "started_at",
      header: "Started Date",
      cell: (row) => <span className="text-xs text-slate-400">{new Date(row.started_at).toLocaleString()}</span>,
    },
  ];

  const auditColumns: Column<SecurityAuditLogItem>[] = [
    {
      key: "id",
      header: "Log ID",
      cell: (row) => <span className="font-mono text-slate-400 text-xs">#{row.id}</span>,
    },
    {
      key: "event_type",
      header: "Event Action",
      cell: (row) => <Badge variant="brand">{row.event_type}</Badge>,
    },
    {
      key: "user_id",
      header: "Actor ID",
      cell: (row) => <span className="font-mono text-xs text-slate-300">{row.user_id || "SYSTEM"}</span>,
    },
    {
      key: "ip_address",
      header: "IP Address",
      cell: (row) => <span className="font-mono text-xs text-slate-400">{row.ip_address || "127.0.0.1"}</span>,
    },
    {
      key: "created_at",
      header: "Timestamp",
      cell: (row) => <span className="text-xs text-slate-400">{new Date(row.created_at).toLocaleString()}</span>,
    },
  ];

  const tabs: TabItem[] = [
    { id: "attempts", label: "Student Attempts Feed" },
    { id: "audit", label: "Security Audit Logs" },
  ];

  if (attemptsError) {
    return (
      <AdminAppShell title="Platform Analytics">
        <ErrorState onRetry={refetch} />
      </AdminAppShell>
    );
  }

  return (
    <AdminAppShell title="Platform Operations & Audit Analytics">
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-brand-400" />
            Platform Activity & Security Audit Trail
          </h2>
          <p className="text-xs text-slate-400">
            Real-time student attempt evaluation logs and append-only administrative security audit trail.
          </p>
        </div>

        {/* Tabbed Activity Data */}
        <Card className="p-6 space-y-4">
          <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />

          {activeTab === "attempts" && (
            <Table
              columns={attemptColumns}
              data={attemptsData?.items || []}
              keyExtractor={(r) => r.id}
              isLoading={isAttemptsLoading}
              emptyTitle="No Attempts Recorded"
              emptyDescription="Student quiz attempts will appear here in real time."
            />
          )}

          {activeTab === "audit" && (
            <Table
              columns={auditColumns}
              data={auditData?.items || []}
              keyExtractor={(r) => String(r.id)}
              isLoading={isAuditLoading}
              emptyTitle="No Audit Logs Found"
              emptyDescription="Administrative security audit events will appear here."
            />
          )}
        </Card>
      </div>
    </AdminAppShell>
  );
};
