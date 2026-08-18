import React from "react";
import { Card } from "./Card";
import { Skeleton } from "./Skeleton";

interface StatCardProps {
  title: string;
  value: React.ReactNode;
  subtitle?: string;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    label?: string;
    isPositive?: boolean;
  };
  isLoading?: boolean;
  className?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  isLoading = false,
  className = "",
}) => {
  return (
    <Card className={`p-4 ${className}`}>
      <div className="flex items-start justify-between gap-3">
        <div className="space-y-1">
          <p className="text-xs font-medium text-slate-400">{title}</p>
          {isLoading ? (
            <Skeleton className="h-7 w-20 mt-1" />
          ) : (
            <h4 className="text-xl font-bold text-slate-100 tracking-tight">{value}</h4>
          )}
          {subtitle && <p className="text-[11px] text-slate-400">{subtitle}</p>}
        </div>

        {icon && (
          <div className="p-2.5 rounded-xl bg-slate-800 border border-slate-700 text-brand-400 shrink-0">
            {icon}
          </div>
        )}
      </div>

      {trend && !isLoading && (
        <div className="mt-3 pt-2 border-t border-slate-800/80 flex items-center gap-1.5 text-[11px]">
          <span
            className={`font-semibold ${
              trend.isPositive ?? trend.value >= 0 ? "text-emerald-400" : "text-rose-400"
            }`}
          >
            {trend.value >= 0 ? `+${trend.value}%` : `${trend.value}%`}
          </span>
          {trend.label && <span className="text-slate-500">{trend.label}</span>}
        </div>
      )}
    </Card>
  );
};
