import { useState, useEffect } from "react";
import { WeekSelector, getCurrentWeek } from "@/components/weekly/WeekSelector";
import { WeeklyReport } from "@/components/weekly/WeeklyReport";
import { useWeekly } from "@/hooks/useWeekly";

export function WeeklyPage() {
  const [weekOf, setWeekOf] = useState(getCurrentWeek);
  const { weeklyReport, loading, error, generateReport, fetchReport, updateReport } = useWeekly();

  useEffect(() => {
    void fetchReport(weekOf);
  }, [weekOf, fetchReport]);

  const handleGenerate = async () => {
    await generateReport(weekOf);
  };

  const handleUpdate = async (data: { this_week: string; next_week: string }) => {
    await updateReport(weekOf, data);
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">週報</h2>

      <div className="flex justify-center">
        <WeekSelector weekOf={weekOf} onChange={setWeekOf} />
      </div>

      <WeeklyReport
        report={weeklyReport}
        loading={loading}
        error={error}
        onGenerate={handleGenerate}
        onUpdate={handleUpdate}
      />
    </div>
  );
}
