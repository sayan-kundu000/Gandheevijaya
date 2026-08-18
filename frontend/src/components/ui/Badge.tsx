import React from "react";
import { clsx } from "clsx";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "success" | "warning" | "error" | "info" | "neutral" | "brand";
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = "neutral", className, ...props }) => {
  const variants = {
    success: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    warning: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    error: "bg-rose-500/10 text-rose-400 border-rose-500/20",
    info: "bg-sky-500/10 text-sky-400 border-sky-500/20",
    neutral: "bg-slate-700/30 text-slate-300 border-slate-700/50",
    brand: "bg-brand-500/10 text-brand-400 border-brand-500/20",
  };

  return (
    <span
      className={clsx(
        "inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium border",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};
