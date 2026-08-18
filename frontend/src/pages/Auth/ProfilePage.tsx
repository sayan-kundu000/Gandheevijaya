import React, { useState, useEffect } from "react";
import { AppShell } from "../../components/layout/AppShell";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../components/feedback/ToastProvider";
import { authApi } from "../../services/authApi";
import {
  User as UserIcon,
  Mail,
  GraduationCap,
  CheckCircle2,
  Save,
  BookOpen,
  Sparkles,
  Layers,
  Check,
} from "lucide-react";

export interface ExamOption {
  id: string;
  name: string;
  category: string;
  description: string;
  badge: string;
  badgeVariant: "brand" | "warning" | "success" | "info";
  subjectsCount: number;
}

export const AVAILABLE_EXAMS: ExamOption[] = [
  {
    id: "GATE_CS",
    name: "GATE CS (Computer Science & IT)",
    category: "Technical & Engineering",
    description:
      "Core CS curriculum: C Programming, Data Structures, Algorithms, Computer Networks, Databases, Operating System, Digital Logic, Computer Organization & Architecture, Theory Of Computation, Compiler Design, Calculus, Linear Algebra, Discrete Mathematics & Graph Theory, Probability & Statistics.",
    badge: "GATE CS",
    badgeVariant: "brand",
    subjectsCount: 14,
  },
  {
    id: "SSC_GK",
    name: "SSC CGL / CHSL (General Studies & Science)",
    category: "Government & SSC",
    description:
      "Comprehensive syllabus: Indian History, Polity, Geography, Indian Economy, Applied Physics, Chemistry, Biology, Current Affairs, Awards & Records.",
    badge: "SSC CGL",
    badgeVariant: "warning",
    subjectsCount: 23,
  },
  {
    id: "BANKING",
    name: "Banking & Finance (IBPS PO / SBI PO / Clerk)",
    category: "Banking & Financial Services",
    description:
      "Specialized banking modules: Banking Awareness, Financial System Architecture, Monetary Policies, RBI Regulations, Banking Terminology.",
    badge: "IBPS / SBI PO",
    badgeVariant: "success",
    subjectsCount: 1,
  },
  {
    id: "APTITUDE",
    name: "Quantitative Aptitude & Logical Reasoning",
    category: "General Aptitude",
    description:
      "Problem-solving foundational modules: Arithmetic, Algebra, Numerical Analysis, and Logical Reasoning.",
    badge: "Aptitude",
    badgeVariant: "info",
    subjectsCount: 2,
  },
];

