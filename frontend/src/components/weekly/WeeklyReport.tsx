import { useState } from "react";
import { Pencil, Save, Sparkles, ClipboardCopy, X } from "lucide-react";
import type { WeeklyReport as WeeklyReportType } from "@/types";

interface WeeklyReportProps {
  report: WeeklyReportType | null;
  loading: boolean;
  error: string | null;
  onGenerate: () => Promise<void>;
  onUpdate: (data: { thisWeek: string; nextWeek: string }) => Promise<void>;
}

export function WeeklyReport({ report, loading, error, onGenerate, onUpdate }: WeeklyReportProps) {
  const [editing, setEditing] = useState(false);
  const [thisWeek, setThisWeek] = useState("");
  const [nextWeek, setNextWeek] = useState("");
  const [copySuccess, setCopySuccess] = useState(false);

  const handleEdit = () => {
    if (report) {
      setThisWeek(report.thisWeek);
      setNextWeek(report.nextWeek);
      setEditing(true);
    }
  };

  const handleCancel = () => {
    setEditing(false);
  };

  const handleSave = async () => {
    try {
      await onUpdate({ thisWeek, nextWeek });
      setEditing(false);
    } catch {
      // エラーは useWeekly 側で処理済み
    }
  };

  const handleCopy = async () => {
    if (!report) return;
    const text = `【今週やったこと】\n${report.thisWeek}\n\n【来週やること】\n${report.nextWeek}`;
    try {
      await navigator.clipboard.writeText(text);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch {
      // clipboard API が使えない場合は無視
    }
  };

  if (loading) {
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

  if (!report) {
    return (
      <div className="rounded-lg border border-dashed border-border py-12 text-center">
        <p className="text-sm text-muted-foreground">この週の週報はまだありません</p>
        <button
          type="button"
          onClick={onGenerate}
          disabled={loading}
          className="mt-4 inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <Sparkles className="h-4 w-4" />
          週報を生成
        </button>
      </div>
    );
  }

  if (editing) {
    return (
      <div className="space-y-4 rounded-lg border border-border bg-card p-6 shadow-sm">
        <div>
          <label className="mb-1 block text-sm font-medium text-foreground">
            今週やったこと
          </label>
          <textarea
            value={thisWeek}
            onChange={(e) => setThisWeek(e.target.value)}
            rows={6}
            className="w-full resize-none rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-foreground">
            来週やること
          </label>
          <textarea
            value={nextWeek}
            onChange={(e) => setNextWeek(e.target.value)}
            rows={6}
            className="w-full resize-none rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
        <div className="flex justify-end gap-2">
          <button
            type="button"
            onClick={handleCancel}
            className="inline-flex items-center gap-2 rounded-md border border-border px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-accent"
          >
            <X className="h-4 w-4" />
            キャンセル
          </button>
          <button
            type="button"
            onClick={handleSave}
            disabled={loading}
            className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Save className="h-4 w-4" />
            保存
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4 rounded-lg border border-border bg-card p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-foreground">週報</h3>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={handleCopy}
            className="inline-flex items-center gap-1.5 rounded-md border border-border px-3 py-1.5 text-xs font-medium text-foreground transition-colors hover:bg-accent"
          >
            <ClipboardCopy className="h-3.5 w-3.5" />
            {copySuccess ? "コピーしました" : "Googleフォーム用にコピー"}
          </button>
          <button
            type="button"
            onClick={handleEdit}
            className="inline-flex items-center gap-1.5 rounded-md border border-border px-3 py-1.5 text-xs font-medium text-foreground transition-colors hover:bg-accent"
          >
            <Pencil className="h-3.5 w-3.5" />
            編集
          </button>
        </div>
      </div>

      <div>
        <h4 className="mb-2 text-sm font-medium text-muted-foreground">今週やったこと</h4>
        <div className="whitespace-pre-wrap rounded-md bg-muted/50 p-4 text-sm text-foreground">
          {report.thisWeek}
        </div>
      </div>

      <div>
        <h4 className="mb-2 text-sm font-medium text-muted-foreground">来週やること</h4>
        <div className="whitespace-pre-wrap rounded-md bg-muted/50 p-4 text-sm text-foreground">
          {report.nextWeek}
        </div>
      </div>

      {report.editedAt && (
        <p className="text-xs text-muted-foreground">
          最終編集: {new Date(report.editedAt).toLocaleString("ja-JP")}
        </p>
      )}
    </div>
  );
}
