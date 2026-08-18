import React, { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { AdminAppShell } from "../../components/layout/AdminAppShell";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import { Select } from "../../components/ui/Select";
import { Pagination } from "../../components/ui/Pagination";
import { Modal } from "../../components/ui/Modal";
import { Checkbox } from "../../components/ui/Checkbox";
import { Table, Column } from "../../components/ui/Table";
import { ErrorState } from "../../components/ui/ErrorState";
import { QuestionRenderer } from "../../features/attempts/components/QuestionRenderer";
import { adminApi } from "../../services/adminApi";
import { taxonomyApi } from "../../services/taxonomyApi";
import { Question, QuestionDifficulty, QuestionType, QuestionStatus } from "../../types";
import {
  FileQuestion,
  Plus,
  Search,
  CheckCircle,
  XCircle,
  Archive,
  Eye,
  Layers,
  Sparkles,
} from "lucide-react";

export const AdminQuestionBankPage: React.FC = () => {
  const queryClient = useQueryClient();

  // Filters State
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [topicId, setTopicId] = useState<number | undefined>(undefined);
  const [questionType, setQuestionType] = useState<string>("");
  const [difficulty, setDifficulty] = useState<string>("");
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");

  // Bulk Selection State
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  // Preview & Editor Modals
  const [previewQuestion, setPreviewQuestion] = useState<Question | null>(null);
  const [isEditorOpen, setIsEditorOpen] = useState(false);

  // Question Form State
  const [qTopicId, setQTopicId] = useState<number>(1);
  const [qType, setQType] = useState<QuestionType>("MCQ");
  const [qDiff, setQDiff] = useState<QuestionDifficulty>("MEDIUM");
  const [qText, setQText] = useState("");
  const [optA, setOptA] = useState("");
  const [optB, setOptB] = useState("");
  const [optC, setOptC] = useState("");
  const [optD, setOptD] = useState("");
  const [correctAnswer, setCorrectAnswer] = useState("A");
  const [explanation, setExplanation] = useState("");

  // Debounce search input
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(handler);
  }, [search]);

  const { data: topics } = useQuery({
    queryKey: ["admin", "topics"],
    queryFn: () => taxonomyApi.getTopics(),
  });

  const {
    data: questionsData,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["admin", "questions", page, pageSize, topicId, questionType, difficulty, statusFilter, debouncedSearch],
    queryFn: () =>
      adminApi.getQuestions({
        page,
        page_size: pageSize,
        topic_id: topicId,
        question_type: questionType || undefined,
        difficulty: difficulty || undefined,
        status: statusFilter || undefined,
      }),
  });

  const createQuestionMutation = useMutation({
    mutationFn: () =>
      adminApi.createQuestion({
        topic_id: qTopicId,
        type: qType,
        difficulty: qDiff,
        question_text: qText.trim(),
        options: qType === "NAT" ? null : { A: optA, B: optB, C: optC, D: optD },
        correct_answer: correctAnswer.trim(),
        explanation: explanation.trim(),
        status: "PUBLISHED",
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "questions"] });
      setIsEditorOpen(false);
      setQText("");
      setExplanation("");
    },
  });

  const bulkStatusMutation = useMutation({
    mutationFn: (targetStatus: string) => adminApi.bulkUpdateQuestionStatus(selectedIds, targetStatus),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "questions"] });
      setSelectedIds([]);
    },
  });

  const handleSelectAll = (checked: boolean) => {
    if (checked && questionsData?.items) {
      setSelectedIds(questionsData.items.map((q) => q.id));
    } else {
      setSelectedIds([]);
    }
  };

  const toggleSelect = (id: string) => {
    setSelectedIds((prev) => (prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]));
  };

  const columns: Column<Question>[] = [
    {
      key: "select",
      header: (
        <Checkbox
          checked={selectedIds.length > 0 && selectedIds.length === (questionsData?.items?.length || 0)}
          onChange={(e) => handleSelectAll(e.target.checked)}
        />
      ),
      cell: (row) => (
        <Checkbox checked={selectedIds.includes(row.id)} onChange={() => toggleSelect(row.id)} />
      ),
    },
    {
      key: "id",
      header: "Question ID",
      cell: (row) => (
        <Link to={`/admin/questions/${row.id}`} className="font-mono text-xs text-brand-400 hover:underline">
          {row.id}
        </Link>
      ),
    },
    {
      key: "question_text",
      header: "Prompt",
      cell: (row) => <span className="text-slate-200 line-clamp-1 max-w-md">{row.question_text}</span>,
    },
    {
      key: "type",
      header: "Type",
      cell: (row) => <Badge variant={row.type === "MSQ" ? "warning" : row.type === "NAT" ? "info" : "neutral"}>{row.type}</Badge>,
    },
    {
      key: "difficulty",
      header: "Difficulty",
      cell: (row) => (
        <Badge
          variant={
            row.difficulty === "HARD" ? "error" : row.difficulty === "MEDIUM" ? "warning" : "success"
          }
        >
          {row.difficulty}
        </Badge>
      ),
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => (
        <Badge variant={row.status === "PUBLISHED" ? "success" : "neutral"}>{row.status}</Badge>
      ),
    },
    {
      key: "actions",
      header: "Actions",
      cell: (row) => (
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setPreviewQuestion(row)}
            title="Preview Student View"
          >
            <Eye className="w-3.5 h-3.5" />
          </Button>
          <Link to={`/admin/questions/${row.id}`}>
            <Button variant="outline" size="sm">
              Details
            </Button>
          </Link>
        </div>
      ),
    },
  ];

  if (error) {
    return (
      <AdminAppShell title="Question Bank">
        <ErrorState onRetry={refetch} />
      </AdminAppShell>
    );
  }

  const totalPages = Math.ceil((questionsData?.total || 0) / pageSize);

  return (
    <AdminAppShell title="Question Bank Management">
      <div className="space-y-6">
        {/* Header Bar */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <FileQuestion className="w-5 h-5 text-brand-400" />
              Central Question Bank Repository
            </h2>
            <p className="text-xs text-slate-400">
              High-performance server-side paginated question bank with C/DSA code block rendering and lifecycle controls.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="primary"
              size="sm"
              leftIcon={<Plus className="w-4 h-4" />}
              onClick={() => setIsEditorOpen(true)}
            >
              Create Question
            </Button>
          </div>
        </div>

        {/* Filter Toolbar */}
        <Card className="p-4 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3">
            <Input
              placeholder="Search prompt..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />

            <Select
              value={topicId ? String(topicId) : ""}
              onChange={(e) => setTopicId(e.target.value ? Number(e.target.value) : undefined)}
            >
              <option value="">All Topics</option>
              {topics?.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </Select>

            <Select value={questionType} onChange={(e) => setQuestionType(e.target.value)}>
              <option value="">All Types (MCQ, MSQ, NAT)</option>
              <option value="MCQ">MCQ (Single Choice)</option>
              <option value="MSQ">MSQ (Multiple Select)</option>
              <option value="NAT">NAT (Numerical)</option>
            </Select>

            <Select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
              <option value="">All Difficulties</option>
              <option value="EASY">EASY</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="HARD">HARD</option>
            </Select>

            <Select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
              <option value="">All Statuses</option>
              <option value="PUBLISHED">PUBLISHED</option>
              <option value="DRAFT">DRAFT</option>
              <option value="ARCHIVED">ARCHIVED</option>
            </Select>
          </div>

          {/* Bulk Actions Bar */}
          {selectedIds.length > 0 && (
            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-900 border border-slate-800 text-xs">
              <span className="font-semibold text-slate-300">
                {selectedIds.length} question(s) selected
              </span>

              <div className="flex items-center gap-2">
                <Button
                  variant="secondary"
                  size="sm"
                  isLoading={bulkStatusMutation.isPending}
                  onClick={() => bulkStatusMutation.mutate("PUBLISHED")}
                >
                  Bulk Publish
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  isLoading={bulkStatusMutation.isPending}
                  onClick={() => bulkStatusMutation.mutate("UNPUBLISHED")}
                >
                  Bulk Unpublish
                </Button>
                <Button
                  variant="danger"
                  size="sm"
                  isLoading={bulkStatusMutation.isPending}
                  onClick={() => bulkStatusMutation.mutate("ARCHIVED")}
                >
                  Bulk Archive
                </Button>
              </div>
            </div>
          )}
        </Card>

        {/* Data Table */}
        <Card className="p-6 space-y-4">
          <Table
            columns={columns}
            data={questionsData?.items || []}
            keyExtractor={(r) => r.id}
            isLoading={isLoading}
            emptyTitle="No Questions Found"
            emptyDescription="Try adjusting search parameters or create a new question."
          />

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="pt-4 border-t border-slate-800">
              <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
            </div>
          )}
        </Card>

        {/* Student View Question Preview Modal */}
        {previewQuestion && (
          <Modal
            isOpen={!!previewQuestion}
            onClose={() => setPreviewQuestion(null)}
            title="Student Perspective Question Preview"
          >
            <div className="space-y-4">
              <QuestionRenderer
                question={{
                  id: previewQuestion.id,
                  type: previewQuestion.type,
                  question_text: previewQuestion.question_text,
                  options: previewQuestion.options,
                  marks: 1.0,
                  negative_marks: 0.25,
                }}
                selectedAnswer={null}
                onSelectAnswer={() => {}}
                disabled
              />

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
                <p className="font-bold text-emerald-400">Admin Answer Key & Explanation:</p>
                <p className="text-slate-300">
                  <span className="text-slate-400">Correct Answer: </span>
                  <span className="font-bold text-emerald-300">{previewQuestion.correct_answer || "N/A"}</span>
                </p>
                {previewQuestion.explanation && (
                  <p className="text-slate-300 font-mono whitespace-pre-wrap">
                    {previewQuestion.explanation}
                  </p>
                )}
              </div>
            </div>
          </Modal>
        )}

        {/* Create Question Modal Editor */}
        <Modal isOpen={isEditorOpen} onClose={() => setIsEditorOpen(false)} title="Create Question Bank Record">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              createQuestionMutation.mutate();
            }}
            className="space-y-4"
          >
            <div className="grid grid-cols-3 gap-3">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-300">Topic</label>
                <Select value={String(qTopicId)} onChange={(e) => setQTopicId(Number(e.target.value))}>
                  {topics?.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.name}
                    </option>
                  ))}
                </Select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-300">Type</label>
                <Select value={qType} onChange={(e) => setQType(e.target.value as QuestionType)}>
                  <option value="MCQ">MCQ</option>
                  <option value="MSQ">MSQ</option>
                  <option value="NAT">NAT</option>
                </Select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-300">Difficulty</label>
                <Select value={qDiff} onChange={(e) => setQDiff(e.target.value as QuestionDifficulty)}>
                  <option value="EASY">EASY</option>
                  <option value="MEDIUM">MEDIUM</option>
                  <option value="HARD">HARD</option>
                </Select>
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Question Prompt / Code</label>
              <textarea
                required
                rows={4}
                placeholder="Enter question statement or C code block..."
                value={qText}
                onChange={(e) => setQText(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs font-mono text-slate-100 focus:outline-none focus:ring-1 focus:ring-brand-500"
              />
            </div>

            {qType !== "NAT" && (
              <div className="grid grid-cols-2 gap-3 text-xs">
                <Input placeholder="Option A" value={optA} onChange={(e) => setOptA(e.target.value)} required />
                <Input placeholder="Option B" value={optB} onChange={(e) => setOptB(e.target.value)} required />
                <Input placeholder="Option C" value={optC} onChange={(e) => setOptC(e.target.value)} required />
                <Input placeholder="Option D" value={optD} onChange={(e) => setOptD(e.target.value)} required />
              </div>
            )}

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Correct Answer Key</label>
              <Input
                required
                placeholder={qType === "NAT" ? "e.g. 42" : "e.g. A or A,B"}
                value={correctAnswer}
                onChange={(e) => setCorrectAnswer(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Solution Explanation</label>
              <textarea
                required
                rows={3}
                placeholder="Detailed step-by-step solution derivation..."
                value={explanation}
                onChange={(e) => setExplanation(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-100 focus:outline-none focus:ring-1 focus:ring-brand-500"
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
              <Button type="button" variant="ghost" onClick={() => setIsEditorOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" variant="primary" isLoading={createQuestionMutation.isPending}>
                Create Question
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </AdminAppShell>
  );
};
