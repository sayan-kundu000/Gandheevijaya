import React from "react";
import { AdminSidebar } from "./AdminSidebar";
import { Topbar } from "./Topbar";

export interface AdminAppShellProps {
  title?: string;
  children: React.ReactNode;
}

export const AdminAppShell: React.FC<AdminAppShellProps> = ({ title = "Admin Governance", children }) => {
  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 antialiased font-sans">
      <AdminSidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Topbar title={`[ADMIN] ${title}`} />
        <main className="flex-1 p-4 md:p-6 lg:p-8 max-w-7xl w-full mx-auto animate-in fade-in duration-200 space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
};
