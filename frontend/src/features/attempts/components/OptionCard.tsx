import React from "react";

interface OptionCardProps {
  optionKey: string;
  optionText: string;
  isSelected?: boolean;
  isDisabled?: boolean;
  onClick: () => void;
}

export const OptionCard: React.FC<OptionCardProps> = ({
  optionKey,
  optionText,
  isSelected = false,
  isDisabled = false,
  onClick,
}) => {
  return (
    <div
      onClick={() => !isDisabled && onClick()}
      className={`p-4 rounded-xl border transition-all flex items-center gap-3 ${
        isDisabled ? "cursor-not-allowed opacity-60" : "cursor-pointer"
      } ${
        isSelected
          ? "border-brand-500 bg-brand-950/40 ring-1 ring-brand-500 text-slate-100"
          : "border-slate-800 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-800/40 text-slate-300"
      }`}
    >
      <div
        className={`w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
          isSelected
            ? "bg-brand-500 text-white"
            : "bg-slate-800 text-slate-400 border border-slate-700"
        }`}
      >
        {optionKey}
      </div>
      <span className="text-sm font-medium leading-relaxed">{optionText}</span>
    </div>
  );
};
