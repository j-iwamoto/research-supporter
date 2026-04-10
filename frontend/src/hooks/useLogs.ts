import { useState, useEffect, useCallback } from "react";
import type { Log } from "@/types";
import { apiFetch } from "@/services/api";

interface UseLogsReturn {
  logs: Log[];
  loading: boolean;
  error: string | null;
  fetchLogs: () => Promise<void>;
  createLog: (content: string) => Promise<void>;
  deleteLog: (id: string) => Promise<void>;
}

export function useLogs(): UseLogsReturn {
  const [logs, setLogs] = useState<Log[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch<Log[]>("/api/logs");
      setLogs(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "日報の取得に失敗しました";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  const createLog = useCallback(async (content: string) => {
    setLoading(true);
    setError(null);
    try {
      await apiFetch<Log>("/api/logs", {
        method: "POST",
        body: JSON.stringify({ content }),
      });
      await fetchLogs();
    } catch (err) {
      const message = err instanceof Error ? err.message : "日報の作成に失敗しました";
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchLogs]);

  const deleteLog = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      await apiFetch<void>(`/api/logs/${id}`, {
        method: "DELETE",
      });
      setLogs((prev) => prev.filter((log) => log.id !== id));
    } catch (err) {
      const message = err instanceof Error ? err.message : "日報の削除に失敗しました";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchLogs();
  }, [fetchLogs]);

  return { logs, loading, error, fetchLogs, createLog, deleteLog };
}
