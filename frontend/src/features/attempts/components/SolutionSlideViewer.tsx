import React, { useState, useEffect } from "react";
import { QuestionSolutionItem } from "../../../types";
import { Card } from "../../../components/ui/Card";
import { Badge } from "../../../components/ui/Badge";
import { Button } from "../../../components/ui/Button";
import {
  CheckCircle2,
  XCircle,
  ChevronLeft,
  ChevronRight,
  BookOpen,
  HelpCircle,
  Filter,
  Check,
  X,
  AlertCircle,
  Lightbulb,
} from "lucide-react";

interface SolutionSlideViewerProps {
  solutions: QuestionSolutionItem[];
}

type FilterType = "ALL" | "INCORRECT" | "CORRECT" | "UNANSWERED";

function normalizeOptions(options: any): { key: string; label: string }[] {
  if (!options) return [];
  if (Array.isArray(options)) {
    return options.map((opt, idx) => {
      const key = String.fromCharCode(65 + idx); // A, B, C, D...
      if (typeof opt === "string") {
        return { key, label: opt };
      }
      if (opt && typeof opt === "object") {
        return {
          key: opt.key || opt.id || key,
          label: opt.text || opt.label || opt.value || JSON.stringify(opt),
        };
      }
      return { key, label: String(opt) };
    });
  }
  if (typeof options === "object") {
    return Object.entries(options).map(([key, val]) => ({
      key,
      label: typeof val === "string" ? val : JSON.stringify(val),
    }));
  }
  return [];
}

