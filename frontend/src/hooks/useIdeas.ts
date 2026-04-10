import { useState, useEffect, useCallback } from "react";
import type { Idea } from "@/types";
import { apiFetch } from "@/services/api";

interface UseIdeasReturn {
  ideas: Idea[];
  loading: boolean;
  error: string | null;
  fetchIdeas: (status?: string, tag?: string) => Promise<void>;
  createIdea: (title: string, description: string) => Promise<void>;
  updateIdea: (id: string, data: Partial<Pick<Idea, "title" | "description" | "status" | "tags">>) => Promise<void>;
  deleteIdea: (id: string) => Promise<void>;
}

export function useIdeas(): UseIdeasReturn {
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchIdeas = useCallback(async (status?: string, tag?: string) => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (status) params.set("status", status);
      if (tag) params.set("tag", tag);
      const query = params.toString();
      const path = query ? `/api/ideas?${query}` : "/api/ideas";
      const data = await apiFetch<{ ideas: Idea[]; total: number }>(path);
      setIdeas(data.ideas);
    } catch (err) {
      const message = err instanceof Error ? err.message : "アイデアの取得に失敗しました";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  const createIdea = useCallback(async (title: string, description: string) => {
    setLoading(true);
    setError(null);
    try {
      await apiFetch<Idea>("/api/ideas", {
        method: "POST",
        body: JSON.stringify({ title, description }),
      });
      await fetchIdeas();
    } catch (err) {
      const message = err instanceof Error ? err.message : "アイデアの作成に失敗しました";
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [fetchIdeas]);

  const updateIdea = useCallback(async (id: string, data: Partial<Pick<Idea, "title" | "description" | "status" | "tags">>) => {
    setLoading(true);
    setError(null);
    try {
      const updated = await apiFetch<Idea>(`/api/ideas/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      });
      setIdeas((prev) => prev.map((idea) => (idea.id === id ? updated : idea)));
    } catch (err) {
      const message = err instanceof Error ? err.message : "アイデアの更新に失敗しました";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteIdea = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      await apiFetch<void>(`/api/ideas/${id}`, {
        method: "DELETE",
      });
      setIdeas((prev) => prev.filter((idea) => idea.id !== id));
    } catch (err) {
      const message = err instanceof Error ? err.message : "アイデアの削除に失敗しました";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchIdeas();
  }, [fetchIdeas]);

  return { ideas, loading, error, fetchIdeas, createIdea, updateIdea, deleteIdea };
}
