import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { authApi } from "../../services/authApi";
import { useAuth } from "../../context/AuthContext";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { UserPlus, Check, GraduationCap } from "lucide-react";

const registerSchema = z.object({
  full_name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type RegisterForm = z.infer<typeof registerSchema>;

const EXAM_CHOICES = [
  { id: "GATE_CS", label: "GATE CS", badge: "Engineering" },
  { id: "SSC_GK", label: "SSC CGL / GK", badge: "Govt / SSC" },
  { id: "BANKING", label: "Banking (IBPS PO / SBI PO)", badge: "Banking" },
  { id: "APTITUDE", label: "Aptitude & Reasoning", badge: "General" },
];

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [selectedExams, setSelectedExams] = useState<string[]>(["GATE_CS"]);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
  });

  const toggleExam = (id: string) => {
    setSelectedExams((prev) => {
      if (prev.includes(id)) {
        if (prev.length === 1) return prev; // At least one
        return prev.filter((item) => item !== id);
      } else {
        return [...prev, id];
      }
    });
  };

  const onSubmit = async (data: RegisterForm) => {
    setErrorMsg(null);
    try {
      const tokens = await authApi.register({
        ...data,
        target_exams: selectedExams,
      });
      login(tokens);
      navigate("/dashboard");
    } catch (err: any) {
      const msg =
        err.response?.data?.error?.message ||
        err.response?.data?.detail ||
        "Registration failed. Email may already exist.";
      setErrorMsg(msg);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-600 to-accent-500 text-white font-bold text-xl shadow-xl shadow-brand-500/20 mb-2">
            G
          </div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Create Account</h1>
          <p className="text-sm text-slate-400">Join Gandheevijaya for GATE CS, SSC & Banking Prep</p>
        </div>

        <Card className="p-6">
          {errorMsg && (
            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-medium mb-4">
              {errorMsg}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <Input
              label="Full Name"
              placeholder="Student Name"
              error={errors.full_name?.message}
              {...register("full_name")}
            />

            <Input
              label="Email Address"
              type="email"
              placeholder="student@example.com"
              error={errors.email?.message}
              {...register("email")}
            />

            <Input
              label="Password"
              type="password"
              placeholder="Minimum 8 characters"
              error={errors.password?.message}
              {...register("password")}
            />

            {/* Target Exam Multi-Select Options */}
            <div className="space-y-2 pt-1">
              <label className="text-xs font-medium text-slate-300 flex items-center justify-between">
                <span className="flex items-center gap-1.5">
                  <GraduationCap className="w-3.5 h-3.5 text-brand-400" />
                  Target Exams (Choose Multiple)
                </span>
                <span className="text-[11px] text-slate-500">{selectedExams.length} selected</span>
              </label>

              <div className="grid grid-cols-2 gap-2">
                {EXAM_CHOICES.map((choice) => {
                  const isChecked = selectedExams.includes(choice.id);
                  return (
                    <button
                      type="button"
                      key={choice.id}
                      onClick={() => toggleExam(choice.id)}
                      className={`p-2.5 rounded-xl border text-left text-xs transition-all flex items-center justify-between gap-2 ${
                        isChecked
                          ? "bg-brand-950/40 border-brand-500 text-slate-100 ring-1 ring-brand-500/30"
                          : "bg-slate-900/40 border-slate-800 text-slate-400 hover:border-slate-700"
                      }`}
                    >
                      <div className="truncate">
                        <p className="font-semibold truncate">{choice.label}</p>
                        <p className="text-[10px] text-slate-500">{choice.badge}</p>
                      </div>
                      <div
                        className={`w-4 h-4 rounded flex items-center justify-center shrink-0 border ${
                          isChecked ? "bg-brand-600 border-brand-500 text-white" : "border-slate-700"
                        }`}
                      >
                        {isChecked && <Check className="w-3 h-3 stroke-[3]" />}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            <Button
              type="submit"
              variant="primary"
              className="w-full mt-3"
              isLoading={isSubmitting}
              leftIcon={<UserPlus className="w-4 h-4" />}
            >
              Create Account
            </Button>
          </form>

          <div className="mt-6 border-t border-slate-800 pt-4 text-center">
            <p className="text-xs text-slate-400">
              Already have an account?{" "}
              <Link to="/login" className="text-brand-400 hover:text-brand-300 font-semibold">
                Sign in
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};