export const SolutionSlideViewer: React.FC<SolutionSlideViewerProps> = ({ solutions }) => {
  const [filter, setFilter] = useState<FilterType>("ALL");
  const [currentIndex, setCurrentIndex] = useState<number>(0);

  if (!solutions || solutions.length === 0) {
    return (
      <Card className="p-8 text-center text-slate-400">
        <HelpCircle className="w-12 h-12 mx-auto mb-3 text-slate-600" />
        <p>No detailed solutions available for this attempt.</p>
      </Card>
    );
  }

  // Helper to extract answer string safely
  const getUserAnswer = (sol: QuestionSolutionItem) => {
    return sol.user_answer ?? sol.selected_answer ?? null;
  };

  // Filter solutions according to selected tab
  const filteredSolutions = solutions.filter((sol) => {
    const ans = getUserAnswer(sol);
    const hasAnswered = ans !== null && ans !== "";
    if (filter === "CORRECT") return sol.is_correct;
    if (filter === "INCORRECT") return !sol.is_correct && hasAnswered;
    if (filter === "UNANSWERED") return !hasAnswered;
    return true;
  });

  // Keep index within bounds when filter changes
  useEffect(() => {
    if (currentIndex >= filteredSolutions.length) {
      setCurrentIndex(Math.max(0, filteredSolutions.length - 1));
    }
  }, [filter, filteredSolutions.length, currentIndex]);

  // Keyboard arrow keys navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "ArrowLeft") {
        setCurrentIndex((prev) => Math.max(0, prev - 1));
      } else if (e.key === "ArrowRight") {
        setCurrentIndex((prev) => Math.min(filteredSolutions.length - 1, prev + 1));
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [filteredSolutions.length]);

  const activeSolution = filteredSolutions[currentIndex] || solutions[0];
  const originalIndex = solutions.findIndex((s) => s.question_id === activeSolution.question_id);

  const optionsList = normalizeOptions(activeSolution.options);

  const isCCode =
    activeSolution.question_text.includes("#include") ||
    activeSolution.question_text.includes("int main") ||
    activeSolution.question_text.includes("{");

  const activeUserAnswer = getUserAnswer(activeSolution);
  const activeHasAnswered = activeUserAnswer !== null && activeUserAnswer !== "";

  // Helper to check option status
  const checkOptionStatus = (optKey: string, optLabel: string) => {
    const userAns = (activeUserAnswer || "").trim();
    const correctAns = (activeSolution.correct_answer || "").trim();

    const isUserChoice =
      userAns !== "" &&
      (userAns === optKey ||
        userAns.split(",").map((s) => s.trim()).includes(optKey) ||
        userAns === optLabel);

    const isRightChoice =
      correctAns !== "" &&
      (correctAns === optKey ||
        correctAns.split(",").map((s) => s.trim()).includes(optKey) ||
        correctAns === optLabel);

    return { isUserChoice, isRightChoice };
  };

  return (
    <div className="space-y-6">
      {/* Top Controls Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-xl bg-slate-900 border border-slate-800 shadow-md">
        {/* Filter Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0">
          <span className="text-xs font-semibold text-slate-400 mr-2 flex items-center gap-1">
            <Filter className="w-3.5 h-3.5 text-brand-400" /> Filter:
          </span>
          <button
            onClick={() => setFilter("ALL")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              filter === "ALL"
                ? "bg-brand-500 text-white font-bold shadow-sm"
                : "bg-slate-800 text-slate-300 hover:bg-slate-700"
            }`}
          >
            All ({solutions.length})
          </button>
          <button
            onClick={() => setFilter("INCORRECT")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              filter === "INCORRECT"
                ? "bg-rose-600 text-white font-bold shadow-sm"
                : "bg-slate-800 text-slate-300 hover:bg-slate-700"
            }`}
          >
            Incorrect ({solutions.filter((s) => !s.is_correct && getUserAnswer(s)).length})
          </button>
          <button
            onClick={() => setFilter("CORRECT")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              filter === "CORRECT"
                ? "bg-emerald-600 text-white font-bold shadow-sm"
                : "bg-slate-800 text-slate-300 hover:bg-slate-700"
            }`}
          >
            Correct ({solutions.filter((s) => s.is_correct).length})
          </button>
          <button
            onClick={() => setFilter("UNANSWERED")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              filter === "UNANSWERED"
                ? "bg-amber-600 text-white font-bold shadow-sm"
                : "bg-slate-800 text-slate-300 hover:bg-slate-700"
            }`}
          >
            Unanswered ({solutions.filter((s) => !getUserAnswer(s)).length})
          </button>
        </div>

        {/* Counter Indicator */}
        <div className="flex items-center gap-3">
          <span className="text-xs font-bold text-slate-300 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
            Slide {currentIndex + 1} of {filteredSolutions.length}
          </span>
        </div>
      </div>

      {/* Slide Navigation Palette Grid */}
      <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
          Jump to Question Slide:
        </p>
        <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto pr-1">
          {filteredSolutions.map((sol, idx) => {
            const isCurrent = idx === currentIndex;
            const userAns = getUserAnswer(sol);
            let statusColor = "bg-slate-800 border-slate-700 text-slate-400 hover:bg-slate-700";
            if (sol.is_correct) {
              statusColor = "bg-emerald-950/60 border-emerald-500/50 text-emerald-300 hover:bg-emerald-900/60";
            } else if (userAns) {
              statusColor = "bg-rose-950/60 border-rose-500/50 text-rose-300 hover:bg-rose-900/60";
            }

            return (
              <button
                key={sol.question_id}
                onClick={() => setCurrentIndex(idx)}
                className={`w-9 h-9 rounded-lg text-xs font-bold flex items-center justify-center border transition-all ${statusColor} ${
                  isCurrent ? "ring-2 ring-brand-400 scale-110 shadow-lg z-10" : ""
                }`}
                title={`Question ${idx + 1}: ${sol.is_correct ? "Correct" : userAns ? "Incorrect" : "Unanswered"}`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Slide Card */}
      <Card className="p-6 md:p-8 space-y-6 bg-slate-900 border border-slate-800 shadow-2xl relative">
        {/* Slide Question Header */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <span className="text-sm md:text-base font-extrabold text-brand-400">
              Question {(originalIndex >= 0 ? originalIndex : currentIndex) + 1}
            </span>
            <Badge variant="neutral" className="uppercase font-mono text-[10px]">
              {activeSolution.type || "MCQ"}
            </Badge>
          </div>

          <div className="flex items-center gap-2">
            <Badge
              variant={
                activeSolution.is_correct
                  ? "success"
                  : activeHasAnswered
                  ? "error"
                  : "neutral"
              }
              className="text-xs py-1 px-3"
            >
              {activeSolution.is_correct ? (
                <span className="flex items-center gap-1 text-emerald-300">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Correct (+{activeSolution.marks_awarded || 1.0})
                </span>
              ) : activeHasAnswered ? (
                <span className="flex items-center gap-1 text-rose-300">
                  <XCircle className="w-3.5 h-3.5" /> Incorrect (-{activeSolution.penalty_deducted || 0.25})
                </span>
              ) : (
                <span className="flex items-center gap-1 text-slate-400">
                  <AlertCircle className="w-3.5 h-3.5" /> Unanswered (0.0)
                </span>
              )}
            </Badge>
          </div>
        </div>

        {/* Question Text / Code Block */}
        <div className="space-y-3">
          {isCCode ? (
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs md:text-sm text-emerald-300 overflow-x-auto whitespace-pre leading-relaxed shadow-inner">
              {activeSolution.question_text}
            </div>
          ) : (
            <p className="text-base md:text-lg font-medium text-slate-100 leading-relaxed">
              {activeSolution.question_text}
            </p>
          )}
        </div>

        {/* Options List with Classic Green & Red Feedback */}
        <div className="space-y-3 pt-2">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Options & Answer Status:
          </p>

          {optionsList.length > 0 ? (
            <div className="grid grid-cols-1 gap-3">
              {optionsList.map(({ key, label }) => {
                const { isUserChoice, isRightChoice } = checkOptionStatus(key, label);

                // Option Card Styling Rules:
                // 1. Right Answer (Classic Emerald Green)
                // 2. User's Wrong Answer (Rose Red)
                // 3. Unselected Neutral
                let cardStyle = "bg-slate-950/60 border-slate-800 text-slate-300 hover:border-slate-700";
                let badgeContent = null;

                if (isRightChoice && isUserChoice) {
                  // User chose the correct answer -> Classic Emerald Green
                  cardStyle =
                    "bg-emerald-950/40 border-2 border-emerald-500 text-emerald-100 shadow-md shadow-emerald-950/40";
                  badgeContent = (
                    <span className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold">
                      <Check className="w-3.5 h-3.5" /> Your Selection (Correct)
                    </span>
                  );
                } else if (isRightChoice) {
                  // Official correct answer (which user missed or skipped) -> Classic Emerald Green
                  cardStyle =
                    "bg-emerald-950/30 border-2 border-emerald-500/80 text-emerald-200 shadow-md shadow-emerald-950/30";
                  badgeContent = (
                    <span className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold">
                      <Check className="w-3.5 h-3.5" /> Official Right Answer
                    </span>
                  );
                } else if (isUserChoice) {
                  // User chose this WRONG answer -> Rose Red
                  cardStyle =
                    "bg-rose-950/40 border-2 border-rose-500 text-rose-100 shadow-md shadow-rose-950/40";
                  badgeContent = (
                    <span className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs font-bold">
                      <X className="w-3.5 h-3.5" /> Your Selection (Incorrect)
                    </span>
                  );
                }

                return (
                  <div
                    key={key}
                    className={`p-4 rounded-xl border transition-all flex items-center justify-between gap-4 ${cardStyle}`}
                  >
                    <div className="flex items-center gap-3.5">
                      <span
                        className={`w-7 h-7 rounded-lg text-xs font-bold flex items-center justify-center border ${
                          isRightChoice
                            ? "bg-emerald-500 text-slate-950 border-emerald-400 font-extrabold"
                            : isUserChoice
                            ? "bg-rose-500 text-white border-rose-400 font-extrabold"
                            : "bg-slate-800 text-slate-300 border-slate-700"
                        }`}
                      >
                        {key}
                      </span>
                      <span className="text-sm font-medium leading-normal">{label}</span>
                    </div>

                    {badgeContent && <div className="flex-shrink-0">{badgeContent}</div>}
                  </div>
                );
              })}
            </div>
          ) : (
            /* NAT (Numerical Answer Type) or Direct Text Display */
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div
                className={`p-4 rounded-xl border ${
                  activeSolution.is_correct
                    ? "bg-emerald-950/30 border-emerald-500/50 text-emerald-200"
                    : activeSolution.user_answer
                    ? "bg-rose-950/30 border-rose-500/50 text-rose-200"
                    : "bg-slate-800/60 border-slate-700 text-slate-300"
                }`}
              >
                <p className="text-xs text-slate-400 mb-1 font-semibold">Your Submitted Answer:</p>
                <p className="text-base font-bold">
                  {activeSolution.user_answer || "Not Answered"}
                </p>
              </div>

              <div className="p-4 rounded-xl bg-emerald-950/30 border-2 border-emerald-500/80 text-emerald-200">
                <p className="text-xs text-emerald-400/90 mb-1 font-semibold">Official Right Answer:</p>
                <p className="text-base font-bold text-emerald-300">{activeSolution.correct_answer}</p>
              </div>
            </div>
          )}
        </div>

        {/* Detailed Solution Explanation Box */}
        <div className="p-5 rounded-xl bg-slate-950 border border-slate-800 space-y-3 shadow-inner">
          <div className="flex items-center gap-2 text-brand-400 font-bold text-xs uppercase tracking-wider">
            <Lightbulb className="w-4 h-4 text-amber-400" />
            <span>Detailed Solution & Explanation:</span>
          </div>

          {activeSolution.explanation ? (
            <div className="text-xs md:text-sm text-slate-200 leading-relaxed font-mono whitespace-pre-wrap bg-slate-900/80 p-4 rounded-lg border border-slate-800/80">
              {activeSolution.explanation}
            </div>
          ) : (
            <p className="text-xs text-slate-500 italic">
              No additional step-by-step explanation recorded for this item.
            </p>
          )}
        </div>

        {/* Slide Footer Navigation Controls */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-800">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
            disabled={currentIndex === 0}
            leftIcon={<ChevronLeft className="w-4 h-4" />}
          >
            Previous
          </Button>

          <span className="text-xs font-semibold text-slate-400 hidden sm:inline">
            Use <kbd className="px-1.5 py-0.5 bg-slate-800 rounded border border-slate-700 text-slate-300 font-mono">←</kbd> and <kbd className="px-1.5 py-0.5 bg-slate-800 rounded border border-slate-700 text-slate-300 font-mono">→</kbd> keys to navigate
          </span>

          <Button
            variant="primary"
            size="sm"
            onClick={() => setCurrentIndex((prev) => Math.min(filteredSolutions.length - 1, prev + 1))}
            disabled={currentIndex === filteredSolutions.length - 1}
            rightIcon={<ChevronRight className="w-4 h-4" />}
          >
            Next
          </Button>
        </div>
      </Card>
    </div>
  );
};
