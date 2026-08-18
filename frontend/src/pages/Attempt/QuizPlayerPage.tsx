import React, { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useQuery, useMutation } from "@tanstack/react-query";
import { attemptApi } from "../../services/attemptApi";
import { AttemptQuestionItem, StartQuizResponse } from "../../types";
import { Card } from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";
import { Badge } from "../../components/ui/Badge";
import { ProgressBar } from "../../components/ui/ProgressBar";
import { Modal } from "../../components/ui/Modal";
import { Skeleton } from "../../components/ui/Skeleton";
import { QuestionRenderer } from "../../features/attempts/components/QuestionRenderer";
import {
  Clock,
  ChevronLeft,
  ChevronRight,
  Bookmark,
  Send,
  Check,
  Menu,
  X,
  AlertCircle,
  RefreshCw,
} from "lucide-react";

export const QuizPlayerPage: React.FC = () => {
  const { attemptId } = useParams<{ attemptId: string }>();
  const navigate = useNavigate();
  const location = useLocation();

  // Initial State from navigation state (if passed from QuizStartPage)
  const initialData: StartQuizResponse | undefined = location.state?.quizData;

  // Hydration Query from Backend if page refreshed or deep linked directly
  const {
    data: resumeData,
    isLoading: isResumeLoading,
    error: resumeError,
    refetch: refetchAttempt,
  } = useQuery({
    queryKey: ["attempt", "resume", attemptId],
    queryFn: () => attemptApi.getAttempt(attemptId || ""),
    enabled: !!attemptId,
    staleTime: 0,
  });

  const attempt = resumeData?.attempt || initialData?.attempt;
  const questions: AttemptQuestionItem[] = resumeData?.questions || initialData?.questions || [];
  const totalQuestions = questions.length || attempt?.total_questions || 0;

  const calculateRemainingSeconds = (att?: any): number => {
    if (!att) return 1800;
    if (typeof att.remaining_seconds === "number" && att.remaining_seconds > 0) {
      return att.remaining_seconds;
    }
    if (att.expires_at) {
      let expStr = String(att.expires_at).trim();
      if (!expStr.endsWith("Z") && !expStr.includes("+") && !expStr.includes("-", 10)) {
        expStr += "Z";
      }
      const expiryMs = new Date(expStr).getTime();
      const nowMs = Date.now();
      const diffSec = Math.floor((expiryMs - nowMs) / 1000);
      if (!isNaN(diffSec) && diffSec > 0) {
        return diffSec;
      }
    }
    return (att.duration_minutes || 30) * 60;
  };

  // Local UI State
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [userAnswers, setUserAnswers] = useState<Record<string, string>>({});
  const [markedQuestions, setMarkedQuestions] = useState<Record<string, boolean>>({});
  const [saveStatus, setSaveStatus] = useState<"SAVED" | "SAVING" | "ERROR">("SAVED");
  const [timeLeftSeconds, setTimeLeftSeconds] = useState<number>(() =>
    calculateRemainingSeconds(initialData?.attempt)
  );
  const [timerStarted, setTimerStarted] = useState<boolean>(false);
  const [isSubmitModalOpen, setIsSubmitModalOpen] = useState<boolean>(false);
  const [isMobilePaletteOpen, setIsMobilePaletteOpen] = useState<boolean>(false);

  // Sync state when resumeData arrives from backend API
  useEffect(() => {
    if (resumeData) {
      if (resumeData.attempt) {
        if (
          resumeData.attempt.status === "SUBMITTED" ||
          resumeData.attempt.status === "EXPIRED"
        ) {
          navigate(`/results/${resumeData.attempt.id}`, { replace: true });
          return;
        }
        const remaining = calculateRemainingSeconds(resumeData.attempt);
        setTimeLeftSeconds(remaining);
        setTimerStarted(true);
      }
      if (resumeData.answers_map) {
        const cleanAnswers: Record<string, string> = {};
        Object.entries(resumeData.answers_map).forEach(([qId, val]) => {
          if (val !== null && val !== undefined) cleanAnswers[qId] = val;
        });
        setUserAnswers(cleanAnswers);
      }
      if (resumeData.review_map) {
        setMarkedQuestions(resumeData.review_map);
      }
    } else if (initialData?.attempt) {
      const remaining = calculateRemainingSeconds(initialData.attempt);
      setTimeLeftSeconds(remaining);
      setTimerStarted(true);
    }
  }, [resumeData, initialData, navigate]);

  // Submission mutation
  const submitMutation = useMutation({
    mutationFn: () => attemptApi.submitAttempt(attemptId || ""),
    onSuccess: (result) => {
      navigate(`/results/${result.attempt_id || result.id || attemptId}`);
    },
  });

  // Countdown timer effect (guarded against premature submission on initial render)
  useEffect(() => {
    if (!timerStarted) return;
    if (timeLeftSeconds <= 0) {
      if (
        attempt &&
        attempt.status === "IN_PROGRESS" &&
        !submitMutation.isPending &&
        !submitMutation.isSuccess
      ) {
        submitMutation.mutate();
      }
      return;
    }
    const timer = setInterval(() => {
      setTimeLeftSeconds((prev) => Math.max(0, prev - 1));
    }, 1000);
    return () => clearInterval(timer);
  }, [timerStarted, timeLeftSeconds, attempt, submitMutation]);

  const currentQuestion = questions[currentIndex];

  // Save Response handler with optimistic update and error handling
  const handleSelectAnswer = async (questionId: string, answerKey: string | null) => {
    setUserAnswers((prev) => {
      const copy = { ...prev };
      if (answerKey === null) {
        delete copy[questionId];
      } else {
        copy[questionId] = answerKey;
      }
      return copy;
    });

    setSaveStatus("SAVING");
    try {
      await attemptApi.saveResponse(attemptId || "", {
        question_id: questionId,
        selected_answer: answerKey,
        marked_for_review: !!markedQuestions[questionId],
      });
      setSaveStatus("SAVED");
    } catch (err) {
      setSaveStatus("ERROR");
    }
  };

  const toggleMarkForReview = async (questionId: string) => {
    const isMarked = !markedQuestions[questionId];
    setMarkedQuestions((prev) => ({ ...prev, [questionId]: isMarked }));
    try {
      await attemptApi.saveResponse(attemptId || "", {
        question_id: questionId,
        selected_answer: userAnswers[questionId] || null,
        marked_for_review: isMarked,
      });
    } catch (e) {
      // Ignore background retry failure
    }
  };

  // Keyboard Navigation Shortcuts (1-4 for MCQ options, N next, P prev, M mark)
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (["INPUT", "TEXTAREA"].includes((e.target as HTMLElement).tagName)) return;
      if (!currentQuestion) return;

      if (["1", "2", "3", "4"].includes(e.key) && currentQuestion.type === "MCQ") {
        const idx = parseInt(e.key, 10) - 1;
        let optKeys: string[] = [];
        if (Array.isArray(currentQuestion.options)) {
          optKeys = currentQuestion.options.map((_, i) => String.fromCharCode(65 + i));
        } else if (typeof currentQuestion.options === "object" && currentQuestion.options !== null) {
          optKeys = Object.keys(currentQuestion.options);
        }
        if (optKeys[idx]) {
          handleSelectAnswer(currentQuestion.id, optKeys[idx]);
        }
      } else if (e.key.toLowerCase() === "n") {
        if (currentIndex < totalQuestions - 1) setCurrentIndex((prev) => prev + 1);
      } else if (e.key.toLowerCase() === "p") {
        if (currentIndex > 0) setCurrentIndex((prev) => prev - 1);
      } else if (e.key.toLowerCase() === "m") {
        toggleMarkForReview(currentQuestion.id);
      }
    },
    [currentIndex, currentQuestion, totalQuestions, markedQuestions, userAnswers]
  );

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  const formatTime = (secs: number) => {
    const h = Math.floor(secs / 3600);
    const m = Math.floor((secs % 3600) / 60);
    const s = secs % 60;
    if (h > 0) {
      return `${h}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
    }
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  const answeredCount = Object.keys(userAnswers).length;
  const markedCount = Object.values(markedQuestions).filter(Boolean).length;

  if (isResumeLoading || !currentQuestion) {
    return (
      <div className="min-h-screen bg-slate-950 p-6 flex flex-col gap-6">
        <Skeleton className="h-16 w-full" />
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <Skeleton className="h-96 lg:col-span-3" />
          <Skeleton className="h-96" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between antialiased">
      {/* Top Bar Header */}
      <header className="h-16 border-b border-slate-800 bg-slate-900/90 backdrop-blur-md px-4 md:px-6 flex items-center justify-between sticky top-0 z-20">
        <div className="flex items-center gap-3">
          <Badge variant="brand">Quiz Attempt</Badge>
          <div className="hidden sm:flex items-center gap-2 text-xs text-slate-400">
            <span>
              Question {currentIndex + 1} of {totalQuestions}
            </span>
          </div>
        </div>

        {/* Autosave Status & Authoritative Timer */}
        <div className="flex items-center gap-3 md:gap-4">
          <div className="text-xs font-mono hidden sm:inline-flex items-center gap-1">
            {saveStatus === "SAVING" ? (
              <span className="text-amber-400 flex items-center gap-1">
                <RefreshCw className="w-3 h-3 animate-spin" /> Saving...
              </span>
            ) : saveStatus === "SAVED" ? (
              <span className="text-emerald-400 flex items-center gap-1">
                <Check className="w-3 h-3" /> Saved
              </span>
            ) : (
              <span className="text-rose-400 flex items-center gap-1">
                <AlertCircle className="w-3 h-3" /> Failed
              </span>
            )}
          </div>

          <div
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border font-mono font-bold text-xs md:text-sm ${
              timeLeftSeconds < 60
                ? "bg-rose-500/20 border-rose-500/50 text-rose-400 animate-pulse"
                : timeLeftSeconds < 300
                ? "bg-amber-500/20 border-amber-500/40 text-amber-400"
                : "bg-slate-800 border-slate-700 text-slate-200"
            }`}
          >
            <Clock className="w-4 h-4" />
            <span>{formatTime(timeLeftSeconds)}</span>
          </div>

          {/* Mobile Palette Toggle */}
          <Button
            variant="outline"
            size="sm"
            className="lg:hidden p-2"
            onClick={() => setIsMobilePaletteOpen(!isMobilePaletteOpen)}
          >
            <Menu className="w-4 h-4" />
          </Button>

          <Button
            variant="danger"
            size="sm"
            leftIcon={<Send className="w-3.5 h-3.5" />}
            onClick={() => setIsSubmitModalOpen(true)}
          >
            Submit
          </Button>
        </div>
      </header>

      {/* Progress Line */}
      <ProgressBar value={((currentIndex + 1) / totalQuestions) * 100} height="sm" />

      {/* Main Body Grid */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Question Area */}
        <div className="lg:col-span-3 space-y-6">
          <Card className="p-6 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-slate-400">
                  Question {currentIndex + 1}
                </span>
              </div>

              <button
                onClick={() => toggleMarkForReview(currentQuestion.id)}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium border transition-colors ${
                  markedQuestions[currentQuestion.id]
                    ? "bg-amber-500/20 border-amber-500/40 text-amber-300"
                    : "bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200"
                }`}
              >
                <Bookmark className="w-3.5 h-3.5" />
                <span>
                  {markedQuestions[currentQuestion.id] ? "Marked for Review" : "Mark for Review"}
                </span>
              </button>
            </div>

            {/* Dynamic Question Renderer */}
            <QuestionRenderer
              question={currentQuestion}
              selectedAnswer={userAnswers[currentQuestion.id] || null}
              onSelectAnswer={(key) => handleSelectAnswer(currentQuestion.id, key)}
            />
          </Card>

          {/* Navigation Bar */}
          <div className="flex items-center justify-between">
            <Button
              variant="outline"
              size="md"
              disabled={currentIndex === 0}
              leftIcon={<ChevronLeft className="w-4 h-4" />}
              onClick={() => setCurrentIndex((prev) => prev - 1)}
            >
              Previous (P)
            </Button>

            <span className="text-xs text-slate-500 hidden sm:inline">
              Shortcuts: [1-4] Select • [N] Next • [P] Prev • [M] Mark
            </span>

            <Button
              variant="primary"
              size="md"
              disabled={currentIndex === totalQuestions - 1}
              rightIcon={<ChevronRight className="w-4 h-4" />}
              onClick={() => setCurrentIndex((prev) => prev + 1)}
            >
              Next (N)
            </Button>
          </div>
        </div>

        {/* Question Palette Sidebar (Desktop) */}
        <div className="hidden lg:block space-y-4">
          <Card className="p-4 space-y-4">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Question Palette
            </h4>

            {/* Question Palette Grid */}
            <div className="grid grid-cols-5 gap-2 max-h-80 overflow-y-auto pr-1">
              {questions.map((q, idx) => {
                const isCurrent = idx === currentIndex;
                const isAnswered = !!userAnswers[q.id];
                const isMarked = !!markedQuestions[q.id];

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
                    key={q.id}
                    onClick={() => setCurrentIndex(idx)}
                    className={`h-9 rounded-lg font-mono text-xs font-semibold border flex items-center justify-center transition-all ${bgClass} ${
                      isCurrent ? "ring-2 ring-brand-400 ring-offset-2 ring-offset-slate-900" : ""
                    }`}
                  >
                    {idx + 1}
                  </button>
                );
              })}
            </div>

            {/* Palette Legend */}
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
                <span className="font-semibold text-slate-200">{totalQuestions - answeredCount}</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5">
                  <span className="w-3 h-3 rounded bg-amber-500 inline-block" /> Marked for Review
                </span>
                <span className="font-semibold text-slate-200">{markedCount}</span>
              </div>
            </div>
          </Card>
        </div>
      </main>

      {/* Mobile Question Palette Drawer */}
      {isMobilePaletteOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex justify-end lg:hidden">
          <div className="w-4/5 max-w-sm bg-slate-900 h-full p-6 border-l border-slate-800 space-y-6 overflow-y-auto">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
                Question Palette
              </h4>
              <button
                onClick={() => setIsMobilePaletteOpen(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-5 gap-2">
              {questions.map((q, idx) => {
                const isCurrent = idx === currentIndex;
                const isAnswered = !!userAnswers[q.id];
                const isMarked = !!markedQuestions[q.id];

                let bgClass = "bg-slate-800 text-slate-400 border-slate-700";
                if (isAnswered && isMarked) bgClass = "bg-purple-600 text-white border-purple-500";
                else if (isAnswered) bgClass = "bg-emerald-600 text-white border-emerald-500";
                else if (isMarked) bgClass = "bg-amber-500 text-slate-950 font-bold border-amber-400";

                return (
                  <button
                    key={q.id}
                    onClick={() => {
                      setCurrentIndex(idx);
                      setIsMobilePaletteOpen(false);
                    }}
                    className={`h-10 rounded-lg font-mono text-xs font-semibold border flex items-center justify-center ${bgClass} ${
                      isCurrent ? "ring-2 ring-brand-400" : ""
                    }`}
                  >
                    {idx + 1}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Submission Confirmation Modal */}
      <Modal
        isOpen={isSubmitModalOpen}
        onClose={() => setIsSubmitModalOpen(false)}
        title="Confirm Quiz Submission"
      >
        <div className="space-y-4">
          <p className="text-sm text-slate-300">
            Are you sure you want to finalize and submit your quiz attempt now?
          </p>

          <div className="grid grid-cols-2 gap-3 p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs">
            <div>
              <p className="text-slate-400">Total Questions</p>
              <p className="text-sm font-bold text-slate-100">{totalQuestions}</p>
            </div>
            <div>
              <p className="text-slate-400">Answered</p>
              <p className="text-sm font-bold text-emerald-400">{answeredCount}</p>
            </div>
            <div>
              <p className="text-slate-400">Unanswered</p>
              <p className="text-sm font-bold text-amber-400">{totalQuestions - answeredCount}</p>
            </div>
            <div>
              <p className="text-slate-400">Time Remaining</p>
              <p className="text-sm font-bold text-brand-400">{formatTime(timeLeftSeconds)}</p>
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <Button variant="ghost" onClick={() => setIsSubmitModalOpen(false)}>
              Continue Quiz
            </Button>
            <Button
              variant="danger"
              isLoading={submitMutation.isPending}
              onClick={() => submitMutation.mutate()}
            >
              Submit Quiz
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};
