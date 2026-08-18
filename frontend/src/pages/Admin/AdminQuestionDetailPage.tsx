import React from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AdminAppShell } from "../../components/layout/AdminAppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Skeleton } from "../../components/ui/Skeleton";
import { ErrorState } from "../../components/ui/ErrorState";
import { adminApi } from "../../services/adminApi";
import { ArrowLeft, CheckCircle, XCircle, Archive, BookOpen, Layers, Sparkles } from "lucide-react";

export const AdminQuestionDetailPage: React.FC = () => {
  const { questionId } = useParams<{ questionId: string }>();
  const queryClient = useQueryClient();

  const {
    data: question,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["admin", "question", questionId],
    queryFn: () => adminApi.getQuestionDetail(questionId || ""),
    enabled: !!questionId,
  });

  const publishMutation = useMutation({
    mutationFn: () => adminApi.publishQuestion(questionId || ""),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin", "question", questionId] }),
  });

  const unpublishMutation = useMutation({
    mutationFn: () => adminApi.unpublishQuestion(questionId || ""),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin", "question", questionId] }),
  });

  const archiveMutation = useMutation({
    mutationFn: () => adminApi.archiveQuestion(questionId || ""),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin", "question", questionId] }),
  });

  if (error) {
    return (
      <AdminAppShell title="Question Record Detail">
        <ErrorState onRetry={refetch} />
      </AdminAppShell>
    );
  }

  if (isLoading || !question) {
    return (
      <AdminAppShell title="Question Record Detail">
        <Skeleton className="h-96 w-full" />
      </AdminAppShell>
    );
  }

  const isCCode =
    question.question_text.includes("#include") ||
    question.question_text.includes("int main") ||
    question.question_text.includes("{");

  return (
    <AdminAppShell title={`Question Record [${question.id}]`}>
      <div className="space-y-6 max-w-4xl mx-auto">
        {/* Back Link */}
        <Link
          to="/admin/questions"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Question Bank
        </Link>

        {/* Top Header Card */}
        <Card className="p-6 bg-gradient-to-r from-slate-900 via-slate-900 to-rose-950/30 border border-slate-800 space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <Badge variant={question.status === "PUBLISHED" ? "success" : "neutral"}>
                  {question.status}
                </Badge>
                <Badge variant={question.type === "MSQ" ? "warning" : question.type === "NAT" ? "info" : "brand"}>
                  {question.type}
                </Badge>
                <Badge variant={question.difficulty === "HARD" ? "error" : "warning"}>
                  {question.difficulty}
                </Badge>
              </div>
              <h1 className="text-xl font-bold text-white font-mono">{question.id}</h1>
            </div>

            {/* Lifecycle Action Buttons */}
            <div className="flex items-center gap-2">
              {question.status !== "PUBLISHED" && (
                <Button
                  variant="primary"
                  size="sm"
                  isLoading={publishMutation.isPending}
                  leftIcon={<CheckCircle className="w-3.5 h-3.5" />}
                  onClick={() => publishMutation.mutate()}
                >
                  Publish
                </Button>
              )}
              {question.status === "PUBLISHED" && (
                <Button
                  variant="outline"
                  size="sm"
                  isLoading={unpublishMutation.isPending}
                  leftIcon={<XCircle className="w-3.5 h-3.5" />}
                  onClick={() => unpublishMutation.mutate()}
                >
                  Unpublish
                </Button>
              )}
              {question.status !== "ARCHIVED" && (
                <Button
                  variant="danger"
                  size="sm"
                  isLoading={archiveMutation.isPending}
                  leftIcon={<Archive className="w-3.5 h-3.5" />}
                  onClick={() => archiveMutation.mutate()}
                >
                  Archive
                </Button>
              )}
            </div>
          </div>
        </Card>

        {/* Question Prompt */}
        <Card className="p-6 space-y-4">
          <CardHeader>
            <CardTitle className="text-sm font-bold text-slate-300 uppercase tracking-wider">
              Question Statement / Code Prompt
            </CardTitle>
          </CardHeader>

          {isCCode ? (
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs md:text-sm text-emerald-300 overflow-x-auto whitespace-pre leading-relaxed shadow-inner">
              {question.question_text}
            </div>
          ) : (
            <p className="text-sm md:text-base font-medium text-slate-100 leading-relaxed">
              {question.question_text}
            </p>
          )}
        </Card>

        {/* Options & Answer Key */}
        <Card className="p-6 space-y-4">
          <CardHeader>
            <CardTitle className="text-sm font-bold text-slate-300 uppercase tracking-wider">
              Options & Answer Key
            </CardTitle>
          </CardHeader>

          {question.options && typeof question.options === "object" ? (
            <div className="space-y-2">
              {Object.entries(question.options).map(([k, v]) => (
                <div
                  key={k}
                  className={`p-3 rounded-lg border flex items-center justify-between text-xs ${
                    question.correct_answer?.includes(k)
                      ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-300 font-bold"
                      : "bg-slate-900/60 border-slate-800 text-slate-300"
                  }`}
                >
                  <span>
                    <span className="font-mono text-slate-400 mr-2">[{k}]</span> {String(v)}
                  </span>
                  {question.correct_answer?.includes(k) && (
                    <Badge variant="success">Correct Key</Badge>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs">
              <span className="text-slate-400">Numerical Target Answer: </span>
              <span className="font-bold font-mono text-emerald-400">{question.correct_answer}</span>
            </div>
          )}
        </Card>

        {/* Solution Explanation */}
        <Card className="p-6 space-y-3">
          <CardHeader>
            <CardTitle className="text-sm font-bold text-brand-400 uppercase tracking-wider">
              Official Solution Explanation
            </CardTitle>
          </CardHeader>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300 leading-relaxed font-mono whitespace-pre-wrap">
            {question.explanation || "No explanation attached to this record."}
          </div>
        </Card>
      </div>
    </AdminAppShell>
  );
};
