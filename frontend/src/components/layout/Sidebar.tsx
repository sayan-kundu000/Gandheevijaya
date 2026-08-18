import React from "react";
import { NavLink, Link } from "react-router-dom";
import { clsx } from "clsx";
import {
  LayoutDashboard,
  GraduationCap,
  BookOpen,
  Award,
  BarChart3,
  Users,
  FileQuestion,
  LogOut,
  ShieldAlert,
  User,
  Sparkles,
} from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import { BrandLogo } from "./BrandLogo";

export const Sidebar: React.FC = () => {
  const { user, logout } = useAuth();
  const isAdmin = user?.role === "ADMIN";

  const studentLinks = [
    { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { to: "/exams", label: "Exams & Subjects", icon: GraduationCap },
    { to: "/quizzes", label: "Quizzes", icon: BookOpen },
    { to: "/results", label: "Attempt History", icon: Award },
    { to: "/analytics", label: "Learning Analytics", icon: BarChart3 },
    { to: "/profile", label: "Profile", icon: User },
  ];

  const adminLinks = [
    { to: "/admin", label: "Admin Overview", icon: ShieldAlert },
    { to: "/admin/users", label: "User Management", icon: Users },
    { to: "/admin/questions", label: "Question Bank", icon: FileQuestion },
  ];

  return (
    <aside className="hidden lg:flex flex-col w-64 border-r border-slate-800 bg-slate-900/90 backdrop-blur-md min-h-screen sticky top-0">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800">
        <BrandLogo />
      </div>

      {/* Navigation Links */}
      <div className="flex-1 px-3 py-4 space-y-6 overflow-y-auto">
        <div>
          <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
            Student Space
          </p>
          <nav className="space-y-1">
            {studentLinks.map((link) => {
              const Icon = link.icon;
              return (
                <NavLink
                  key={link.to}
                  to={link.to}
                  className={({ isActive }) =>
                    clsx(
                      "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                      isActive
                        ? "bg-brand-600/15 text-brand-400 font-semibold"
                        : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                    )
                  }
                >
                  <Icon className="w-4 h-4" />
                  <span>{link.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        {isAdmin && (
          <div>
            <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              Admin Governance
            </p>
            <nav className="space-y-1">
              {adminLinks.map((link) => {
                const Icon = link.icon;
                return (
                  <NavLink
                    key={link.to}
                    to={link.to}
                    className={({ isActive }) =>
                      clsx(
                        "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                        isActive
                          ? "bg-rose-500/15 text-rose-400 font-semibold"
                          : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                      )
                    }
                  >
                    <Icon className="w-4 h-4" />
                    <span>{link.label}</span>
                  </NavLink>
                );
              })}
            </nav>
          </div>
        )}
      </div>

      {/* User Footer */}
      <div className="p-4 border-t border-slate-800">
        <div className="flex items-center justify-between">
          <Link to="/profile" className="flex items-center gap-2.5 overflow-hidden group">
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-semibold text-xs text-brand-400 shrink-0 group-hover:border-brand-500">
              {user?.full_name?.charAt(0) || "U"}
            </div>
            <div className="truncate">
              <p className="text-xs font-semibold text-slate-200 truncate group-hover:text-brand-300">
                {user?.full_name}
              </p>
              <p className="text-[11px] text-slate-500 capitalize">{user?.role?.toLowerCase()}</p>
            </div>
          </Link>
          <button
            onClick={logout}
            title="Log out"
            className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-950/20 transition-colors"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Bhagavad Geeta Dedicated Portal Box at the Very Bottom (Replacing White Bordered Box) */}
      <div className="p-3 border-t border-slate-800 bg-slate-950/90">
        <NavLink
          to="/gita"
          className={({ isActive }) =>
            clsx(
              "flex items-center gap-3 p-3 rounded-xl border transition-all shadow-lg group relative overflow-hidden",
              isActive
                ? "bg-gradient-to-r from-amber-950/80 via-slate-900 to-amber-950/60 border-amber-400 shadow-amber-500/10"
                : "bg-slate-900/90 border-slate-800 hover:border-amber-500/50 hover:bg-slate-900 hover:shadow-amber-500/10"
            )
          }
        >
          <div className="w-8 h-8 rounded-lg bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0 group-hover:scale-105 transition-transform">
            <Sparkles className="w-4 h-4 animate-pulse" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-bold text-amber-300 font-serif tracking-wide truncate group-hover:text-amber-200">
              Bhagavad Geeta
            </p>
            <p className="text-[10px] font-medium text-amber-400/80 truncate">
              Student Philosophy Portal →
            </p>
          </div>
        </NavLink>
      </div>
    </aside>
  );
};

