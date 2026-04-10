import { useState, type FormEvent } from "react";
import { Send } from "lucide-react";

interface LogFormProps {
  onSubmit: (content: string) => Promise<void>;
  loading: boolean;
}

export function LogForm({ onSubmit, loading }: LogFormProps) {
  const [content, setContent] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const trimmed = content.trim();
    if (!trimmed) return;

    try {
      await onSubmit(trimmed);
      setContent("");
    } catch {
      // エラーは useLogs 側で処理済み
    }
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-lg border border-border bg-card p-4 shadow-sm">
      <label htmlFor="log-content" className="mb-2 block text-sm font-medium text-foreground">
        研究活動を記録
      </label>
      <textarea
        id="log-content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="今日行った研究活動を入力してください..."
        rows={4}
        disabled={loading}
        className="w-full resize-none rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
      />
      <div className="mt-3 flex justify-end">
        <button
          type="submit"
          disabled={loading || !content.trim()}
          className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? (
            <>
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
              送信中...
            </>
          ) : (
            <>
              <Send className="h-4 w-4" />
              記録する
            </>
          )}
        </button>
      </div>
    </form>
  );
}
