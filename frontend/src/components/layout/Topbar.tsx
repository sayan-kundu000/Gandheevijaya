import React from "react";
import { useAuth } from "../../context/AuthContext";
import { Badge } from "../ui/Badge";
import { ThemeSwitcher } from "./ThemeSwitcher";
import { GraduationCap } from "lucide-react";

export interface TopbarProps {
  title?: string;
}

export const Topbar: React.FC<TopbarProps> = ({ title = "Dashboard" }) => {
  const { user } = useAuth();

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-20">
      <div className="flex items-center gap-3">
        <h2 className="text-lg font-bold text-slate-100 tracking-tight">{title}</h2>
      </div>

      <div className="flex items-center gap-3">
        {/* Interactive 5-Mode Theme Switcher */}
        <ThemeSwitcher />

        {user?.target_exam && (
          <Badge variant="brand" className="hidden md:inline-flex gap-1.5 py-1 px-3">
            <GraduationCap className="w-3.5 h-3.5" />
            <span>Target: {user.target_exam}</span>
          </Badge>
        )}

        <div className="flex items-center gap-2 border-l border-slate-800 pl-3">
          <div className="w-8 h-8 rounded-full bg-brand-600/20 border border-brand-500/30 flex items-center justify-center font-bold text-xs text-brand-300">
            {user?.full_name?.charAt(0) || "U"}
          </div>
          <span className="text-xs font-semibold text-slate-300 hidden md:inline">
            {user?.full_name}
          </span>
        </div>
      </div>
    </header>
  );
};
