import React from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { BowArrowGLogo } from "../common/BowArrowGLogo";
import {
  LayoutDashboard,
  Users,
  ShieldCheck,
  FileQuestion,
  GraduationCap,
  Database,
  BarChart3,
  LogOut,
  Sparkles,
} from "lucide-react";

export const AdminSidebar: React.FC = () => {
  const { user, logout } = useAuth();

  const navGroups = [
    {
      title: "Governance & CMS",
      items: [
        { name: "Overview", path: "/admin", icon: LayoutDashboard },
        { name: "User Management", path: "/admin/users", icon: Users },
        { name: "Security Audit Logs", path: "/admin/audit-logs", icon: ShieldCheck },
      ],
    },
    {
      title: "Question Bank & Content",
      items: [
        { name: "Question Pool", path: "/admin/questions", icon: FileQuestion },
        { name: "Taxonomy & Exams", path: "/admin/taxonomy", icon: GraduationCap },
        { name: "Data Ingestion (ETL)", path: "/admin/etl", icon: Database },
      ],
    },
    {
      title: "Analytics & System",
      items: [
        { name: "System Metrics", path: "/admin/analytics", icon: BarChart3 },
      ],
    },
  ];

  return (
    <aside className="hidden lg:flex flex-col w-64 border-r border-rose-900/30 bg-slate-950/95 backdrop-blur-md min-h-screen sticky top-0">
      {/* Brand Header */}
      <div className="flex items-center gap-3 p-5 border-b border-slate-800 bg-rose-950/20">
        <div className="w-9 h-9 rounded-xl bg-slate-900 flex items-center justify-center p-1.5 border border-rose-500/40 shadow-lg shadow-rose-500/20">
          <BowArrowGLogo
            className="w-full h-full"
            bowColor="#fbbf24"
            arrowColor="#f43f5e"
            glowColor="rgba(244,63,94,0.6)"
          />
        </div>
        <div>
          <h1 className="text-base font-bold tracking-tight text-white">Gandheevijaya</h1>
          <p className="text-xs text-rose-400 font-semibold uppercase tracking-wider">Admin Control</p>
        </div>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 px-3 py-4 space-y-6 overflow-y-auto">
        {navGroups.map((group, groupIdx) => (
          <div key={groupIdx}>
            <p className="px-3 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              {group.title}
            </p>
            <nav className="space-y-1">
              {group.items.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    end={item.path === "/admin"}
                    className={({ isActive }) =>
                      `flex items-center gap-3 px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${
                        isActive
                          ? "bg-rose-600/20 text-rose-300 border border-rose-500/30"
                          : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/60"
                      }`
                    }
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.name}</span>
                  </NavLink>
                );
              })}
            </nav>
          </div>
        ))}
      </div>

      {/* User Footer */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-900/40">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 overflow-hidden">
            <div className="w-8 h-8 rounded-full bg-rose-500/20 border border-rose-500/30 flex items-center justify-center text-rose-300 font-bold text-xs">
              {user?.full_name?.charAt(0) || "A"}
            </div>
            <div className="truncate">
              <p className="text-xs font-semibold text-slate-200 truncate">{user?.full_name}</p>
              <span className="inline-flex items-center gap-1 text-[10px] text-rose-400 font-mono">
                <Sparkles className="w-3 h-3" /> ADMIN
              </span>
            </div>
          </div>
          <button
            type="button"
            onClick={logout}
            className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors"
            title="Log out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
};
