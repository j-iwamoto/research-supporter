import { LogItem } from "@/components/logs/LogItem";
import type { Log } from "@/types";

interface LogListProps {
  logs: Log[];
  loading: boolean;
  onDelete: (id: string) => void;
}

export function LogList({ logs, loading, onDelete }: LogListProps) {
  if (loading && logs.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
        <span className="ml-2 text-sm text-muted-foreground">読み込み中...</span>
      </div>
    );
  }

  if (logs.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-border py-12 text-center">
        <p className="text-sm text-muted-foreground">
          まだ記録がありません
        </p>
        <p className="mt-1 text-xs text-muted-foreground">
          上のフォームから研究活動を記録しましょう
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {logs.map((log) => (
        <LogItem key={log.id} log={log} onDelete={onDelete} />
      ))}
    </div>
  );
}
