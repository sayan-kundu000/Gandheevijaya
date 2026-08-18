import React from "react";
import { Link } from "react-router-dom";
import { Subject } from "../../../types";
import { Card } from "../../../components/ui/Card";
import { Badge } from "../../../components/ui/Badge";
import { Button } from "../../../components/ui/Button";
import { BookOpen, Layers, ArrowRight } from "lucide-react";

interface SubjectCardProps {
  subject: Subject;
}

export const SubjectCard: React.FC<SubjectCardProps> = ({ subject }) => {
  return (
    <Card className="p-5 flex flex-col justify-between">
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <h4 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-brand-400" />
            {subject.name}
          </h4>
          <Badge variant="info">{subject.code}</Badge>
        </div>
        <p className="text-xs text-slate-400">
          {subject.description || "Core subject module containing detailed topics and practice quizzes."}
        </p>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-1.5 text-xs text-slate-400">
          <Layers className="w-3.5 h-3.5" />
          <span>{subject.topics_count ?? 0} Topics</span>
        </div>

        <Link to={`/quizzes?subject_id=${subject.id}`}>
          <Button variant="outline" size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
            Practice Quizzes
          </Button>
        </Link>
      </div>
    </Card>
  );
};
