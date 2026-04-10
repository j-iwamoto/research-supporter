import { useAuth } from "@/contexts/AuthContext";

export function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-background px-6">
      <h1 className="text-lg font-semibold">研究タスク管理AI</h1>
      <div className="flex items-center gap-4">
        {user && (
          <>
            <span className="text-sm text-muted-foreground">
              {user.displayName}
            </span>
            <button
              onClick={logout}
              className="text-sm text-muted-foreground hover:text-foreground"
            >
              ログアウト
            </button>
          </>
        )}
      </div>
    </header>
  );
}
