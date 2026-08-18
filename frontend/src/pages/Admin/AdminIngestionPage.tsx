import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AdminAppShell } from "../../components/layout/AdminAppShell";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import { Checkbox } from "../../components/ui/Checkbox";
import { Modal } from "../../components/ui/Modal";
import { Table, Column } from "../../components/ui/Table";
import { ErrorState } from "../../components/ui/ErrorState";
import { adminApi } from "../../services/adminApi";
import { ContentImportJobItem, ContentImportJobDetailResponse } from "../../types";
import { Database, Play, AlertCircle, CheckCircle2, XCircle, RefreshCw, FileText } from "lucide-react";

export const AdminIngestionPage: React.FC = () => {
  const queryClient = useQueryClient();

  const [isTriggerModalOpen, setIsTriggerModalOpen] = useState(false);
  const [jobDetail, setJobDetail] = useState<ContentImportJobDetailResponse | null>(null);

  // Import Form State
  const [sourcePath, setSourcePath] = useState("datasets");
  const [dryRun, setDryRun] = useState(false);
  const [upsert, setUpsert] = useState(false);
  const [subjectOverride, setSubjectOverride] = useState("");

  const {
    data: jobsData,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["admin", "imports"],
    queryFn: () => adminApi.getImportJobs(),
  });

  const triggerMutation = useMutation({
    mutationFn: () =>
      adminApi.triggerImport({
        source_path: sourcePath.trim(),
        dry_run: dryRun,
        upsert: upsert,
        subject: subjectOverride.trim() || undefined,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "imports"] });
      queryClient.invalidateQueries({ queryKey: ["admin", "questions"] });
      setIsTriggerModalOpen(false);
    },
  });

  const inspectJob = async (jobId: number) => {
    try {
      const data = await adminApi.getImportJobDetail(jobId);
      setJobDetail(data);
    } catch (e) {
      // Ignore
    }
  };

  const columns: Column<ContentImportJobItem>[] = [
    {
      key: "id",
      header: "Job ID",
      cell: (row) => <span className="font-mono font-bold text-slate-300">#{row.id}</span>,
    },
    {
      key: "source_path",
      header: "Source Path / File",
      cell: (row) => <span className="font-mono text-xs text-brand-300">{row.source_path}</span>,
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => (
        <Badge
          variant={
            row.status === "COMPLETED"
              ? "success"
              : row.status === "FAILED"
              ? "error"
              : "warning"
          }
        >
          {row.status}
        </Badge>
      ),
    },
    {
      key: "total_found",
      header: "Found",
      cell: (row) => <span className="text-slate-300 font-mono">{row.total_found}</span>,
    },
    {
      key: "total_imported",
      header: "Imported",
      cell: (row) => <span className="text-emerald-400 font-bold font-mono">{row.total_imported}</span>,
    },
    {
      key: "total_skipped",
      header: "Skipped",
      cell: (row) => <span className="text-amber-400 font-mono">{row.total_skipped}</span>,
    },
    {
      key: "total_errors",
      header: "Errors",
      cell: (row) => <span className="text-rose-400 font-bold font-mono">{row.total_errors}</span>,
    },
    {
      key: "started_at",
      header: "Started Date",
      cell: (row) => <span className="text-xs text-slate-400">{new Date(row.started_at).toLocaleString()}</span>,
    },
    {
      key: "actions",
      header: "Actions",
      cell: (row) => (
        <Button variant="ghost" size="sm" onClick={() => inspectJob(row.id)}>
          Logs
        </Button>
      ),
    },
  ];

  if (error) {
    return (
      <AdminAppShell title="Ingestion Pipeline">
        <ErrorState onRetry={refetch} />
      </AdminAppShell>
    );
  }

  return (
    <AdminAppShell title="JSON ETL Ingestion Pipeline">
      <div className="space-y-6">
        {/* Header Controls */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Database className="w-5 h-5 text-purple-400" />
              Question Bank Ingestion Pipeline Monitor
            </h2>
            <p className="text-xs text-slate-400">
              Track real-time JSON → PostgreSQL ETL ingestion, validation errors, skipped duplicate records, and dry-run previews.
            </p>
          </div>

          <Button
            variant="primary"
            size="sm"
            leftIcon={<Play className="w-4 h-4" />}
            onClick={() => setIsTriggerModalOpen(true)}
          >
            Trigger ETL Import
          </Button>
        </div>

        {/* Job History Table */}
        <Card className="p-6 space-y-4">
          <Table
            columns={columns}
            data={jobsData?.items || []}
            keyExtractor={(r) => r.id}
            isLoading={isLoading}
            emptyTitle="No Import Jobs Recorded"
            emptyDescription="Click 'Trigger ETL Import' to run your first JSON question ingestion job."
          />
        </Card>

        {/* Job Detail & Error Logs Modal */}
        {jobDetail && (
          <Modal isOpen={!!jobDetail} onClose={() => setJobDetail(null)} title={`Import Job #${jobDetail.job.id} Log Report`}>
            <div className="space-y-4">
              <div className="grid grid-cols-4 gap-3 p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs text-center font-mono">
                <div>
                  <p className="text-slate-400">Found</p>
                  <p className="text-sm font-bold text-slate-100">{jobDetail.job.total_found}</p>
                </div>
                <div>
                  <p className="text-slate-400">Imported</p>
                  <p className="text-sm font-bold text-emerald-400">{jobDetail.job.total_imported}</p>
                </div>
                <div>
                  <p className="text-slate-400">Skipped</p>
                  <p className="text-sm font-bold text-amber-400">{jobDetail.job.total_skipped}</p>
                </div>
                <div>
                  <p className="text-slate-400">Errors</p>
                  <p className="text-sm font-bold text-rose-400">{jobDetail.job.total_errors}</p>
                </div>
              </div>

              {jobDetail.error_logs && jobDetail.error_logs.length > 0 ? (
                <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
                  <p className="text-xs font-bold text-rose-400">Validation & System Error Logs:</p>
                  {jobDetail.error_logs.map((log, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-rose-950/20 border border-rose-900/30 text-xs font-mono">
                      <p className="font-semibold text-rose-300">{log.error_type}</p>
                      <p className="text-slate-300">{log.message}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-400 py-4 text-center">
                  No error logs recorded for this import job. All records imported cleanly.
                </p>
              )}
            </div>
          </Modal>
        )}

        {/* Trigger Import Modal */}
        <Modal isOpen={isTriggerModalOpen} onClose={() => setIsTriggerModalOpen(false)} title="Run Question Bank Ingestion Pipeline">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              triggerMutation.mutate();
            }}
            className="space-y-4"
          >
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Source Directory / JSON File Path</label>
              <Input
                required
                placeholder="datasets"
                value={sourcePath}
                onChange={(e) => setSourcePath(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Default Subject Override (Optional)</label>
              <Input
                placeholder="CPROG or DSA"
                value={subjectOverride}
                onChange={(e) => setSubjectOverride(e.target.value)}
              />
            </div>

            <div className="space-y-3 pt-2">
              <Checkbox
                label="Dry Run Mode (Validate and preview without mutating database)"
                checked={dryRun}
                onChange={(e) => setDryRun(e.target.checked)}
              />

              <Checkbox
                label="Upsert Mode (Update existing duplicate questions with new content)"
                checked={upsert}
                onChange={(e) => setUpsert(e.target.checked)}
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
              <Button type="button" variant="ghost" onClick={() => setIsTriggerModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" variant="primary" isLoading={triggerMutation.isPending}>
                Run Ingestion Pipeline
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </AdminAppShell>
  );
};
