import { Dashboard } from "@/components/dashboard/Dashboard";
import { useDashboard } from "@/hooks/useDashboard";

export function DashboardPage() {
  const { summary, loading, error } = useDashboard();

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">ダッシュボード</h2>
      <Dashboard summary={summary} loading={loading} error={error} />
    </div>
  );
}
