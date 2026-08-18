import React, { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AdminAppShell } from "../../components/layout/AdminAppShell";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import { Select } from "../../components/ui/Select";
import { Pagination } from "../../components/ui/Pagination";
import { Modal } from "../../components/ui/Modal";
import { Table, Column } from "../../components/ui/Table";
import { ErrorState } from "../../components/ui/ErrorState";
import { adminApi } from "../../services/adminApi";
import { AdminUserItem, AdminUserDetailResponse } from "../../types";
import { Users, Search, UserCheck, UserX, Shield, Award } from "lucide-react";

export const AdminUserManagementPage: React.FC = () => {
  const queryClient = useQueryClient();

  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [roleFilter, setRoleFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");

  const [selectedUser, setSelectedUser] = useState<AdminUserDetailResponse | null>(null);
  const [userToToggle, setUserToToggle] = useState<AdminUserItem | null>(null);

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(handler);
  }, [search]);

  const {
    data: usersData,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["admin", "users", page, pageSize, roleFilter, statusFilter, debouncedSearch],
    queryFn: () =>
      adminApi.getUsers({
        page,
        page_size: pageSize,
        role: roleFilter || undefined,
        is_active: statusFilter === "active" ? true : statusFilter === "disabled" ? false : undefined,
        search: debouncedSearch || undefined,
      }),
  });

  const disableMutation = useMutation({
    mutationFn: (userId: string) => adminApi.disableUser(userId, "Admin action"),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
      setUserToToggle(null);
    },
  });

  const reactivateMutation = useMutation({
    mutationFn: (userId: string) => adminApi.reactivateUser(userId, "Admin action"),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "users"] });
      setUserToToggle(null);
    },
  });

  const inspectUser = async (userId: string) => {
    try {
      const data = await adminApi.getUserDetail(userId);
      setSelectedUser(data);
    } catch (e) {
      // Ignore
    }
  };

  const columns: Column<AdminUserItem>[] = [
    {
      key: "full_name",
      header: "User Name",
      cell: (row) => <span className="font-bold text-slate-100">{row.full_name}</span>,
    },
    {
      key: "email",
      header: "Email Address",
      cell: (row) => <span className="text-slate-400 font-mono text-xs">{row.email}</span>,
    },
    {
      key: "role",
      header: "Role",
      cell: (row) => <Badge variant={row.role === "ADMIN" ? "error" : "brand"}>{row.role}</Badge>,
    },
    {
      key: "target_exam",
      header: "Target Stream",
      cell: (row) => <span className="text-slate-300 text-xs">{row.target_exam || "GATE CS"}</span>,
    },
    {
      key: "is_active",
      header: "Account Status",
      cell: (row) => (
        <Badge variant={row.is_active ? "success" : "neutral"}>
          {row.is_active ? "Active" : "Disabled"}
        </Badge>
      ),
    },
    {
      key: "actions",
      header: "Actions",
      cell: (row) => (
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={() => inspectUser(row.id)}>
            Metrics
          </Button>

          {row.is_active ? (
            <Button variant="danger" size="sm" onClick={() => setUserToToggle(row)}>
              Disable
            </Button>
          ) : (
            <Button variant="primary" size="sm" onClick={() => setUserToToggle(row)}>
              Reactivate
            </Button>
          )}
        </div>
      ),
    },
  ];

  if (error) {
    return (
      <AdminAppShell title="User Directory">
        <ErrorState onRetry={refetch} />
      </AdminAppShell>
    );
  }

  const totalPages = Math.ceil((usersData?.total || 0) / pageSize);

  return (
    <AdminAppShell title="User Directory & Governance">
      <div className="space-y-6">
        {/* Header Controls */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Users className="w-5 h-5 text-brand-400" />
              User Account Directory & Governance
            </h2>
            <p className="text-xs text-slate-400">
              Directory listing of student and administrator accounts with status toggle protections.
            </p>
          </div>
        </div>

        {/* Filter Toolbar */}
        <Card className="p-4 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <Input
              placeholder="Search user name or email..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />

            <Select value={roleFilter} onChange={(e) => setRoleFilter(e.target.value)}>
              <option value="">All Roles (Student, Admin)</option>
              <option value="STUDENT">STUDENT</option>
              <option value="ADMIN">ADMIN</option>
            </Select>

            <Select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
              <option value="">All Account Statuses</option>
              <option value="active">Active Accounts</option>
              <option value="disabled">Disabled Accounts</option>
            </Select>
          </div>
        </Card>

        {/* Data Table */}
        <Card className="p-6 space-y-4">
          <Table
            columns={columns}
            data={usersData?.items || []}
            keyExtractor={(r) => r.id}
            isLoading={isLoading}
            emptyTitle="No Users Found"
            emptyDescription="No user accounts match the current query parameters."
          />

          {totalPages > 1 && (
            <div className="pt-4 border-t border-slate-800">
              <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
            </div>
          )}
        </Card>

        {/* User Account Detail Modal */}
        {selectedUser && (
          <Modal isOpen={!!selectedUser} onClose={() => setSelectedUser(null)} title={`User Metrics: ${selectedUser.user.full_name}`}>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3 p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs">
                <div>
                  <p className="text-slate-400">Email Address</p>
                  <p className="text-sm font-bold text-slate-100 font-mono">{selectedUser.user.email}</p>
                </div>
                <div>
                  <p className="text-slate-400">Account Role</p>
                  <p className="text-sm font-bold text-brand-400">{selectedUser.user.role}</p>
                </div>
                <div>
                  <p className="text-slate-400">Total Quiz Attempts</p>
                  <p className="text-sm font-bold text-slate-100">{selectedUser.user.total_attempts_count || 0}</p>
                </div>
                <div>
                  <p className="text-slate-400">Average Accuracy</p>
                  <p className="text-sm font-bold text-emerald-400">{selectedUser.user.average_accuracy || 0}%</p>
                </div>
              </div>

              <div className="space-y-2">
                <p className="text-xs font-bold text-slate-300">Recent Quiz Attempt Records:</p>
                {selectedUser.recent_attempts && selectedUser.recent_attempts.length > 0 ? (
                  <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                    {selectedUser.recent_attempts.map((att) => (
                      <div key={att.id} className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-xs flex justify-between">
                        <span>Quiz #{att.quiz_id}</span>
                        <span className="font-bold text-brand-400">{att.score} Marks</span>
                        <span className="text-emerald-400 font-bold">{att.accuracy}% Acc</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 py-3 text-center">No recent quiz attempts found.</p>
                )}
              </div>
            </div>
          </Modal>
        )}

        {/* Toggle Status Confirmation Modal */}
        {userToToggle && (
          <Modal isOpen={!!userToToggle} onClose={() => setUserToToggle(null)} title="Confirm Account Action">
            <div className="space-y-4">
              <p className="text-sm text-slate-300">
                Are you sure you want to {userToToggle.is_active ? "disable" : "reactivate"} the account for{" "}
                <span className="font-bold text-white">{userToToggle.full_name}</span> ({userToToggle.email})?
              </p>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
                <Button variant="ghost" onClick={() => setUserToToggle(null)}>
                  Cancel
                </Button>

                {userToToggle.is_active ? (
                  <Button
                    variant="danger"
                    isLoading={disableMutation.isPending}
                    onClick={() => disableMutation.mutate(userToToggle.id)}
                  >
                    Disable User Account
                  </Button>
                ) : (
                  <Button
                    variant="primary"
                    isLoading={reactivateMutation.isPending}
                    onClick={() => reactivateMutation.mutate(userToToggle.id)}
                  >
                    Reactivate Account
                  </Button>
                )}
              </div>
            </div>
          </Modal>
        )}
      </div>
    </AdminAppShell>
  );
};
