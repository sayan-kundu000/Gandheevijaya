import React from "react";
import { Link } from "react-router-dom";
import { Quiz } from "../../../types";
import { Card } from "../../../components/ui/Card";
import { Badge } from "../../../components/ui/Badge";
import { Button } from "../../../components/ui/Button";
import { Clock, HelpCircle, Award, Play } from "lucide-react";

interface QuizCardProps {
  quiz: Quiz;
}

export const QuizCard: React.FC<QuizCardProps> = ({ quiz }) => {
  return (
    <Card className="p-5 flex flex-col justify-between hover:border-slate-700 transition-all">
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <Badge variant="brand">{quiz.subject_name || "Assessment"}</Badge>
          {quiz.topic_name && <Badge variant="neutral">{quiz.topic_name}</Badge>}
        </div>

        <div>
          <h4 className="text-base font-bold text-slate-100 mb-1">{quiz.title}</h4>
          <p className="text-xs text-slate-400 line-clamp-2">
            {quiz.description || "Comprehensive timed examination quiz."}
          </p>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-slate-800 space-y-3">
        <div className="grid grid-cols-3 gap-2 text-center text-xs">
          <div className="p-2 rounded-lg bg-slate-800/60 border border-slate-800">
            <p className="text-[10px] text-slate-400">Questions</p>
            <p className="font-bold text-slate-200 flex items-center justify-center gap-1 mt-0.5">
              <HelpCircle className="w-3 h-3 text-brand-400" />
              {quiz.question_count ?? 0}
            </p>
          </div>

          <div className="p-2 rounded-lg bg-slate-800/60 border border-slate-800">
            <p className="text-[10px] text-slate-400">Duration</p>
            <p className="font-bold text-slate-200 flex items-center justify-center gap-1 mt-0.5">
              <Clock className="w-3 h-3 text-amber-400" />
              {quiz.duration_minutes} m
            </p>
          </div>

          <div className="p-2 rounded-lg bg-slate-800/60 border border-slate-800">
            <p className="text-[10px] text-slate-400">Pass</p>
            <p className="font-bold text-slate-200 flex items-center justify-center gap-1 mt-0.5">
              <Award className="w-3 h-3 text-emerald-400" />
              {quiz.pass_percentage}%
            </p>
          </div>
        </div>

        <Link to={`/quizzes/${quiz.id}`} className="block">
          <Button
            variant="primary"
            size="md"
            className="w-full justify-center"
            rightIcon={<Play className="w-4 h-4 fill-current" />}
          >
            Start Quiz
          </Button>
        </Link>
      </div>
    </Card>
  );
};
