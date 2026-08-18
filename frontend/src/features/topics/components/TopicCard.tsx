import React from "react";
import { Link } from "react-router-dom";
import { Topic } from "../../../types";
import { Card } from "../../../components/ui/Card";
import { Badge } from "../../../components/ui/Badge";
import { Button } from "../../../components/ui/Button";
import { Layers, HelpCircle, ArrowRight } from "lucide-react";

interface TopicCardProps {
  topic: Topic;
}

export const TopicCard: React.FC<TopicCardProps> = ({ topic }) => {
  return (
    <Card className="p-4 flex flex-col justify-between">
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <h5 className="text-sm font-bold text-slate-100 flex items-center gap-2">
            <Layers className="w-4 h-4 text-emerald-400" />
            {topic.name}
          </h5>
          <Badge variant="neutral">{topic.code}</Badge>
        </div>
        <p className="text-xs text-slate-400 line-clamp-2">
          {topic.description || "Specific topic within syllabus for focused assessment."}
        </p>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
        <span className="text-xs text-slate-400 flex items-center gap-1">
          <HelpCircle className="w-3.5 h-3.5 text-slate-500" />
          {topic.questions_count ?? 0} Questions
        </span>

        <Link to={`/quizzes?topic_id=${topic.id}`}>
          <Button variant="ghost" size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
            Start Practice
          </Button>
        </Link>
      </div>
    </Card>
  );
};
