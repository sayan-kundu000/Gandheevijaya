import React from "react";
import { Clock } from "lucide-react";

interface TimerProps {
  secondsLeft: number;
  className?: string;
}

export const Timer: React.FC<TimerProps> = ({ secondsLeft, className = "" }) => {
  const minutes = Math.floor(secondsLeft / 60);
  const seconds = secondsLeft % 60;
  const formatted = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

  const isWarning = secondsLeft < 180; // less than 3 mins

  return (
    <div
      className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border font-mono font-bold text-sm ${
        isWarning
          ? "bg-rose-500/20 border-rose-500/40 text-rose-400 animate-pulse"
          : "bg-slate-800 border-slate-700 text-slate-200"
      } ${className}`}
    >
      <Clock className="w-4 h-4" />
      <span>{formatted}</span>
    </div>
  );
};
