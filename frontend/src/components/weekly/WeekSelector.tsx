import { ChevronLeft, ChevronRight } from "lucide-react";

interface WeekSelectorProps {
  weekOf: string;
  onChange: (weekOf: string) => void;
}

/** ISO週番号からYYYY-Www文字列を計算するユーティリティ */
function getISOWeekString(date: Date): string {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  const weekNo = Math.ceil(((d.getTime() - yearStart.getTime()) / 86400000 + 1) / 7);
  return `${d.getUTCFullYear()}-W${String(weekNo).padStart(2, "0")}`;
}

/** YYYY-Www文字列から月曜日のDateを取得 */
function weekStringToDate(weekStr: string): Date {
  const match = weekStr.match(/^(\d{4})-W(\d{2})$/);
  if (!match) return new Date();
  const year = parseInt(match[1], 10);
  const week = parseInt(match[2], 10);
  const jan4 = new Date(Date.UTC(year, 0, 4));
  const dayOfWeek = jan4.getUTCDay() || 7;
  const monday = new Date(jan4.getTime());
  monday.setUTCDate(jan4.getUTCDate() - dayOfWeek + 1 + (week - 1) * 7);
  return monday;
}

function shiftWeek(weekOf: string, delta: number): string {
  const date = weekStringToDate(weekOf);
  date.setUTCDate(date.getUTCDate() + delta * 7);
  return getISOWeekString(date);
}

function formatWeekRange(weekOf: string): string {
  const monday = weekStringToDate(weekOf);
  const sunday = new Date(monday.getTime());
  sunday.setUTCDate(monday.getUTCDate() + 6);
  const fmt = (d: Date) =>
    `${d.getUTCMonth() + 1}/${d.getUTCDate()}`;
  return `${fmt(monday)} - ${fmt(sunday)}`;
}

export function getCurrentWeek(): string {
  return getISOWeekString(new Date());
}

export function WeekSelector({ weekOf, onChange }: WeekSelectorProps) {
  return (
    <div className="flex items-center gap-3">
      <button
        type="button"
        onClick={() => onChange(shiftWeek(weekOf, -1))}
        className="rounded-md p-2 text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
        aria-label="前の週"
      >
        <ChevronLeft className="h-5 w-5" />
      </button>

      <div className="text-center">
        <p className="text-lg font-semibold text-foreground">{weekOf}</p>
        <p className="text-sm text-muted-foreground">{formatWeekRange(weekOf)}</p>
      </div>

      <button
        type="button"
        onClick={() => onChange(shiftWeek(weekOf, 1))}
        className="rounded-md p-2 text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
        aria-label="次の週"
      >
        <ChevronRight className="h-5 w-5" />
      </button>
    </div>
  );
}
