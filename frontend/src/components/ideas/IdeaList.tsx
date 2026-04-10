import { useState } from "react";
import { Search } from "lucide-react";
import { IdeaCard } from "@/components/ideas/IdeaCard";
import type { Idea } from "@/types";

const filterStatuses: Array<{ label: string; value: string }> = [
  { label: "すべて", value: "" },
  { label: "未着手", value: "未着手" },
  { label: "検討中", value: "検討中" },
  { label: "採用", value: "採用" },
  { label: "却下", value: "却下" },
];

interface IdeaListProps {
  ideas: Idea[];
  loading: boolean;
  onStatusChange: (id: string, status: Idea["status"]) => void;
  onDelete: (id: string) => void;
}

export function IdeaList({ ideas, loading, onStatusChange, onDelete }: IdeaListProps) {
  const [statusFilter, setStatusFilter] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  const filteredIdeas = ideas.filter((idea) => {
    if (statusFilter && idea.status !== statusFilter) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        idea.title.toLowerCase().includes(q) ||
        idea.description.toLowerCase().includes(q) ||
        idea.tags.some((tag) => tag.toLowerCase().includes(q))
      );
    }
    return true;
  });

  if (loading && ideas.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
        <span className="ml-2 text-sm text-muted-foreground">読み込み中...</span>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* フィルタ・検索 */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <div className="flex gap-1">
          {filterStatuses.map((fs) => (
            <button
              key={fs.value}
              type="button"
              onClick={() => setStatusFilter(fs.value)}
              className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                statusFilter === fs.value
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground"
              }`}
            >
              {fs.label}
            </button>
          ))}
        </div>

        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="アイデアを検索..."
            className="w-full rounded-md border border-input bg-background py-1.5 pl-9 pr-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
      </div>

      {/* 一覧 */}
      {filteredIdeas.length === 0 ? (
        <div className="rounded-lg border border-dashed border-border py-12 text-center">
          <p className="text-sm text-muted-foreground">
            {ideas.length === 0 ? "まだアイデアがありません" : "条件に一致するアイデアがありません"}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredIdeas.map((idea) => (
            <IdeaCard
              key={idea.id}
              idea={idea}
              onStatusChange={onStatusChange}
              onDelete={onDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}
