import React from "react";
import { Exam } from "../../../types";
import { Card } from "../../../components/ui/Card";
import { Badge } from "../../../components/ui/Badge";
import { GraduationCap, BookOpen } from "lucide-react";

interface ExamCardProps {
  exam: Exam;
  isSelected?: boolean;
  onSelect: (examId: number) => void;
}

export const ExamCard: React.FC<ExamCardProps> = ({ exam, isSelected = false, onSelect }) => {
  return (
    <Card
      onClick={() => onSelect(exam.id)}
      className={`cursor-pointer transition-all p-5 flex flex-col justify-between ${
        isSelected
          ? "border-brand-500 bg-brand-950/20 ring-1 ring-brand-500"
          : "hover:border-slate-700"
      }`}
    >
      <div>
        <div className="flex items-center justify-between mb-2">
          <Badge variant={exam.code === "GATE_CS" ? "brand" : "neutral"}>{exam.code}</Badge>
          <GraduationCap className="w-5 h-5 text-slate-400" />
        </div>
        <h4 className="text-base font-bold text-slate-100 mb-1">{exam.name}</h4>
        <p className="text-xs text-slate-400 line-clamp-2">
          {exam.description || "Comprehensive examination stream syllabus and question bank assessments."}
        </p>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
        <span className="flex items-center gap-1.5">
          <BookOpen className="w-3.5 h-3.5 text-brand-400" />
          {exam.subjects_count ?? 0} Subjects
        </span>
        <Badge variant={exam.status === "ACTIVE" ? "success" : "neutral"}>{exam.status}</Badge>
      </div>
    </Card>
  );
};
