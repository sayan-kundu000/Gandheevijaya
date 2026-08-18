import React from "react";
import { clsx } from "clsx";

export interface ProgressBarProps {
  value: number; // 0 to 100
  color?: "brand" | "emerald" | "amber" | "rose";
  height?: "sm" | "md" | "lg";
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  color = "brand",
  height = "md",
  className,
}) => {
  const clampedValue = Math.min(100, Math.max(0, value));

  const colors = {
    brand: "bg-brand-500",
    emerald: "bg-emerald-500",
    amber: "bg-amber-500",
    rose: "bg-rose-500",
  };

  const heights = {
    sm: "h-1.5",
    md: "h-2.5",
    lg: "h-4",
  };

  return (
    <div className={clsx("w-full bg-slate-800 rounded-full overflow-hidden", heights[height], className)}>
      <div
        className={clsx("h-full transition-all duration-300 ease-out rounded-full", colors[color])}
        style={{ width: `${clampedValue}%` }}
      />
    </div>
  );
};
