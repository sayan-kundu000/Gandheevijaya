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
import { Subject } from "../../types";
import { Layers, Plus, Search } from "lucide-react";

export const AdminSubjectsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [selectedExamId, setSelectedExamId] = useState<number | undefined>(undefined);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [search, setSearch] = useState("");

  // Form State
  const [examId, setExamId] = useState<number>(1);
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const { data: exams } = useQuery({
    queryKey: ["admin", "exams"],
    queryFn: taxonomyApi.getExams,
  });

  const {
    data: subjects,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["admin", "subjects", selectedExamId],
    queryFn: () => taxonomyApi.getSubjects(selectedExamId),
  });

  const createMutation = useMutation({
    mutationFn: () =>
      adminApi.createSubject({
        exam_id: examId,
        code: code.trim(),
        name: name.trim(),
        description: description.trim() || undefined,
        status: "ACTIVE",
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "subjects"] });
      queryClient.invalidateQueries({ queryKey: ["subjects"] });
      setIsModalOpen(false);
      setCode("");
      setName("");
      setDescription("");
    },
  });

  const filteredSubjects = subjects?.filter(
    (s) =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.code.toLowerCase().includes(search.toLowerCase())
  );

  const columns: Column<Subject>[] = [
    {
      key: "code",
      header: "Subject Code",
      cell: (row) => <Badge variant="neutral">{row.code}</Badge>,
    },
    {
      key: "name",
      header: "Subject Name",
      cell: (row) => <span className="font-bold text-slate-100">{row.name}</span>,
    },
    {
      key: "exam_name",
      header: "Parent Exam Stream",
      cell: (row) => <Badge variant="brand">{row.exam_name || "Exam #" + row.exam_id}</Badge>,
    },
    {
      key: "topics_count",
      header: "Topics Count",
      cell: (row) => <span className="text-slate-200 font-semibold">{row.topics_count ?? 0}</span>,
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
      <AdminAppShell title="Subject Management">
        <ErrorState onRetry={refetch} />
      </AdminAppShell>
    );
  }

  return (
    <AdminAppShell title="Subject Taxonomy Management">
      <div className="space-y-6">
        {/* Header Controls */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Layers className="w-5 h-5 text-emerald-400" />
              Subject Modules Taxonomy
            </h2>
            <p className="text-xs text-slate-400">
              Manage subject modules under examination streams (e.g., C Programming, DSA).
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Select
              value={selectedExamId ? String(selectedExamId) : ""}
              onChange={(e) => setSelectedExamId(e.target.value ? Number(e.target.value) : undefined)}
              className="w-48"
            >
              <option value="">All Exam Streams</option>
              {exams?.map((e) => (
                <option key={e.id} value={e.id}>
                  {e.name} ({e.code})
                </option>
              ))}
            </Select>

            <Input
              placeholder="Search subject..."
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
              Add Subject
            </Button>
          </div>
        </div>

        {/* Subject Table */}
        <Card className="p-6 space-y-4">
          <Table
            columns={columns}
            data={filteredSubjects || []}
            keyExtractor={(r) => r.id}
            isLoading={isLoading}
            emptyTitle="No Subjects Found"
            emptyDescription="Create a new subject module under an active exam category."
          />
        </Card>

        {/* Modal Form */}
        <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Register New Subject Module">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              createMutation.mutate();
            }}
            className="space-y-4"
          >
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Parent Exam Stream</label>
              <Select
                value={String(examId)}
                onChange={(e) => setExamId(Number(e.target.value))}
                required
              >
                {exams?.map((e) => (
                  <option key={e.id} value={e.id}>
                    {e.name} ({e.code})
                  </option>
                ))}
              </Select>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Subject Code (e.g. CPROG, DSA, QA)</label>
              <Input
                required
                placeholder="CPROG"
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Subject Name</label>
              <Input
                required
                placeholder="C Programming & Data Types"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Description</label>
              <Input
                placeholder="Core fundamentals of C syntax, pointers, and memory."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
              <Button type="button" variant="ghost" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" variant="primary" isLoading={createMutation.isPending}>
                Create Subject
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </AdminAppShell>
  );
};
