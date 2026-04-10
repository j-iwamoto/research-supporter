import { useState, useCallback } from "react";
import type { WeeklyReport } from "@/types";
import { apiFetch } from "@/services/api";

interface UseWeeklyReturn {
  weeklyReport: WeeklyReport | null;
  weeklyReports: WeeklyReport[];
  loading: boolean;
  error: string | null;
  generateReport: (weekOf: string) => Promise<void>;
  fetchReport: (weekOf: string) => Promise<void>;
  updateReport: (weekOf: string, data: { this_week: string; next_week: string }) => Promise<void>;
  fetchReports: () => Promise<void>;
}

export function useWeekly(): UseWeeklyReturn {
  const [weeklyReport, setWeeklyReport] = useState<WeeklyReport | null>(null);
  const [weeklyReports, setWeeklyReports] = useState<WeeklyReport[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateReport = useCallback(async (weekOf: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch<WeeklyReport>("/api/weekly/generate", {
        method: "POST",
        body: JSON.stringify({ week_of: weekOf }),
      });
      setWeeklyReport(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "週報の生成に失敗しました";
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchReport = useCallback(async (weekOf: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch<WeeklyReport>(`/api/weekly/${weekOf}`);
      setWeeklyReport(data);
    } catch (err) {
      // 404 = まだ週報が生成されていない（正常）
      const message = err instanceof Error ? err.message : "";
      if (message.includes("404")) {
        setWeeklyReport(null);
      } else {
        setError(message || "週報の取得に失敗しました");
        setWeeklyReport(null);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  const updateReport = useCallback(async (weekOf: string, data: { this_week: string; next_week: string }) => {
    setLoading(true);
    setError(null);
    try {
      const updated = await apiFetch<WeeklyReport>(`/api/weekly/${weekOf}`, {
        method: "PUT",
        body: JSON.stringify(data),
      });
      setWeeklyReport(updated);
    } catch (err) {
      const message = err instanceof Error ? err.message : "週報の更新に失敗しました";
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchReports = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch<{ reports: WeeklyReport[]; total: number }>("/api/weekly");
      setWeeklyReports(data.reports);
    } catch (err) {
      const message = err instanceof Error ? err.message : "週報一覧の取得に失敗しました";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    weeklyReport,
    weeklyReports,
    loading,
    error,
    generateReport,
    fetchReport,
    updateReport,
    fetchReports,
  };
}
