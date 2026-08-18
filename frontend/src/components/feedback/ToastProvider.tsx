import React, { createContext, useContext, useState, useCallback } from "react";
import { CheckCircle2, AlertCircle, Info, AlertTriangle, X } from "lucide-react";

export type ToastType = "success" | "error" | "info" | "warning";

export interface ToastItem {
  id: string;
  type: ToastType;
  title?: string;
  message: string;
}

interface ToastContextType {
  toast: (item: Omit<ToastItem, "id">) => void;
  success: (message: string, title?: string) => void;
  error: (message: string, title?: string) => void;
  info: (message: string, title?: string) => void;
  warning: (message: string, title?: string) => void;
  removeToast: (id: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toast = useCallback(
    ({ type, title, message }: Omit<ToastItem, "id">) => {
      const id = Math.random().toString(36).substring(2, 9);
      setToasts((prev) => [...prev, { id, type, title, message }]);
      setTimeout(() => {
        removeToast(id);
      }, 4000);
    },
    [removeToast]
  );

  const success = useCallback((message: string, title?: string) => toast({ type: "success", title, message }), [toast]);
  const error = useCallback((message: string, title?: string) => toast({ type: "error", title, message }), [toast]);
  const info = useCallback((message: string, title?: string) => toast({ type: "info", title, message }), [toast]);
  const warning = useCallback((message: string, title?: string) => toast({ type: "warning", title, message }), [toast]);

  return (
    <ToastContext.Provider value={{ toast, success, error, info, warning, removeToast }}>
      {children}
      {/* Fixed Toast Container */}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2.5 max-w-sm w-full pointer-events-none px-4">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`pointer-events-auto p-4 rounded-xl border shadow-xl flex items-start justify-between gap-3 text-xs transition-all transform animate-in slide-in-from-bottom-2 ${
              t.type === "success"
                ? "bg-slate-900 border-emerald-500/40 text-emerald-300"
                : t.type === "error"
                ? "bg-slate-900 border-rose-500/40 text-rose-300"
                : t.type === "warning"
                ? "bg-slate-900 border-amber-500/40 text-amber-300"
                : "bg-slate-900 border-sky-500/40 text-sky-300"
            }`}
          >
            <div className="flex items-start gap-2.5">
              {t.type === "success" && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />}
              {t.type === "error" && <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />}
              {t.type === "warning" && <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />}
              {t.type === "info" && <Info className="w-4 h-4 text-sky-400 shrink-0" />}
              <div className="space-y-0.5">
                {t.title && <h5 className="font-bold text-sm text-slate-100">{t.title}</h5>}
                <p className="text-slate-300">{t.message}</p>
              </div>
            </div>
            <button
              onClick={() => removeToast(t.id)}
              className="text-slate-400 hover:text-slate-200 transition-colors p-0.5"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within ToastProvider");
  }
  return context;
};
