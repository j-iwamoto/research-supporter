import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { usePageTitle } from "@/hooks/usePageTitle";

export function LoginPage() {
  usePageTitle("ログイン");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    await login();
    navigate("/");
  };

  return (
    <div className="flex h-screen items-center justify-center bg-background">
      <div className="w-full max-w-sm space-y-6 rounded-lg border border-border p-8 shadow-sm">
        <div className="space-y-2 text-center">
          <h1 className="text-2xl font-bold text-foreground">研究タスク管理AI</h1>
          <p className="text-sm text-muted-foreground">
            Googleアカウントでログインしてください
          </p>
        </div>
        <button
          onClick={handleLogin}
          className="flex w-full items-center justify-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          Googleでログイン
        </button>
      </div>
    </div>
  );
}
