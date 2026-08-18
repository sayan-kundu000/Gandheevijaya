import React, { Component, ErrorInfo, ReactNode } from "react";
import { AlertCircle, RefreshCw, Home } from "lucide-react";
import { Button } from "../ui/Button";
import { Card } from "../ui/Card";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Gandheevijaya React ErrorBoundary caught an exception:", error, errorInfo);
  }

  private handleReload = () => {
    window.location.reload();
  };

  private handleGoHome = () => {
    window.location.href = "/dashboard";
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-6">
          <Card className="max-w-md w-full p-6 text-center space-y-4 border-rose-500/30">
            <div className="mx-auto w-12 h-12 rounded-full bg-rose-500/10 text-rose-400 flex items-center justify-center border border-rose-500/20">
              <AlertCircle className="w-6 h-6" />
            </div>

            <div className="space-y-1">
              <h3 className="text-lg font-bold text-slate-100">Something Went Wrong</h3>
              <p className="text-xs text-slate-400">
                Gandheevijaya encountered an unexpected rendering error.
              </p>
            </div>

            {this.state.error?.message && (
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-[11px] font-mono text-rose-300 text-left overflow-x-auto">
                {this.state.error.message}
              </div>
            )}

            <div className="flex items-center justify-center gap-3 pt-2">
              <Button
                variant="outline"
                size="sm"
                leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
                onClick={this.handleReload}
              >
                Reload Page
              </Button>

              <Button
                variant="primary"
                size="sm"
                leftIcon={<Home className="w-3.5 h-3.5" />}
                onClick={this.handleGoHome}
              >
                Go to Dashboard
              </Button>
            </div>
          </Card>
        </div>
      );
    }

    return this.props.children;
  }
}
