import { Trash2 } from "lucide-react";
import type { Log } from "@/types";

const categoryColors: Record<Log["category"], string> = {
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

interface LogItemProps {
  log: Log;
  onDelete: (id: string) => void;
}

export function LogItem({ log, onDelete }: LogItemProps) {
  const handleDelete = () => {
    if (window.confirm("この記録を削除しますか？")) {
      onDelete(log.id);
    }
  };

  return (
    <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <p className="whitespace-pre-wrap text-sm text-foreground">
            {log.content}
          </p>

          <div className="mt-3 flex flex-wrap items-center gap-2">
            <span
              className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${categoryColors[log.category]}`}
            >
              {log.category}
            </span>

            {log.tags.map((tag) => (
              <span
                key={tag}
                className="inline-flex items-center rounded-full bg-secondary px-2.5 py-0.5 text-xs font-medium text-secondary-foreground"
              >
                {tag}
              </span>
            ))}

            <span className="ml-auto text-xs text-muted-foreground">
              {formatDate(log.createdAt)}
            </span>
          </div>
        </div>

        <button
          type="button"
          onClick={handleDelete}
          className="shrink-0 rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-destructive/10 hover:text-destructive"
          aria-label="削除"
        >
          <Trash2 className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
