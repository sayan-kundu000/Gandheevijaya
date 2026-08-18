import React from "react";
import { AppShell } from "../../components/layout/AppShell";
import { BhagavadGeetaSection } from "../../components/common/BhagavadGeetaSection";
import { Sparkles, BookOpen, Compass, Award, ShieldCheck } from "lucide-react";
import { Card, CardHeader, CardTitle } from "../../components/ui/Card";

export const BhagavadGeetaPortalPage: React.FC = () => {
  return (
    <AppShell title="Bhagavad Geeta Student Portal">
      <div className="space-y-6 max-w-7xl mx-auto pb-12">
        {/* Portal Header */}
        <div className="relative rounded-2xl bg-gradient-to-r from-amber-950/80 via-slate-900 to-amber-900/60 p-6 md:p-10 border border-amber-500/30 shadow-2xl overflow-hidden">
          <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
          
          <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="space-y-2 max-w-3xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-semibold uppercase tracking-wider">
                <Sparkles className="w-3.5 h-3.5" />
                Dedicated Student Philosophy Portal
              </div>
              <h1 className="text-2xl md:text-4xl font-extrabold text-slate-100 tracking-tight font-serif">
                Bhagavad Geeta: Rational Philosophy & Mindset for Competitive Exams
              </h1>
              <p className="text-sm md:text-base text-slate-300 leading-relaxed">
                A secular, realist synthesis of the 18 chapters and 23 student-focused modules. Master anxiety management, process orientation, emotional stability, and metacognition for GATE, SSC, Banking, and high-stakes tests.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-3 w-full md:w-auto shrink-0">
              <div className="p-3 rounded-xl bg-slate-900/80 border border-amber-500/20 text-center">
                <p className="text-xl font-bold text-amber-400">23</p>
                <p className="text-[11px] text-slate-400 uppercase tracking-wider font-medium">Modules</p>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/80 border border-amber-500/20 text-center">
                <p className="text-xl font-bold text-emerald-400">14</p>
                <p className="text-[11px] text-slate-400 uppercase tracking-wider font-medium">Competencies</p>
              </div>
            </div>
          </div>
        </div>

        {/* The Full Bhagavad Geeta Interactive Portal Component */}
        <BhagavadGeetaSection />
      </div>
    </AppShell>
  );
};
