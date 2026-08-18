import React from "react";
import { useTheme } from "../../context/ThemeContext";
import { BowArrowGLogo } from "../common/BowArrowGLogo";

export const BrandLogo: React.FC<{ collapsed?: boolean }> = ({ collapsed = false }) => {
  const { theme } = useTheme();

  if (theme === "pink-neon") {
    return (
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-pink-900/80 via-rose-950/80 to-fuchsia-950/80 flex items-center justify-center p-1.5 shadow-[0_0_15px_rgba(236,72,153,0.6)] border border-pink-300/40">
          <BowArrowGLogo
            className="w-full h-full"
            bowColor="#f472b6"
            arrowColor="#fb7185"
            glowColor="rgba(244,114,182,0.8)"
          />
        </div>
        {!collapsed && (
          <div>
            <h1 className="text-base font-black tracking-wider text-pink-300 drop-shadow-[0_0_8px_rgba(244,114,182,0.8)] uppercase">
              Gandheevijaya
            </h1>
            <p className="text-[10px] text-fuchsia-400 font-bold uppercase tracking-widest flex items-center gap-1">
              <span>Pink Neon</span> • <span>Girls Edition</span>
            </p>
          </div>
        )}
      </div>
    );
  }

  if (theme === "blue-neon") {
    return (
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-950/80 via-blue-950/80 to-slate-950/80 flex items-center justify-center p-1.5 shadow-[0_0_15px_rgba(6,182,212,0.6)] border border-cyan-300/40">
          <BowArrowGLogo
            className="w-full h-full"
            bowColor="#22d3ee"
            arrowColor="#38bdf8"
            glowColor="rgba(34,211,238,0.8)"
          />
        </div>
        {!collapsed && (
          <div>
            <h1 className="text-base font-black tracking-wider text-cyan-300 drop-shadow-[0_0_8px_rgba(34,211,238,0.8)] uppercase font-mono">
              Gandheevijaya
            </h1>
            <p className="text-[10px] text-sky-400 font-bold uppercase tracking-widest flex items-center gap-1 font-mono">
              <span>Blue Neon</span> • <span>Boys Edition</span>
            </p>
          </div>
        )}
      </div>
    );
  }

  if (theme === "supernatural") {
    return (
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-950/90 via-red-950/90 to-black flex items-center justify-center p-1.5 border-2 border-amber-500/60 shadow-[0_0_15px_rgba(217,119,6,0.5)]">
          <BowArrowGLogo
            className="w-full h-full"
            bowColor="#fbbf24"
            arrowColor="#f97316"
            glowColor="rgba(245,158,11,0.8)"
          />
        </div>
        {!collapsed && (
          <div>
            <h1 className="text-base font-serif font-black tracking-widest text-amber-400 drop-shadow-[0_0_8px_rgba(245,158,11,0.6)] uppercase">
              Gandheevijaya
            </h1>
            <p className="text-[10px] text-amber-600/90 font-serif font-bold uppercase tracking-widest flex items-center gap-1">
              <span>Supernatural</span> • <span>Hunters 🔯</span>
            </p>
          </div>
        )}
      </div>
    );
  }

  if (theme === "light") {
    return (
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-indigo-50/90 flex items-center justify-center p-1.5 shadow-md shadow-indigo-100 border border-indigo-200">
          <BowArrowGLogo
            className="w-full h-full"
            bowColor="#4f46e5"
            arrowColor="#0284c7"
          />
        </div>
        {!collapsed && (
          <div>
            <h1 className="text-base font-bold tracking-tight text-slate-900">Gandheevijaya</h1>
            <p className="text-xs text-slate-500 font-medium">GATE • SSC • Banking</p>
          </div>
        )}
      </div>
    );
  }

  // Default Dark Mode Logo
  return (
    <div className="flex items-center gap-3">
      <div className="w-9 h-9 rounded-xl bg-slate-900/90 flex items-center justify-center p-1.5 border border-brand-500/40 shadow-lg shadow-brand-500/20">
        <BowArrowGLogo
          className="w-full h-full"
          bowColor="#fbbf24"
          arrowColor="#38bdf8"
          glowColor="rgba(251,191,36,0.6)"
        />
      </div>
      {!collapsed && (
        <div>
          <h1 className="text-base font-bold tracking-tight text-white">Gandheevijaya</h1>
          <p className="text-xs text-slate-400 font-medium">GATE • SSC • Banking</p>
        </div>
      )}
    </div>
  );
};
