import React from "react";

interface RadioProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  description?: string;
}

export const Radio: React.FC<RadioProps> = ({
  label,
  description,
  className = "",
  id,
  disabled,
  ...props
}) => {
  const generatedId = id || `radio-${Math.random().toString(36).substring(2, 9)}`;

  return (
    <div className="flex items-start gap-2.5">
      <input
        type="radio"
        id={generatedId}
        disabled={disabled}
        className={`h-4 w-4 border-slate-700 bg-slate-900 text-brand-500 focus:ring-brand-500 focus:ring-offset-slate-950 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
        {...props}
      />
      {(label || description) && (
        <div className="text-xs space-y-0.5">
          {label && (
            <label
              htmlFor={generatedId}
              className={`font-medium text-slate-200 cursor-pointer ${
                disabled ? "opacity-50 cursor-not-allowed" : ""
              }`}
            >
              {label}
            </label>
          )}
          {description && <p className="text-slate-400">{description}</p>}
        </div>
      )}
    </div>
  );
};
