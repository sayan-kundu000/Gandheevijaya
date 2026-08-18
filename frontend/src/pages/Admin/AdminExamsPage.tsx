import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AdminAppShell } from "../../components/layout/AdminAppShell";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import { Modal } from "../../components/ui/Modal";
import { Table, Column } from "../../components/ui/Table";
import { ErrorState } from "../../components/ui/ErrorState";
import { taxonomyApi } from "../../services/taxonomyApi";
import { adminApi } from "../../services/adminApi";
import { Exam } from "../../types";
import { GraduationCap, Plus, Layers, Search } from "lucide-react";

export const AdminExamsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [search, setSearch] = useState("");

  // Form State
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const {
    data: exams,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["admin", "exams"],
    queryFn: taxonomyApi.getExams,
  });

  const createMutation = useMutation({
    mutationFn: () =>
      adminApi.createExam({
        category_id: 1,
        code: code.trim(),
        name: name.trim(),
        description: description.trim() || undefined,
        status: "ACTIVE",
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "exams"] });
      queryClient.invalidateQueries({ queryKey: ["exams"] });
      setIsModalOpen(false);
      setCode("");
      setName("");
      setDescription("");
    },
  });

  const filteredExams = exams?.filter(
    (e) =>
      e.name.toLowerCase().includes(search.toLowerCase()) ||
      e.code.toLowerCase().includes(search.toLowerCase())
  );

  const columns: Column<Exam>[] = [
    {
      key: "code",
      header: "Exam Code",
      cell: (row) => <Badge variant="brand">{row.code}</Badge>,
    },
    {
      key: "name",
      header: "Exam Stream Name",
      cell: (row) => <span className="font-bold text-slate-100">{row.name}</span>,
    },
    {
      key: "description",
      header: "Description",
      cell: (row) => <span className="text-slate-400 text-xs line-clamp-1">{row.description || "N/A"}</span>,
    },
    {
      key: "subjects_count",
      header: "Subjects Count",
      cell: (row) => <span className="text-slate-200 font-semibold">{row.subjects_count ?? 0}</span>,
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
      <AdminAppShell title="Exam Taxonomy">
        <ErrorState onRetry={refetch} />
      </AdminAppShell>
    );
  }

  return (
    <AdminAppShell title="Exam Taxonomy Management">
      <div className="space-y-6">
        {/* Header Controls */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <GraduationCap className="w-5 h-5 text-brand-400" />
              Examination Categories & Streams
            </h2>
            <p className="text-xs text-slate-400">
              Manage multi-exam streams (GATE CS, SSC, Banking) backed by dynamic PostgreSQL taxonomy.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Input
              placeholder="Search exam code or name..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-64"
            />
            <Button
              variant="primary"
              size="sm"
              leftIcon={<Plus className="w-4 h-4" />}
              onClick={() => setIsModalOpen(true)}
            >
              Add Exam Stream
            </Button>
          </div>
        </div>

        {/* Exam Table */}
        <Card className="p-6 space-y-4">
          <Table
            columns={columns}
            data={filteredExams || []}
            keyExtractor={(r) => r.id}
            isLoading={isLoading}
            emptyTitle="No Exams Configured"
            emptyDescription="Click 'Add Exam Stream' to create your first examination stream."
          />
        </Card>

        {/* Modal Form to Create Exam */}
        <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Register New Exam Category">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              createMutation.mutate();
            }}
            className="space-y-4"
          >
            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Exam Code (e.g. GATE_CS, SSC_CGL, BANK_PO)</label>
              <Input
                required
                placeholder="GATE_CS"
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Full Stream Name</label>
              <Input
                required
                placeholder="GATE Computer Science & Engineering"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-slate-300">Description</label>
              <Input
                placeholder="Comprehensive exam syllabus for engineering graduates."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
              <Button type="button" variant="ghost" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" variant="primary" isLoading={createMutation.isPending}>
                Create Exam Stream
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </AdminAppShell>
  );
};
