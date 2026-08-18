import React from "react";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";
import { MobileNav } from "./MobileNav";

export interface AppShellProps {
  title?: string;
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ title, children }) => {
  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 antialiased">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 pb-16 lg:pb-0">
        <Topbar title={title} />
        <main className="flex-1 p-4 md:p-6 lg:p-8 max-w-7xl w-full mx-auto animate-in fade-in duration-200">
          {children}
        </main>
      </div>
      <MobileNav />
    </div>
  );
};
