import { FileText, Lightbulb, BarChart3, Sparkles } from "lucide-react";
import type { DashboardSummary } from "@/types";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { WeeklyChart } from "@/components/dashboard/WeeklyChart";

interface DashboardProps {
  summary: DashboardSummary | null;
  loading: boolean;
  error: string | null;
}

const categoryLabels: Record<string, string> = {
  実験: "実験",
  論文読み: "論文読み",
  コーディング: "コーディング",
  ミーティング: "ミーティング",
  執筆: "執筆",
  その他: "その他",
};

export function Dashboard({ summary, loading, error }: DashboardProps) {
  if (loading && !summary) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
        <span className="ml-2 text-sm text-muted-foreground">読み込み中...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-destructive/10 px-4 py-3 text-sm text-destructive">
        {error}
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="rounded-lg border border-dashed border-border py-12 text-center">
        <p className="text-sm text-muted-foreground">データがありません</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 統計カード */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <StatsCard
          title="今週の記録数"
          value={summary.totalLogsThisWeek}
          subtext="件の研究活動"
          icon={FileText}
        />
        <StatsCard
          title="アイデア数"
          value={summary.totalIdeas}
          subtext={`採用: ${summary.ideaStatusCounts["採用"] ?? 0}件`}
          icon={Lightbulb}
        />
        <StatsCard
          title="カテゴリ数"
          value={Object.values(summary.categoryCounts).filter((c) => c > 0).length}
          subtext="種類の活動"
          icon={BarChart3}
        />
      </div>

      {/* カテゴリ別カウント */}
      <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
        <h3 className="mb-3 text-sm font-medium text-foreground">カテゴリ別記録数</h3>
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
          {Object.entries(summary.categoryCounts).map(([category, count]) => (
            <div
              key={category}
              className="flex items-center justify-between rounded-md bg-muted/50 px-3 py-2"
            >
              <span className="text-sm text-foreground">
                {categoryLabels[category] ?? category}
              </span>
              <span className="text-sm font-semibold text-foreground">{count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 週次推移チャート */}
      {summary.weeklyTrend.length > 0 && (
        <WeeklyChart data={summary.weeklyTrend} />
      )}

      {/* AIからの提案 */}
      {summary.aiSuggestion && (
        <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
          <div className="flex items-start gap-3">
            <div className="rounded-md bg-primary/10 p-2">
              <Sparkles className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="text-sm font-medium text-foreground">AIからの提案</h3>
              <p className="mt-1 whitespace-pre-wrap text-sm text-muted-foreground">
                {summary.aiSuggestion}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
