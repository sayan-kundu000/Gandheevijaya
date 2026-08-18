import React from "react";
import { clsx } from "clsx";

export const Skeleton: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, ...props }) => {
  return <div className={clsx("animate-pulse rounded-lg bg-slate-800/80", className)} {...props} />;
};
