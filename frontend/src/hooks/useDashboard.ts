import { useState, useEffect, useCallback } from "react";
import type { DashboardSummary } from "@/types";
import { apiFetch } from "@/services/api";

interface UseDashboardReturn {
  summary: DashboardSummary | null;
  loading: boolean;
  error: string | null;
  fetchSummary: () => Promise<void>;
}

export function useDashboard(): UseDashboardReturn {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSummary = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch<DashboardSummary>("/api/dashboard/summary");
      setSummary(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "ダッシュボードの取得に失敗しました";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchSummary();
  }, [fetchSummary]);

  return { summary, loading, error, fetchSummary };
}
