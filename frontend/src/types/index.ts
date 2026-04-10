/** 日報の記録 */
export interface Log {
  id: string;
  content: string;
  category: "実験" | "論文読み" | "コーディング" | "ミーティング" | "執筆" | "その他";
  tags: string[];
  created_at: string;
  user_id: string;
  week_of: string;
}

/** アイデアメモ */
export interface Idea {
  id: string;
  title: string;
  description: string;
  tags: string[];
  status: "未着手" | "検討中" | "採用" | "却下";
  related_ideas: string[];
  created_at: string;
  updated_at: string;
  user_id: string;
}

/** 週報 */
export interface WeeklyReport {
  id: string;
  user_id: string;
  week_of: string;
  this_week: string;
  next_week: string;
  generated_at: string;
  edited_at: string | null;
}

/** ダッシュボードサマリー */
export interface DashboardSummary {
  totalLogsThisWeek: number;
  categoryCounts: Record<string, number>;
  totalIdeas: number;
  ideaStatusCounts: Record<string, number>;
  weeklyTrend: {
    weekOf: string;
    count: number;
  }[];
  aiSuggestion: string | null;
}
