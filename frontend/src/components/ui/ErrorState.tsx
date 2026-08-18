import React from "react";
import { AlertTriangle } from "lucide-react";
import { Button } from "./Button";

export interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = "Failed to load data",
  message = "An unexpected error occurred while communicating with the server.",
  onRetry,
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center rounded-xl border border-rose-500/20 bg-rose-950/10">
      <AlertTriangle className="w-10 h-10 text-rose-400 mb-3" />
      <h3 className="text-base font-semibold text-rose-200 mb-1">{title}</h3>
      <p className="text-sm text-slate-400 max-w-sm mb-4">{message}</p>
      {onRetry && (
        <Button variant="outline" size="sm" onClick={onRetry}>
          Try Again
        </Button>
      )}
    </div>
  );
};
