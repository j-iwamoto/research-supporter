import { Trash2 } from "lucide-react";
import type { Idea } from "@/types";

const statusColors: Record<Idea["status"], string> = {
  未着手: "bg-gray-100 text-gray-800",
  検討中: "bg-yellow-100 text-yellow-800",
  採用: "bg-green-100 text-green-800",
  却下: "bg-red-100 text-red-800",
};

const allStatuses: Idea["status"][] = ["未着手", "検討中", "採用", "却下"];

interface IdeaCardProps {
  idea: Idea;
  onStatusChange: (id: string, status: Idea["status"]) => void;
  onDelete: (id: string) => void;
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleString("ja-JP", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function IdeaCard({ idea, onStatusChange, onDelete }: IdeaCardProps) {
  const handleDelete = () => {
    if (window.confirm("このアイデアを削除しますか？")) {
      onDelete(idea.id);
    }
  };

  return (
    <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <h4 className="text-sm font-semibold text-foreground">{idea.title}</h4>
          {idea.description && (
            <p className="mt-1 whitespace-pre-wrap text-sm text-muted-foreground">
              {idea.description}
            </p>
          )}

          <div className="mt-3 flex flex-wrap items-center gap-2">
            <select
              value={idea.status}
              onChange={(e) => onStatusChange(idea.id, e.target.value as Idea["status"])}
              className={`rounded-full border-0 px-2.5 py-0.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-ring ${statusColors[idea.status]}`}
            >
              {allStatuses.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>

            {idea.tags.map((tag) => (
              <span
                key={tag}
                className="inline-flex items-center rounded-full bg-secondary px-2.5 py-0.5 text-xs font-medium text-secondary-foreground"
              >
                {tag}
              </span>
            ))}

            {idea.relatedIdeas.length > 0 && (
              <span className="text-xs text-muted-foreground">
                関連: {idea.relatedIdeas.length}件
              </span>
            )}

            <span className="ml-auto text-xs text-muted-foreground">
              {formatDate(idea.createdAt)}
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
