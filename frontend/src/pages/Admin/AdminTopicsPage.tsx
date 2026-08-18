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
import { taxonomyApi } from "../../services/taxonomyApi";
import { adminApi } from "../../services/adminApi";
import { Topic } from "../../types";
import { Tag, Plus, Search } from "lucide-react";

export const AdminTopicsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [selectedSubjectId, setSelectedSubjectId] = useState<number | undefined>(undefined);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [search, setSearch] = useState("");

  // Form State
  const [subjectId, setSubjectId] = useState<number>(1);
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const { data: subjects } = useQuery({
    queryKey: ["admin", "subjects"],
    queryFn: () => taxonomyApi.getSubjects(),
  });

  const {
    data: topics,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["admin", "topics", selectedSubjectId],
    queryFn: () => taxonomyApi.getTopics(selectedSubjectId),
  });

  const createMutation = useMutation({
    mutationFn: () =>
      adminApi.createTopic({
        subject_id: subjectId,
        code: code.trim() || undefined,
        name: name.trim(),
        description: description.trim() || undefined,
        status: "ACTIVE",
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "topics"] });
      queryClient.invalidateQueries({ queryKey: ["topics"] });
      setIsModalOpen(false);
      setCode("");
      setName("");
      setDescription("");
    },
  });

  const filteredTopics = topics?.filter(
    (t) =>
      t.name.toLowerCase().includes(search.toLowerCase()) ||
      (t.code && t.code.toLowerCase().includes(search.toLowerCase()))
  );

  const columns: Column<Topic>[] = [
    {
      key: "code",
      header: "Topic Code",
      cell: (row) => <Badge variant="neutral">{row.code || `TOPIC-${row.id}`}</Badge>,
    },
    {
      key: "name",
      header: "Topic Name",
      cell: (row) => <span className="font-bold text-slate-100">{row.name}</span>,
    },
    {
      key: "subject_name",
      header: "Parent Subject",
      cell: (row) => <Badge variant="brand">{row.subject_name || "Subject #" + row.subject_id}</Badge>,
    },
    {
      key: "questions_count",
      header: "Question Count",
      cell: (row) => <span className="text-slate-200 font-semibold">{row.questions_count ?? 0}</span>,
    },
    {
      key: "status",
      header: "Status",
      cell: (row) => (
        <Badge variant={row.status === "ACTIVE" ? "success" : "neutral"}>{row.status}</Badge>
      ),
    },
  ];

  if (error) {
    return (
      <AdminAppShell title="Topic Management">
        <ErrorState onRetry={refetch} />
      </AdminAppShell>
    );
  }

  return (
    <AdminAppShell title="Topic Concept Taxonomy">
      <div className="space-y-6">
        {/* Header Controls */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Tag className="w-5 h-5 text-amber-400" />
              Syllabus Topics & Concepts
            </h2>
            <p className="text-xs text-slate-400">
              Manage specific subject topics (e.g., Pointers, Trees, Recursion, Arrays).
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Select
              value={selectedSubjectId ? String(selectedSubjectId) : ""}
              onChange={(e) => setSelectedSubjectId(e.target.value ? Number(e.target.value) : undefined)}
              className="w-48"
            >
              <option value="">All Subjects</option>
              {subjects?.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.code})
                </option>
              ))}
            </Select>

            <Input
              placeholder="Search topic..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-48"
            />

            <Button
              variant="primary"
              size="sm"
              leftIcon={<Plus className="w-4 h-4" />}
              onClick={() => setIsModalOpen(true)}
            >
              Add Topic
            </Button>
          </div>
        </div>

        {/* Topic Table */}
        <Card className="p-6 space-y-4">
          <Table
            columns={columns}
            data={filteredTopics || []}
            keyExtractor={(r) => r.id}
            isLoading={isLoading}
            emptyTitle="No Topics Found"
            emptyDescription="Create topics under subject modules to classify practice questions."
          />
        </Card>

        {/* Modal Form */}
        <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Register New Topic">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              createMutation.mutate();
            }}
            className="space-y-4"
          >
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Parent Subject Module</label>
              <Select
                value={String(subjectId)}
                onChange={(e) => setSubjectId(Number(e.target.value))}
                required
              >
                {subjects?.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.code})
                  </option>
                ))}
              </Select>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Topic Code (Optional, e.g. PTR, RECUR)</label>
              <Input
                placeholder="PTR"
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Topic Name</label>
              <Input
                required
                placeholder="Pointers & Memory Allocation"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Description</label>
              <Input
                placeholder="Pointer arithmetic, stack vs heap allocation, function pointers."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
              <Button type="button" variant="ghost" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" variant="primary" isLoading={createMutation.isPending}>
                Create Topic
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </AdminAppShell>
  );
};
