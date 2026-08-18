import React, { useState, useRef, useEffect } from "react";
import { ChevronDown } from "lucide-react";

export interface DropdownItem {
  key: string;
  label: React.ReactNode;
  icon?: React.ReactNode;
  danger?: boolean;
  onClick: () => void;
}

interface DropdownProps {
  trigger: React.ReactNode;
  items: DropdownItem[];
  align?: "left" | "right";
  className?: string;
}

export const Dropdown: React.FC<DropdownProps> = ({
  trigger,
  items,
  align = "right",
  className = "",
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className={`relative inline-block text-left ${className}`} ref={containerRef}>
      <div onClick={() => setIsOpen((prev) => !prev)}>{trigger}</div>

      {isOpen && (
        <div
          className={`absolute z-30 mt-2 w-48 rounded-xl bg-slate-900 border border-slate-800 shadow-2xl py-1 focus:outline-none ${
            align === "right" ? "right-0" : "left-0"
          }`}
        >
          {items.map((item) => (
            <button
              key={item.key}
              onClick={() => {
                item.onClick();
                setIsOpen(false);
              }}
              className={`w-full text-left px-3.5 py-2 text-xs font-medium flex items-center gap-2 transition-colors ${
                item.danger
                  ? "text-rose-400 hover:bg-rose-500/10 hover:text-rose-300"
                  : "text-slate-300 hover:bg-slate-800 hover:text-slate-100"
              }`}
            >
              {item.icon}
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
