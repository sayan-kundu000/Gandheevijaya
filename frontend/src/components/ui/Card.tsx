import React from "react";
import { clsx } from "clsx";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  glass?: boolean;
}

export const Card: React.FC<CardProps> = ({ children, className, glass = true, ...props }) => {
  return (
    <div
      className={clsx(
        "rounded-xl border border-slate-800 p-5 shadow-xl transition-all",
        glass ? "bg-slate-900/80 backdrop-blur-md" : "bg-slate-800",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className, ...props }) => (
  <div className={clsx("flex items-center justify-between border-b border-slate-800 pb-3 mb-4", className)} {...props}>
    {children}
  </div>
);

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({ children, className, ...props }) => (
  <h3 className={clsx("text-lg font-semibold text-slate-100 tracking-tight", className)} {...props}>
    {children}
  </h3>
);

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className, ...props }) => (
  <div className={clsx("text-slate-300", className)} {...props}>
    {children}
  </div>
);

