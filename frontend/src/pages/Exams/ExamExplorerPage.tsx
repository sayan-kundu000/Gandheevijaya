import React, { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { AppShell } from "../../components/layout/AppShell";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { Skeleton } from "../../components/ui/Skeleton";
import { ErrorState } from "../../components/ui/ErrorState";
import { taxonomyApi } from "../../services/taxonomyApi";
import { useAuth } from "../../context/AuthContext";
import {
  GraduationCap,
  BookOpen,
  Layers,
  ArrowRight,
  Sparkles,
  Search,
  Filter,
  CheckCircle2,
} from "lucide-react";

export const ExamExplorerPage: React.FC = () => {
  const { user } = useAuth();
  const [selectedExamId, setSelectedExamId] = useState<number | undefined>(undefined);
  const [searchQuery, setSearchQuery] = useState("");

  const {
    data: exams,
    isLoading: isExamsLoading,
    error: examsError,
  } = useQuery({
    queryKey: ["exams"],
    queryFn: taxonomyApi.getExams,
  });

  // Determine effective exam ID (default to first target exam or first available exam)
  const activeExamId = useMemo(() => {
    if (selectedExamId !== undefined) {
      return selectedExamId;
    }
    if (exams && exams.length > 0) {
      // Prioritize student's enrolled target exams
      if (user?.target_exams && user.target_exams.length > 0) {
        const primaryTarget = user.target_exams[0];
        const match = exams.find(
          (e) =>
            e.code === primaryTarget ||
            (primaryTarget === "SSC" && e.code === "SSC_GK") ||
            (primaryTarget === "IBPS_PO" && e.code === "BANKING")
        );
        if (match) return match.id;
      }
      // Fallback to GATE_CS or first exam
      const gateMatch = exams.find((e) => e.code === "GATE_CS");
      return gateMatch ? gateMatch.id : exams[0].id;
    }
    return undefined;
  }, [selectedExamId, exams, user]);

  const {
    data: subjects,
    isLoading: isSubjectsLoading,
  } = useQuery({
    queryKey: ["subjects", activeExamId],
    queryFn: () => taxonomyApi.getSubjects(activeExamId),
    enabled: activeExamId !== undefined,
  });

  const currentExam = exams?.find((e) => e.id === activeExamId);

  const filteredSubjects = useMemo(() => {
    if (!subjects) return [];
    if (!searchQuery.trim()) return subjects;
    const q = searchQuery.toLowerCase().trim();
    return subjects.filter(
      (s) =>
        s.name.toLowerCase().includes(q) ||
        s.code.toLowerCase().includes(q) ||
        (s.description && s.description.toLowerCase().includes(q))
    );
  }, [subjects, searchQuery]);

  if (examsError) {
    return (
      <AppShell title="Exams & Subjects">
        <ErrorState message="Failed to load examination streams." />
      </AppShell>
    );
  }

  return (
    <AppShell title="Exam & Subject Curriculum Explorer">
      <div className="space-y-8">
        {/* Exam Category Stream Selector */}
        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <GraduationCap className="w-5 h-5 text-brand-400" />
                Select Examination Stream
              </h2>
              <p className="text-xs text-slate-400">
                Choose an exam stream below to view its specific subjects, topics, and practice tests.
              </p>
            </div>

            {user?.target_exams && user.target_exams.length > 0 && (
              <div className="flex items-center gap-1.5 text-xs text-slate-400 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
                <Sparkles className="w-3.5 h-3.5 text-brand-400" />
                <span>Your Enrolled Streams:</span>
                <span className="font-semibold text-slate-200">
                  {user.target_exams.join(", ")}
                </span>
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
            {isExamsLoading ? (
              <>
                <Skeleton className="h-32 w-full" />
                <Skeleton className="h-32 w-full" />
                <Skeleton className="h-32 w-full" />
                <Skeleton className="h-32 w-full" />
              </>
            ) : (
              exams?.map((exam) => {
                const isSelected = activeExamId === exam.id;
                const isTarget =
                  user?.target_exams?.includes(exam.code) ||
                  (exam.code === "SSC_GK" && user?.target_exams?.includes("SSC")) ||
                  (exam.code === "BANKING" && user?.target_exams?.includes("IBPS_PO"));

                return (
                  <Card
                    key={exam.id}
                    onClick={() => setSelectedExamId(exam.id)}
                    className={`cursor-pointer transition-all p-4 flex flex-col justify-between select-none relative ${
                      isSelected
                        ? "border-brand-500 bg-brand-950/30 ring-1 ring-brand-500 shadow-lg shadow-brand-950/40"
                        : "hover:border-slate-700 bg-slate-900/50 hover:bg-slate-800/40"
                    }`}
                  >
                    <div className="space-y-1.5">
                      <div className="flex items-center justify-between mb-1">
                        <Badge
                          variant={
                            exam.code === "GATE_CS"
                              ? "brand"
                              : exam.code === "SSC_GK"
                              ? "warning"
                              : exam.code === "BANKING"
                              ? "success"
                              : "info"
                          }
                        >
                          {exam.code}
                        </Badge>
                        {isTarget && (
                          <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                            <CheckCircle2 className="w-3 h-3" /> Target
                          </span>
                        )}
                      </div>
                      <h3 className={`text-sm font-bold ${isSelected ? "text-white" : "text-slate-200"}`}>
                        {exam.name}
                      </h3>
                      <p className="text-xs text-slate-400 line-clamp-2">
                        {exam.description || "Comprehensive syllabus modules and practice drills."}
                      </p>
                    </div>

                    <div className="pt-3 mt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                      <span className="text-slate-400 text-[11px] flex items-center gap-1">
                        <Layers className="w-3 h-3 text-slate-400" />
                        {exam.subjects_count ?? (exam.code === "GATE_CS" ? 14 : exam.code === "SSC_GK" ? 23 : exam.code === "BANKING" ? 1 : 2)} Subjects
                      </span>
                      <span className={`text-[11px] font-semibold ${isSelected ? "text-brand-400" : "text-slate-500"}`}>
                        {isSelected ? "Active View" : "Select"}
                      </span>
                    </div>
                  </Card>
                );
              })
            )}
          </div>
        </div>

        {/* Selected Exam Banner & Subjects Listing */}
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-brand-950/40 border border-slate-800">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <Badge variant="brand">{currentExam?.code || "EXAM"}</Badge>
                <h3 className="text-lg font-bold text-white tracking-tight">
                  {currentExam ? `${currentExam.name} - Subjects` : "Available Subjects"}
                </h3>
              </div>
              <p className="text-xs text-slate-400 max-w-xl">
                Showing exclusively {filteredSubjects.length} subjects associated with {currentExam?.name || "this exam stream"}.
              </p>
            </div>

            {/* Search filter */}
            <div className="relative w-full sm:w-72">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search subject or code..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-brand-500 transition-colors"
              />
            </div>
          </div>

          {/* Subjects Grid */}
          {isSubjectsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <Skeleton className="h-36 w-full" />
              <Skeleton className="h-36 w-full" />
              <Skeleton className="h-36 w-full" />
            </div>
          ) : filteredSubjects && filteredSubjects.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredSubjects.map((subj) => (
                <Card
                  key={subj.id}
                  className="p-5 flex flex-col justify-between hover:border-brand-500/40 transition-all group bg-slate-900/60"
                >
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Badge variant="neutral">{subj.code}</Badge>
                      <span className="text-[11px] text-slate-400 font-medium">
                        {subj.topics_count || "Multiple"} Topics
                      </span>
                    </div>

                    <h4 className="text-base font-bold text-slate-100 group-hover:text-brand-300 transition-colors">
                      {subj.name}
                    </h4>

                    <p className="text-xs text-slate-400 line-clamp-2">
                      {subj.description || "Master core concepts, problem-solving techniques, and exam patterns."}
                    </p>
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between gap-2">
                    <Link to={`/subjects/${subj.id}`}>
                      <Button variant="secondary" size="sm">
                        View Topics
                      </Button>
                    </Link>

                    <Link to={`/quizzes?subject_id=${subj.id}`}>
                      <Button variant="primary" size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
                        Practice Tests
                      </Button>
                    </Link>
                  </div>
                </Card>
              ))}
            </div>
          ) : (
            <Card className="p-8 text-center space-y-2 border-slate-800">
              <BookOpen className="w-8 h-8 text-slate-600 mx-auto" />
              <h4 className="text-sm font-bold text-slate-300">No subjects found</h4>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                {searchQuery
                  ? `No subjects match the search query "${searchQuery}".`
                  : "No subjects are currently listed under this examination category."}
              </p>
            </Card>
          )}
        </div>
      </div>
    </AppShell>
  );
};
