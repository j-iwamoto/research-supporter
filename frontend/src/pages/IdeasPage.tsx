import { IdeaForm } from "@/components/ideas/IdeaForm";
import { IdeaList } from "@/components/ideas/IdeaList";
import { useIdeas } from "@/hooks/useIdeas";
import type { Idea } from "@/types";

export function IdeasPage() {
  const { ideas, loading, error, createIdea, updateIdea, deleteIdea } = useIdeas();

  const handleStatusChange = (id: string, status: Idea["status"]) => {
    void updateIdea(id, { status });
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">アイデア</h2>

      <IdeaForm onSubmit={createIdea} loading={loading} />

      {error && (
        <div className="rounded-md bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {error}
        </div>
      )}

      <div>
        <h3 className="mb-3 text-lg font-semibold">アイデア一覧</h3>
        <IdeaList
          ideas={ideas}
          loading={loading}
          onStatusChange={handleStatusChange}
          onDelete={deleteIdea}
        />
      </div>
    </div>
  );
}
