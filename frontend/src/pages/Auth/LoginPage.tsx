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
import { LogIn, Sparkles } from "lucide-react";

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
});

type LoginForm = z.infer<typeof loginSchema>;

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginForm) => {
    setErrorMsg(null);
    try {
      const tokens = await authApi.login({ email: data.email, password: data.password });
      login(tokens);
      navigate("/dashboard");
    } catch (err: any) {
      const msg =
        err.response?.data?.error?.message ||
        err.response?.data?.detail ||
        (!err.response
          ? "Unable to connect to backend server. Please ensure the backend API server is running on http://localhost:8000."
          : "Invalid email or password");
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
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Welcome Back</h1>
          <p className="text-sm text-slate-400">Log in to Gandheevijaya Assessment Portal</p>
        </div>

        <Card className="p-6">
          {errorMsg && (
            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-medium mb-4">
              {errorMsg}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
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
              placeholder="••••••••"
              error={errors.password?.message}
              {...register("password")}
            />

            <Button
              type="submit"
              variant="primary"
              className="w-full mt-2"
              isLoading={isSubmitting}
              leftIcon={<LogIn className="w-4 h-4" />}
            >
              Sign In
            </Button>
          </form>

          {/* Quick Demo Login Credentials */}
          <div className="mt-4 pt-4 border-t border-slate-800 space-y-2">
            <p className="text-xs font-semibold text-slate-400 text-center">Quick Demo Login</p>
            <div className="grid grid-cols-2 gap-2">
              <Button
                type="button"
                variant="outline"
                size="sm"
                className="text-xs"
                onClick={async () => {
                  setErrorMsg(null);
                  setValue("email", "admin@gandheevijaya.com");
                  setValue("password", "AdminPassword123!");
                  try {
                    const tokens = await authApi.login({
                      email: "admin@gandheevijaya.com",
                      password: "AdminPassword123!",
                    });
                    login(tokens);
                    navigate("/admin");
                  } catch (err: any) {
                    const msg =
                      err.response?.data?.error?.message ||
                      err.response?.data?.detail ||
                      (!err.response
                        ? "Unable to connect to backend server. Please ensure backend server is running on http://localhost:8000."
                        : "Failed to login as Admin.");
                    setErrorMsg(msg);
                  }
                }}
              >
                Log In as Admin
              </Button>
              <Button
                type="button"
                variant="outline"
                size="sm"
                className="text-xs"
                onClick={async () => {
                  setErrorMsg(null);
                  setValue("email", "student@gandheevijaya.com");
                  setValue("password", "StudentPassword123!");
                  try {
                    const tokens = await authApi.login({
                      email: "student@gandheevijaya.com",
                      password: "StudentPassword123!",
                    });
                    login(tokens);
                    navigate("/dashboard");
                  } catch (err: any) {
                    const msg =
                      err.response?.data?.error?.message ||
                      err.response?.data?.detail ||
                      (!err.response
                        ? "Unable to connect to backend server. Please ensure backend server is running on http://localhost:8000."
                        : "Failed to login as Student.");
                    setErrorMsg(msg);
                  }
                }}
              >
                Log In as Student
              </Button>
            </div>
          </div>

          <div className="mt-6 border-t border-slate-800 pt-4 text-center">
            <p className="text-xs text-slate-400">
              Don't have an account?{" "}
              <Link to="/register" className="text-brand-400 hover:text-brand-300 font-semibold">
                Register here
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};
