import { useState, type FormEvent } from "react";
import { Plus } from "lucide-react";

interface IdeaFormProps {
  onSubmit: (title: string, description: string) => Promise<void>;
  loading: boolean;
}

export function IdeaForm({ onSubmit, loading }: IdeaFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle) return;

    try {
      await onSubmit(trimmedTitle, description.trim());
      setTitle("");
      setDescription("");
    } catch {
      // エラーは useIdeas 側で処理済み
    }
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-lg border border-border bg-card p-4 shadow-sm">
      <h3 className="mb-3 text-sm font-medium text-foreground">新しいアイデアを追加</h3>
      <div className="space-y-3">
        <div>
          <label htmlFor="idea-title" className="mb-1 block text-xs font-medium text-muted-foreground">
            タイトル（必須）
          </label>
          <input
            id="idea-title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="アイデアのタイトル..."
            disabled={loading}
            className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          />
        </div>
        <div>
          <label htmlFor="idea-description" className="mb-1 block text-xs font-medium text-muted-foreground">
            詳細説明（オプション）
          </label>
          <textarea
            id="idea-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="アイデアの詳細..."
            rows={3}
            disabled={loading}
            className="w-full resize-none rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          />
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading || !title.trim()}
            className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
                追加中...
              </>
            ) : (
              <>
                <Plus className="h-4 w-4" />
                追加
              </>
            )}
          </button>
        </div>
      </div>
    </form>
  );
}
