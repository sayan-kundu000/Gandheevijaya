import React from "react";
import { AlertCircle, CheckCircle2, Info, AlertTriangle, X } from "lucide-react";

export type AlertVariant = "info" | "success" | "warning" | "error";

interface AlertProps {
  variant?: AlertVariant;
  title?: string;
  children: React.ReactNode;
  onClose?: () => void;
  className?: string;
}

const variantStyles: Record<AlertVariant, { bg: string; border: string; text: string; icon: React.ReactNode }> = {
  info: {
    bg: "bg-sky-500/10",
    border: "border-sky-500/20",
    text: "text-sky-300",
    icon: <Info className="w-4 h-4 text-sky-400 shrink-0" />,
  },
  success: {
    bg: "bg-emerald-500/10",
    border: "border-emerald-500/20",
    text: "text-emerald-300",
    icon: <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />,
  },
  warning: {
    bg: "bg-amber-500/10",
    border: "border-amber-500/20",
    text: "text-amber-300",
    icon: <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />,
  },
  error: {
    bg: "bg-rose-500/10",
    border: "border-rose-500/20",
    text: "text-rose-300",
    icon: <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />,
  },
};

export const Alert: React.FC<AlertProps> = ({
  variant = "info",
  title,
  children,
  onClose,
  className = "",
}) => {
  const style = variantStyles[variant];

  return (
    <div
      role="alert"
      className={`p-4 rounded-xl border flex items-start justify-between gap-3 text-xs leading-relaxed ${style.bg} ${style.border} ${style.text} ${className}`}
    >
      <div className="flex items-start gap-2.5">
        {style.icon}
        <div className="space-y-0.5">
          {title && <h5 className="font-bold text-sm text-slate-100">{title}</h5>}
          <div className="text-slate-300">{children}</div>
        </div>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="text-slate-400 hover:text-slate-200 transition-colors p-0.5 rounded-lg"
          aria-label="Dismiss alert"
        >
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  );
};
