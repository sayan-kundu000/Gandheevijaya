import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AdminAppShell } from "../../components/layout/AdminAppShell";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import { Select } from "../../components/ui/Select";
import { Modal } from "../../components/ui/Modal";
import { Table, Column } from "../../components/ui/Table";
import { ErrorState } from "../../components/ui/ErrorState";
import { quizApi } from "../../services/quizApi";
import { taxonomyApi } from "../../services/taxonomyApi";
import { adminApi } from "../../services/adminApi";
import { Quiz, QuestionPoolInfoResponse } from "../../types";
import { BookOpen, Plus, CheckCircle, Archive, Search, ShieldCheck, AlertCircle } from "lucide-react";

export const AdminQuizManagementPage: React.FC = () => {
  const queryClient = useQueryClient();

  const [isBuilderOpen, setIsBuilderOpen] = useState(false);
  const [poolInfo, setPoolInfo] = useState<QuestionPoolInfoResponse | null>(null);

  // Form State
  const [subjectId, setSubjectId] = useState<number>(1);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [durationMinutes, setDurationMinutes] = useState<number>(30);
  const [passingScore, setPassingScore] = useState<number>(50);
  const [negativeMarking, setNegativeMarking] = useState<number>(0.25);
  const [isPublished, setIsPublished] = useState(true);

  const { data: subjects } = useQuery({
    queryKey: ["admin", "subjects"],
    queryFn: () => taxonomyApi.getSubjects(),
  });

  const {
    data: quizzes,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["admin", "quizzes"],
    queryFn: () => quizApi.getQuizzes(),
  });

  const createQuizMutation = useMutation({
    mutationFn: () =>
      adminApi.createQuiz({
        subject_id: subjectId,
        title: title.trim(),
        description: description.trim() || undefined,
        duration_minutes: durationMinutes,
        passing_score: passingScore,
        negative_marking: negativeMarking,
        is_published: isPublished,
        status: isPublished ? "PUBLISHED" : "DRAFT",
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "quizzes"] });
      queryClient.invalidateQueries({ queryKey: ["quizzes"] });
      setIsBuilderOpen(false);
      setTitle("");
      setDescription("");
    },
  });

  const publishMutation = useMutation({
    mutationFn: (quizId: number) => adminApi.publishQuiz(quizId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin", "quizzes"] }),
  });

  const archiveMutation = useMutation({
    mutationFn: (quizId: number) => adminApi.archiveQuiz(quizId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin", "quizzes"] }),
  });

  const inspectPool = async (quizId: number) => {
    try {
      const data = await adminApi.inspectQuestionPool(quizId);
      setPoolInfo(data);
    } catch (e) {
      // Ignore
    }
  };

  const columns: Column<Quiz>[] = [
    {
      key: "title",
      header: "Quiz Title",
      cell: (row) => <span className="font-bold text-slate-100">{row.title}</span>,
    },
    {
      key: "subject",
      header: "Subject Module",
      cell: (row) => <Badge variant="brand">{row.subject_name || "Subject #" + row.subject_id}</Badge>,
    },
    {
      key: "duration_minutes",
      header: "Duration",
      cell: (row) => <span className="font-mono text-slate-300">{row.duration_minutes} Mins</span>,
    },
    {
      key: "question_count",
      header: "Questions",
      cell: (row) => <span className="font-semibold text-slate-200">{row.question_count || 10}</span>,
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => (
        <Badge variant={row.is_published ? "success" : "neutral"}>
          {row.is_published ? "Published" : "Draft"}
        </Badge>
      ),
    },
    {
      key: "actions",
      header: "Actions",
      cell: (row) => (
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={() => inspectPool(row.id)}>
            Pool Health
          </Button>
          {!row.is_published && (
            <Button
              variant="primary"
              size="sm"
              isLoading={publishMutation.isPending}
              onClick={() => publishMutation.mutate(row.id)}
            >
              Publish
            </Button>
          )}
          {row.is_published && (
            <Button
              variant="danger"
              size="sm"
              isLoading={archiveMutation.isPending}
              onClick={() => archiveMutation.mutate(row.id)}
            >
              Archive
            </Button>
          )}
        </div>
      ),
    },
  ];

  if (error) {
    return (
      <AdminAppShell title="Quiz Catalog">
        <ErrorState onRetry={refetch} />
      </AdminAppShell>
    );
  }

  return (
    <AdminAppShell title="Quiz Catalog & Builder">
      <div className="space-y-6">
        {/* Header Bar */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-rose-400" />
              Assessment Quizzes & Practice Catalog
            </h2>
            <p className="text-xs text-slate-400">
              Configure practice test specifications, validate question pool availability, and manage publishing states.
            </p>
          </div>

          <Button
            variant="primary"
            size="sm"
            leftIcon={<Plus className="w-4 h-4" />}
            onClick={() => setIsBuilderOpen(true)}
          >
            Create New Quiz
          </Button>
        </div>

        {/* Quizzes Table */}
        <Card className="p-6 space-y-4">
          <Table
            columns={columns}
            data={quizzes || []}
            keyExtractor={(r) => r.id}
            isLoading={isLoading}
            emptyTitle="No Quizzes Found"
            emptyDescription="Create your first quiz test to start offering student practice."
          />
        </Card>

        {/* Question Pool Inspection Modal */}
        {poolInfo && (
          <Modal isOpen={!!poolInfo} onClose={() => setPoolInfo(null)} title="Question Pool Availability Scan">
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Pool Validation Status:</span>
                  <Badge variant={poolInfo.has_sufficient_pool ? "success" : "error"}>
                    {poolInfo.has_sufficient_pool ? "Sufficient Pool" : "Insufficient Pool"}
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Requested Question Count:</span>
                  <span className="font-bold text-slate-100">{poolInfo.requested_count}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Available Published Questions:</span>
                  <span className="font-bold text-emerald-400">{poolInfo.available_published_questions}</span>
                </div>
              </div>

              {!poolInfo.has_sufficient_pool && (
                <p className="text-xs text-rose-400/90 font-medium">
                  Warning: The subject does not have enough published questions to fulfill this quiz requirement. Please publish more questions before publishing this quiz.
                </p>
              )}
            </div>
          </Modal>
        )}

        {/* Quiz Builder Modal */}
        <Modal isOpen={isBuilderOpen} onClose={() => setIsBuilderOpen(false)} title="Configure New Quiz">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              createQuizMutation.mutate();
            }}
            className="space-y-4"
          >
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Subject Module</label>
              <Select value={String(subjectId)} onChange={(e) => setSubjectId(Number(e.target.value))} required>
                {subjects?.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.code})
                  </option>
                ))}
              </Select>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Quiz Title</label>
              <Input
                required
                placeholder="C Pointers & Array Practice Quiz"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Description</label>
              <Input
                placeholder="Timed 30-minute practice exam covering pointer expressions."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-300">Duration (Mins)</label>
                <Input
                  type="number"
                  required
                  value={durationMinutes}
                  onChange={(e) => setDurationMinutes(Number(e.target.value))}
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-300">Passing Score %</label>
                <Input
                  type="number"
                  required
                  value={passingScore}
                  onChange={(e) => setPassingScore(Number(e.target.value))}
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-300">Negative Penalty</label>
                <Input
                  type="number"
                  step="0.01"
                  required
                  value={negativeMarking}
                  onChange={(e) => setNegativeMarking(Number(e.target.value))}
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
              <Button type="button" variant="ghost" onClick={() => setIsBuilderOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" variant="primary" isLoading={createQuizMutation.isPending}>
                Create Quiz
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </AdminAppShell>
  );
};
