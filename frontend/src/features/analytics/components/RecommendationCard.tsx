import React from "react";
import { Link } from "react-router-dom";
import { PrescriptiveRecommendation } from "../../../types";
import { Badge } from "../../../components/ui/Badge";
import { Button } from "../../../components/ui/Button";
import { ArrowRight, Sparkles } from "lucide-react";

interface RecommendationCardProps {
  recommendation: PrescriptiveRecommendation;
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({ recommendation }) => {
  return (
    <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/60 hover:border-slate-700 transition-colors flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div className="space-y-1.5">
        <div className="flex items-center gap-2 flex-wrap">
          <Badge variant="brand" className="flex items-center gap-1">
            <Sparkles className="w-3 h-3" /> Priority #{recommendation.priority_rank}
          </Badge>
          <h5 className="font-bold text-slate-100 text-sm">{recommendation.topic_name}</h5>
          <Badge variant="neutral">{recommendation.subject_name}</Badge>
          <Badge variant={recommendation.accuracy < 50 ? "error" : "warning"}>
            Accuracy: {recommendation.accuracy}%
          </Badge>
        </div>
        <p className="text-xs text-slate-300 font-medium">{recommendation.recommended_action}</p>
        <p className="text-[11px] text-slate-400">{recommendation.explanation_reason}</p>
      </div>

      <Link to={`/quizzes?topic_id=${recommendation.topic_id}`} className="shrink-0">
        <Button variant="primary" size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
          Practice Topic
        </Button>
      </Link>
    </div>
  );
};
