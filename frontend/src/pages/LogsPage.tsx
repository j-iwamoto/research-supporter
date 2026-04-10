import { LogForm } from "@/components/logs/LogForm";
import { LogList } from "@/components/logs/LogList";
import { useLogs } from "@/hooks/useLogs";

export function LogsPage() {
  const { logs, loading, error, createLog, deleteLog } = useLogs();

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">日報</h2>

      <LogForm onSubmit={createLog} loading={loading} />

      {error && (
        <div className="rounded-md bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {error}
        </div>
      )}

      <div>
        <h3 className="mb-3 text-lg font-semibold">今日の記録</h3>
        <LogList logs={logs} loading={loading} onDelete={deleteLog} />
      </div>
    </div>
  );
}
