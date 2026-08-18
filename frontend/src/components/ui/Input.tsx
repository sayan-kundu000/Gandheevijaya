import React from "react";
import { clsx } from "clsx";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className, id, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="flex flex-col gap-1.5 w-full">
        {label && (
          <label htmlFor={inputId} className="text-xs font-medium text-slate-300">
            {label}
          </label>
        )}
        <input
          id={inputId}
          ref={ref}
          className={clsx(
            "w-full rounded-lg bg-slate-800/80 border px-3.5 py-2 text-sm text-slate-100 placeholder-slate-500 transition-colors focus:outline-none focus:ring-2 focus:ring-brand-500",
            error ? "border-rose-500/80 focus:ring-rose-500" : "border-slate-700/80 hover:border-slate-600",
            className
          )}
          {...props}
        />
        {error && <p className="text-xs text-rose-400 font-medium">{error}</p>}
        {helperText && !error && <p className="text-xs text-slate-500">{helperText}</p>}
      </div>
    );
  }
);
Input.displayName = "Input";
