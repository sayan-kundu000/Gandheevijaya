import React from "react";
import { Card } from "../../../components/ui/Card";

interface QuestionPaletteProps {
  questionsCount: number;
  currentIndex: number;
  userAnswers: Record<string, string>;
  markedQuestions: Record<string, boolean>;
  getQuestionId: (index: number) => string;
  onSelectQuestion: (index: number) => void;
}

export const QuestionPalette: React.FC<QuestionPaletteProps> = ({
  questionsCount,
  currentIndex,
  userAnswers,
  markedQuestions,
  getQuestionId,
  onSelectQuestion,
}) => {
  let answeredCount = 0;
  let markedCount = 0;

  for (let i = 0; i < questionsCount; i++) {
    const qId = getQuestionId(i);
    if (userAnswers[qId]) answeredCount++;
    if (markedQuestions[qId]) markedCount++;
  }

  return (
    <Card className="p-4 space-y-4">
      <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
        Question Palette
      </h4>

      <div className="grid grid-cols-5 gap-2 max-h-72 overflow-y-auto pr-1">
        {Array.from({ length: questionsCount }).map((_, idx) => {
          const qId = getQuestionId(idx);
          const isCurrent = idx === currentIndex;
          const isAnswered = !!userAnswers[qId];
          const isMarked = !!markedQuestions[qId];

          let bgClass = "bg-slate-800 text-slate-400 border-slate-700";
          if (isAnswered && isMarked) {
            bgClass = "bg-purple-600 text-white border-purple-500";
          } else if (isAnswered) {
            bgClass = "bg-emerald-600 text-white border-emerald-500";
          } else if (isMarked) {
            bgClass = "bg-amber-500 text-slate-950 font-bold border-amber-400";
          }

          return (
            <button
              key={idx}
              onClick={() => onSelectQuestion(idx)}
              className={`h-9 rounded-lg font-mono text-xs font-semibold border flex items-center justify-center transition-all ${bgClass} ${
                isCurrent ? "ring-2 ring-brand-400 ring-offset-2 ring-offset-slate-900" : ""
              }`}
              aria-label={`Question ${idx + 1}`}
            >
              {idx + 1}
            </button>
          );
        })}
      </div>

      <div className="pt-3 border-t border-slate-800 space-y-2 text-[11px] text-slate-400">
        <div className="flex items-center justify-between">
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-emerald-600 inline-block" /> Answered
          </span>
          <span className="font-semibold text-slate-200">{answeredCount}</span>
        </div>

        <div className="flex items-center justify-between">
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-slate-800 border border-slate-700 inline-block" /> Unanswered
          </span>
          <span className="font-semibold text-slate-200">{questionsCount - answeredCount}</span>
        </div>

        <div className="flex items-center justify-between">
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded bg-amber-500 inline-block" /> Marked for Review
          </span>
          <span className="font-semibold text-slate-200">{markedCount}</span>
        </div>
      </div>
    </Card>
  );
};
