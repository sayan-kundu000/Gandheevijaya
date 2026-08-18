import React, { useState, useRef, useEffect } from "react";
import { useTheme, THEME_CONFIGS, ThemeMode } from "../../context/ThemeContext";
import { Palette, Check, ChevronDown } from "lucide-react";

export const ThemeSwitcher: React.FC = () => {
  const { theme, setTheme } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const activeConfig = THEME_CONFIGS.find((t) => t.id === theme) || THEME_CONFIGS[0];

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-xl border border-slate-700 bg-slate-800/80 hover:bg-slate-700/80 text-xs font-semibold text-slate-200 transition-all shadow-sm focus:outline-none"
        title="Switch Visual Theme"
      >
        <Palette className="w-3.5 h-3.5 text-brand-400" />
        <span className="hidden sm:inline-flex items-center gap-1.5">
          <span>{activeConfig.icon}</span>
          <span>{activeConfig.name}</span>
        </span>
        <span className="sm:hidden">{activeConfig.icon}</span>
        <ChevronDown className={`w-3 h-3 transition-transform ${isOpen ? "rotate-180" : ""}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 rounded-2xl bg-slate-900 border border-slate-700 shadow-2xl z-50 p-2 space-y-1 animate-in fade-in zoom-in-95 duration-150">
          <p className="px-3 py-1 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
            Select Visual Theme:
          </p>

          {THEME_CONFIGS.map((config) => {
            const isSelected = config.id === theme;
            return (
              <button
                key={config.id}
                onClick={() => {
                  setTheme(config.id);
                  setIsOpen(false);
                }}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-all text-left ${
                  isSelected
                    ? "bg-brand-600/20 text-brand-300 font-bold border border-brand-500/30"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <span className="text-sm">{config.icon}</span>
                  <div>
                    <p className="leading-tight">{config.name}</p>
                    <p className="text-[10px] text-slate-400 font-normal leading-tight">
                      {config.description}
                    </p>
                  </div>
                </div>

                {isSelected && <Check className="w-4 h-4 text-brand-400" />}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};
