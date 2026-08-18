import React from "react";
import { AttemptQuestionItem, QuestionType } from "../../../types";
import { Checkbox } from "../../../components/ui/Checkbox";
import { Input } from "../../../components/ui/Input";
import { Button } from "../../../components/ui/Button";
import { Badge } from "../../../components/ui/Badge";
import { clsx } from "clsx";
import { Code, Check, X } from "lucide-react";

export interface QuestionRendererProps {
  question: AttemptQuestionItem;
  selectedAnswer: string | null;
  onSelectAnswer: (answerKey: string | null) => void;
  disabled?: boolean;
}

export const QuestionRenderer: React.FC<QuestionRendererProps> = ({
  question,
  selectedAnswer,
  onSelectAnswer,
  disabled = false,
}) => {
  // Extract options format (can be Array or Object or Null for NAT)
  const getOptionsList = (optionsPayload: any): { key: string; text: string }[] => {
    if (!optionsPayload) return [];
    if (Array.isArray(optionsPayload)) {
      return optionsPayload.map((val, idx) => ({
        key: String.fromCharCode(65 + idx),
        text: String(val),
      }));
    }
    if (typeof optionsPayload === "object") {
      return Object.entries(optionsPayload).map(([k, v]) => ({
        key: String(k),
        text: String(v),
      }));
    }
    return [];
  };

  const optionsList = getOptionsList(question.options);
  const isCPlusCode =
    question.question_text.includes("#include") ||
    question.question_text.includes("int main") ||
    question.question_text.includes("printf") ||
    question.question_text.includes("*ptr") ||
    question.question_text.includes("void");

  // MSQ multiple answers parser (e.g., comma separated or JSON string)
  const msqSelectedKeys = selectedAnswer ? selectedAnswer.split(",").map((s) => s.trim()) : [];

  const handleMsqToggle = (key: string) => {
    if (disabled) return;
    let next: string[];
    if (msqSelectedKeys.includes(key)) {
      next = msqSelectedKeys.filter((k) => k !== key);
    } else {
      next = [...msqSelectedKeys, key];
    }
    onSelectAnswer(next.length > 0 ? next.sort().join(",") : null);
  };

  return (
    <div className="space-y-6">
      {/* Question Header & Type Tag */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Badge variant={question.type === "MSQ" ? "warning" : question.type === "NAT" ? "info" : "brand"}>
            {question.type === "MSQ" ? "Multiple Select (MSQ)" : question.type === "NAT" ? "Numerical (NAT)" : "Multiple Choice (MCQ)"}
          </Badge>
          <span className="text-xs font-semibold text-slate-400">
            +{question.marks} Marks {question.negative_marks > 0 && `| -${question.negative_marks} Penalty`}
          </span>
        </div>
      </div>

      {/* Question Text / Code Block */}
      <div className="space-y-3">
        {isCPlusCode || question.question_text.includes("\n") ? (
          <div className="space-y-3">
            <p className="text-sm md:text-base font-medium text-slate-200 leading-relaxed">
              {question.question_text.split(/```/)[0]}
            </p>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs md:text-sm text-emerald-300 overflow-x-auto whitespace-pre leading-relaxed shadow-inner">
              {question.question_text.includes("```")
                ? question.question_text.split(/```/)[1]?.replace(/^(c|cpp|python)\n/, "")
                : question.question_text}
            </div>
          </div>
        ) : (
          <p className="text-sm md:text-base font-medium text-slate-100 leading-relaxed">
            {question.question_text}
          </p>
        )}
      </div>

      {/* Options Rendering */}
      {question.type === "NAT" ? (
        /* Numerical Input System */
        <div className="space-y-3 max-w-md pt-2">
          <label className="text-xs font-semibold text-slate-400 block">
            Enter numerical answer value:
          </label>
          <div className="flex items-center gap-3">
            <Input
              type="number"
              step="any"
              placeholder="e.g. 42 or 3.14"
              value={selectedAnswer || ""}
              disabled={disabled}
              onChange={(e) => onSelectAnswer(e.target.value ? e.target.value : null)}
              className="font-mono text-base"
            />
            {selectedAnswer && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onSelectAnswer(null)}
                disabled={disabled}
                className="text-slate-400 hover:text-rose-400"
              >
                Clear
              </Button>
            )}
          </div>
        </div>
      ) : question.type === "MSQ" ? (
        /* MSQ Multi-Select Checkboxes */
        <div className="space-y-3 pt-2">
          <p className="text-xs text-amber-400/90 font-medium">
            Select one or more correct options.
          </p>
          {optionsList.map((opt, idx) => {
            const isChecked = msqSelectedKeys.includes(opt.key);
            return (
              <div
                key={opt.key}
                onClick={() => handleMsqToggle(opt.key)}
                className={clsx(
                  "p-4 rounded-xl border cursor-pointer transition-all flex items-center gap-3",
                  isChecked
                    ? "border-amber-500 bg-amber-950/20 ring-1 ring-amber-500/40"
                    : "border-slate-800 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-800/40",
                  disabled && "opacity-60 cursor-not-allowed"
                )}
              >
                <div
                  className={clsx(
                    "w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs shrink-0",
                    isChecked
                      ? "bg-amber-500 text-slate-950"
                      : "bg-slate-800 text-slate-400 border border-slate-700"
                  )}
                >
                  {opt.key}
                </div>
                <span className="text-sm font-medium text-slate-200 flex-1">{opt.text}</span>
                <span className="text-xs text-slate-500 font-mono">[{idx + 1}]</span>
              </div>
            );
          })}
        </div>
      ) : (
        /* Standard MCQ Single Choice Radio Options */
        <div className="space-y-3 pt-2">
          {optionsList.map((opt, idx) => {
            const isSelected = selectedAnswer === opt.key;
            return (
              <div
                key={opt.key}
                onClick={() => !disabled && onSelectAnswer(opt.key)}
                className={clsx(
                  "p-4 rounded-xl border cursor-pointer transition-all flex items-center gap-3",
                  isSelected
                    ? "border-brand-500 bg-brand-950/40 ring-1 ring-brand-500"
                    : "border-slate-800 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-800/40",
                  disabled && "opacity-60 cursor-not-allowed"
                )}
              >
                <div
                  className={clsx(
                    "w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs shrink-0",
                    isSelected
                      ? "bg-brand-600 text-white shadow-md shadow-brand-600/30"
                      : "bg-slate-800 text-slate-400 border border-slate-700"
                  )}
                >
                  {opt.key}
                </div>
                <span className="text-sm font-medium text-slate-200 flex-1">{opt.text}</span>
                <span className="text-xs text-slate-500 font-mono">[{idx + 1}]</span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
