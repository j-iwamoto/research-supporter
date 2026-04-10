import { useState, useMemo } from "react";
import { FileText } from "lucide-react";
import { LogForm } from "@/components/logs/LogForm";
import { LogList } from "@/components/logs/LogList";
import { useLogs } from "@/hooks/useLogs";
import { usePageTitle } from "@/hooks/usePageTitle";
import { EmptyState } from "@/components/ui/EmptyState";
import type { Log } from "@/types";

type WeekFilter = "this-week" | "last-week" | "all";
type CategoryFilter = Log["category"] | "all";

const CATEGORIES: { value: CategoryFilter; label: string }[] = [
  { value: "all", label: "すべて" },
  { value: "実験", label: "実験" },
  { value: "論文読み", label: "論文読み" },
  { value: "コーディング", label: "コーディング" },
  { value: "ミーティング", label: "ミーティング" },
  { value: "執筆", label: "執筆" },
  { value: "その他", label: "その他" },
];

function getWeekRange(offset: number): { start: Date; end: Date } {
  const now = new Date();
  const dayOfWeek = now.getDay();
  // 月曜始まり
  const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
  const start = new Date(now);
  start.setDate(now.getDate() + mondayOffset + offset * 7);
  start.setHours(0, 0, 0, 0);
  const end = new Date(start);
  end.setDate(start.getDate() + 7);
  return { start, end };
}

export function LogsPage() {
  usePageTitle("日報");
  const { logs, loading, error, createLog, deleteLog } = useLogs();
  const [weekFilter, setWeekFilter] = useState<WeekFilter>("all");
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>("all");

  const filteredLogs = useMemo(() => {
    let result = logs;

    // 週フィルタ
    if (weekFilter !== "all") {
      const offset = weekFilter === "this-week" ? 0 : -1;
      const { start, end } = getWeekRange(offset);
      result = result.filter((log) => {
        const d = new Date(log.created_at);
        return d >= start && d < end;
      });
    }

    // カテゴリフィルタ
    if (categoryFilter !== "all") {
      result = result.filter((log) => log.category === categoryFilter);
    }

    return result;
  }, [logs, weekFilter, categoryFilter]);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-foreground">日報</h2>

      <LogForm onSubmit={createLog} loading={loading} />

      {error && (
        <div className="rounded-md bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {error}
        </div>
      )}

      {/* フィルタ */}
      <div className="flex flex-wrap items-center gap-3">
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-foreground">期間:</label>
          <select
            value={weekFilter}
            onChange={(e) => setWeekFilter(e.target.value as WeekFilter)}
            className="rounded-md border border-input bg-background px-3 py-1.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="all">すべて</option>
            <option value="this-week">今週</option>
            <option value="last-week">先週</option>
          </select>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-foreground">カテゴリ:</label>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value as CategoryFilter)}
            className="rounded-md border border-input bg-background px-3 py-1.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {CATEGORIES.map((cat) => (
              <option key={cat.value} value={cat.value}>
                {cat.label}
              </option>
            ))}
          </select>
        </div>
        {(weekFilter !== "all" || categoryFilter !== "all") && (
          <span className="text-xs text-muted-foreground">
            {filteredLogs.length}件表示
          </span>
        )}
      </div>

      <div>
        <h3 className="mb-3 text-lg font-semibold text-foreground">記録一覧</h3>
        {filteredLogs.length === 0 && !loading ? (
          <EmptyState
            icon={FileText}
            title="記録がありません"
            description="上のフォームから研究活動を記録しましょう"
          />
        ) : (
          <LogList logs={filteredLogs} loading={loading} onDelete={deleteLog} />
        )}
      </div>
    </div>
  );
}
