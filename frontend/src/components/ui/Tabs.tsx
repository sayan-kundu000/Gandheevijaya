import React from "react";
import { clsx } from "clsx";

export interface TabItem {
  id: string;
  label: string;
  badge?: number | string;
}

export interface TabsProps {
  tabs: TabItem[];
  activeTab: string;
  onChange: (tabId: string) => void;
}

export const Tabs: React.FC<TabsProps> = ({ tabs, activeTab, onChange }) => {
  return (
    <div className="flex border-b border-slate-800 gap-2 overflow-x-auto no-scrollbar">
      {tabs.map((tab) => {
        const isActive = tab.id === activeTab;
        return (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={clsx(
              "flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors whitespace-nowrap",
              isActive
                ? "border-brand-500 text-brand-400 bg-brand-500/5"
                : "border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700"
            )}
          >
            <span>{tab.label}</span>
            {tab.badge !== undefined && (
              <span
                className={clsx(
                  "px-1.5 py-0.5 text-xs rounded-full",
                  isActive ? "bg-brand-500/20 text-brand-300" : "bg-slate-800 text-slate-400"
                )}
              >
                {tab.badge}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
};
