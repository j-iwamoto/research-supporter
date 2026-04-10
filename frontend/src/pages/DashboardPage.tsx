import { Link } from "react-router-dom";
import { ArrowRight, FileText } from "lucide-react";
import { Dashboard } from "@/components/dashboard/Dashboard";
import { useDashboard } from "@/hooks/useDashboard";
import { useLogs } from "@/hooks/useLogs";
import { usePageTitle } from "@/hooks/usePageTitle";
import { EmptyState } from "@/components/ui/EmptyState";

const categoryColors: Record<string, string> = {
  実験: "bg-blue-100 text-blue-800",
  論文読み: "bg-green-100 text-green-800",
  コーディング: "bg-purple-100 text-purple-800",
  ミーティング: "bg-orange-100 text-orange-800",
  執筆: "bg-red-100 text-red-800",
  その他: "bg-gray-100 text-gray-800",
};

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleString("ja-JP", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function DashboardPage() {
  usePageTitle("ダッシュボード");
  const { summary, loading, error } = useDashboard();
  const { logs, loading: logsLoading } = useLogs();

  const recentLogs = logs.slice(0, 5);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-foreground">ダッシュボード</h2>
      <Dashboard summary={summary} loading={loading} error={error} />

      {/* 直近の記録 */}
      <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-medium text-foreground">直近の記録</h3>
          <Link
            to="/logs"
            className="inline-flex items-center gap-1 text-sm text-primary hover:underline"
          >
            すべて表示
            <ArrowRight className="h-3 w-3" />
          </Link>
        </div>

        {logsLoading && recentLogs.length === 0 ? (
          <div className="flex items-center justify-center py-6">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-primary border-t-transparent" />
            <span className="ml-2 text-sm text-muted-foreground">読み込み中...</span>
          </div>
        ) : recentLogs.length === 0 ? (
          <EmptyState
            icon={FileText}
            title="まだ記録がありません"
            description="日報ページから研究活動を記録しましょう"
          />
        ) : (
          <div className="space-y-2">
            {recentLogs.map((log) => (
              <div
                key={log.id}
                className="flex items-center gap-3 rounded-md bg-muted/50 px-3 py-2"
              >
                <span
                  className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ${categoryColors[log.category] ?? "bg-gray-100 text-gray-800"}`}
                >
                  {log.category}
                </span>
                <span className="min-w-0 flex-1 truncate text-sm text-foreground">
                  {log.content}
                </span>
                <span className="shrink-0 text-xs text-muted-foreground">
                  {formatDate(log.created_at)}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
