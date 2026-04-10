/** 日報の記録 */
export interface Log {
  id: string;
  content: string;
  category: "実験" | "論文読み" | "コーディング" | "ミーティング" | "その他";
  tags: string[];
  createdAt: string;
  userId: string;
  weekOf: string;
}

/** アイデアメモ */
export interface Idea {
  id: string;
  title: string;
  description: string;
  tags: string[];
  status: "未着手" | "検討中" | "採用" | "却下";
  relatedIdeas: string[];
  createdAt: string;
  updatedAt: string;
  userId: string;
}

/** 週報 */
export interface WeeklyReport {
  id: string;
  userId: string;
  weekOf: string;
  thisWeek: string;
  nextWeek: string;
  generatedAt: string;
  editedAt: string | null;
}

/** ダッシュボードサマリー */
export interface DashboardSummary {
  totalLogsThisWeek: number;
  categoryCounts: Record<Log["category"], number>;
  totalIdeas: number;
  ideaStatusCounts: Record<Idea["status"], number>;
  weeklyTrend: {
    weekOf: string;
    count: number;
  }[];
  aiSuggestion: string | null;
}
