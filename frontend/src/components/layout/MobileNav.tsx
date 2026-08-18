import React from "react";
import { NavLink } from "react-router-dom";
import { clsx } from "clsx";
import { LayoutDashboard, GraduationCap, BookOpen, Award, BarChart3 } from "lucide-react";

export const MobileNav: React.FC = () => {
  const navItems = [
    { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { to: "/exams", label: "Exams", icon: GraduationCap },
    { to: "/quizzes", label: "Quizzes", icon: BookOpen },
    { to: "/results", label: "History", icon: Award },
    { to: "/analytics", label: "Analytics", icon: BarChart3 },
  ];

  return (
    <nav className="lg:hidden fixed bottom-0 left-0 right-0 h-16 border-t border-slate-800 bg-slate-950/95 backdrop-blur-lg z-30 flex items-center justify-around px-2">
      {navItems.map((item) => {
        const Icon = item.icon;
        return (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              clsx(
                "flex flex-col items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors",
                isActive ? "text-brand-400 font-semibold" : "text-slate-500 hover:text-slate-300"
              )
            }
          >
            <Icon className="w-5 h-5" />
            <span className="text-[10px]">{item.label}</span>
          </NavLink>
        );
      })}
    </nav>
  );
};
