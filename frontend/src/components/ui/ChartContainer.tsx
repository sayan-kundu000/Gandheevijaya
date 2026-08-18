import React from "react";
import { Card, CardHeader, CardTitle } from "./Card";
import { Skeleton } from "./Skeleton";
import { EmptyState } from "./EmptyState";
import { BarChart2 } from "lucide-react";

interface ChartContainerProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  isLoading?: boolean;
  isEmpty?: boolean;
  emptyTitle?: string;
  emptyDescription?: string;
  action?: React.ReactNode;
  className?: string;
}

export const ChartContainer: React.FC<ChartContainerProps> = ({
  title,
  subtitle,
  children,
  isLoading = false,
  isEmpty = false,
  emptyTitle = "Insufficient Data",
  emptyDescription = "Complete more quiz assessments to generate performance visualization.",
  action,
  className = "",
}) => {
  return (
    <Card className={className}>
      <CardHeader className="flex flex-row items-center justify-between gap-4">
        <div>
          <CardTitle>{title}</CardTitle>
          {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
        </div>
        {action}
      </CardHeader>

      <div className="p-4 pt-0">
        {isLoading ? (
          <Skeleton className="h-64 w-full rounded-xl" />
        ) : isEmpty ? (
          <div className="py-8">
            <EmptyState
              icon={<BarChart2 className="w-10 h-10 text-slate-500" />}
              title={emptyTitle}
              description={emptyDescription}
            />
          </div>
        ) : (
          <div className="w-full h-64">{children}</div>
        )}
      </div>
    </Card>
  );
};
