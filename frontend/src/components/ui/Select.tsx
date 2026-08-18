import React from "react";
import { clsx } from "clsx";

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  options?: { value: string | number; label: string }[];
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, options, children, className, id, ...props }, ref) => {
    const selectId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="flex flex-col gap-1.5 w-full">
        {label && (
          <label htmlFor={selectId} className="text-xs font-medium text-slate-300">
            {label}
          </label>
        )}
        <select
          id={selectId}
          ref={ref}
          className={clsx(
            "w-full rounded-lg bg-slate-800/80 border px-3.5 py-2 text-sm text-slate-100 transition-colors focus:outline-none focus:ring-2 focus:ring-brand-500",
            error ? "border-rose-500/80" : "border-slate-700/80 hover:border-slate-600",
            className
          )}
          {...props}
        >
          {options
            ? options.map((opt) => (
                <option key={opt.value} value={opt.value} className="bg-slate-800 text-slate-100">
                  {opt.label}
                </option>
              ))
            : children}
        </select>
        {error && <p className="text-xs text-rose-400 font-medium">{error}</p>}
      </div>
    );
  }
);
Select.displayName = "Select";