export const ProfilePage: React.FC = () => {
  const { user, updateUser } = useAuth();
  const { success, error: showError } = useToast();

  const [fullName, setFullName] = useState(user?.full_name || "");
  const [selectedExams, setSelectedExams] = useState<string[]>(
    user?.target_exams && user.target_exams.length > 0 ? user.target_exams : ["GATE_CS"]
  );
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (user?.full_name) {
      setFullName(user.full_name);
    }
    if (user?.target_exams && user.target_exams.length > 0) {
      setSelectedExams(user.target_exams);
    }
  }, [user]);

  const toggleExam = (examId: string) => {
    setSelectedExams((prev) => {
      if (prev.includes(examId)) {
        if (prev.length === 1) {
          showError("You must select at least one target exam stream.");
          return prev;
        }
        return prev.filter((id) => id !== examId);
      } else {
        return [...prev, examId];
      }
    });
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedExams.length === 0) {
      showError("Please select at least one target exam.");
      return;
    }

    setIsSaving(true);
    try {
      const updated = await authApi.updateProfile({
        full_name: fullName.trim() || undefined,
        target_exams: selectedExams,
      });
      updateUser(updated);
      success("Profile & Target Exams successfully updated!");
    } catch (err: any) {
      showError(err.response?.data?.error?.message || "Failed to update profile.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <AppShell title="Student Profile & Exam Categories">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Profile Card Header */}
        <Card className="p-6 bg-gradient-to-r from-slate-900 via-slate-900 to-brand-950/40 border border-slate-800">
          <div className="flex flex-col sm:flex-row items-center gap-5">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-brand-600 to-accent-500 flex items-center justify-center text-2xl font-bold text-white shadow-xl ring-4 ring-slate-800">
              {user?.full_name?.charAt(0) || user?.email?.charAt(0).toUpperCase() || "S"}
            </div>

            <div className="space-y-1.5 text-center sm:text-left flex-1">
              <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
                <h1 className="text-xl font-bold text-white">{user?.full_name || "Student"}</h1>
                <Badge variant={user?.role === "ADMIN" ? "error" : "brand"}>{user?.role}</Badge>
                <Badge variant="success">Active Account</Badge>
              </div>
              <p className="text-xs text-slate-400 flex items-center justify-center sm:justify-start gap-1.5">
                <Mail className="w-3.5 h-3.5 text-slate-400" /> {user?.email}
              </p>
              <div className="flex flex-wrap items-center justify-center sm:justify-start gap-1.5 pt-1">
                <span className="text-[11px] text-slate-400 font-medium mr-1">Enrolled Streams:</span>
                {selectedExams.map((examId) => {
                  const examDef = AVAILABLE_EXAMS.find((e) => e.id === examId);
                  return (
                    <Badge key={examId} variant={examDef?.badgeVariant || "neutral"}>
                      {examDef?.badge || examId}
                    </Badge>
                  );
                })}
              </div>
            </div>
          </div>
        </Card>

        {/* Edit Profile & Target Exams Form */}
        <form onSubmit={handleSave} className="space-y-6">
          {/* Personal Information */}
          <Card className="p-6 space-y-4">
            <CardHeader className="p-0 pb-2">
              <CardTitle className="flex items-center gap-2 text-base">
                <UserIcon className="w-4 h-4 text-brand-400" />
                Personal Information
              </CardTitle>
            </CardHeader>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Input
                label="Full Name"
                placeholder="Your Full Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />

              <Input
                label="Email Address"
                value={user?.email || ""}
                disabled
                className="bg-slate-900/60 text-slate-400 cursor-not-allowed"
              />
            </div>
          </Card>

          {/* Target Exam Multi-Selection */}
          <Card className="p-6 space-y-5">
            <CardHeader className="p-0 pb-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <CardTitle className="flex items-center gap-2 text-base">
                    <GraduationCap className="w-5 h-5 text-brand-400" />
                    Target Exam Streams (Choose Multiple)
                  </CardTitle>
                  <p className="text-xs text-slate-400 mt-1">
                    Select all the examinations you are preparing for. Subject modules and practice drills will be customized based on your selected categories.
                  </p>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <Badge variant="brand">
                    {selectedExams.length} of {AVAILABLE_EXAMS.length} Selected
                  </Badge>
                </div>
              </div>
            </CardHeader>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
              {AVAILABLE_EXAMS.map((exam) => {
                const isSelected = selectedExams.includes(exam.id);
                return (
                  <div
                    key={exam.id}
                    onClick={() => toggleExam(exam.id)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all flex flex-col justify-between select-none relative ${
                      isSelected
                        ? "bg-brand-950/30 border-brand-500 ring-1 ring-brand-500/50 shadow-lg shadow-brand-950/50"
                        : "bg-slate-900/40 border-slate-800 hover:border-slate-700 hover:bg-slate-800/30"
                    }`}
                  >
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Badge variant={exam.badgeVariant}>{exam.badge}</Badge>
                          <span className="text-[11px] text-slate-400">{exam.category}</span>
                        </div>
                        <div
                          className={`w-5 h-5 rounded-md flex items-center justify-center transition-colors border ${
                            isSelected
                              ? "bg-brand-600 border-brand-500 text-white"
                              : "border-slate-700 bg-slate-800 text-transparent"
                          }`}
                        >
                          <Check className="w-3.5 h-3.5 stroke-[3]" />
                        </div>
                      </div>

                      <h3 className={`text-sm font-bold transition-colors ${isSelected ? "text-white" : "text-slate-200"}`}>
                        {exam.name}
                      </h3>

                      <p className="text-xs text-slate-400 leading-relaxed">
                        {exam.description}
                      </p>
                    </div>

                    <div className="pt-3 mt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
                      <span className="flex items-center gap-1">
                        <Layers className="w-3.5 h-3.5 text-slate-400" />
                        {exam.subjectsCount} Specialized Subjects
                      </span>
                      <span className={`font-semibold ${isSelected ? "text-brand-400" : "text-slate-500"}`}>
                        {isSelected ? "Enrolled" : "Click to select"}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>

          {/* Action Bar */}
          <div className="flex justify-end items-center gap-3">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              isLoading={isSaving}
              leftIcon={<Save className="w-4 h-4" />}
            >
              Save Profile & Exam Preferences
            </Button>
          </div>
        </form>
      </div>
    </AppShell>
  );
};
