import { useState, useEffect, type FormEvent } from "react";
import { Save, User, Clock, Sun, Moon } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useToast } from "@/contexts/ToastContext";
import { usePageTitle } from "@/hooks/usePageTitle";

interface Settings {
  weeklyReportDay: string;
  timezone: string;
  theme: "light" | "dark";
}

const DAYS = [
  { value: "0", label: "日曜日" },
  { value: "1", label: "月曜日" },
  { value: "2", label: "火曜日" },
  { value: "3", label: "水曜日" },
  { value: "4", label: "木曜日" },
  { value: "5", label: "金曜日" },
  { value: "6", label: "土曜日" },
];

const TIMEZONES = [
  "Asia/Tokyo",
  "America/New_York",
  "America/Los_Angeles",
  "Europe/London",
  "UTC",
];

function loadSettings(): Settings {
  try {
    const stored = localStorage.getItem("research-manager-settings");
    if (stored) {
      return JSON.parse(stored) as Settings;
    }
  } catch {
    // ignore
  }
  return {
    weeklyReportDay: "5", // 金曜日
    timezone: "Asia/Tokyo",
    theme: "light",
  };
}

function saveSettingsToStorage(settings: Settings) {
  localStorage.setItem("research-manager-settings", JSON.stringify(settings));
}

function applyTheme(theme: "light" | "dark") {
  if (theme === "dark") {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }
}

export function SettingsPage() {
  usePageTitle("設定");
  const { user } = useAuth();
  const { showToast } = useToast();
  const [settings, setSettings] = useState<Settings>(loadSettings);
  const [saving, setSaving] = useState(false);

  // 初回マウント時にテーマ適用
  useEffect(() => {
    applyTheme(settings.theme);
  }, [settings.theme]);

  const handleThemeToggle = () => {
    setSettings((prev) => ({
      ...prev,
      theme: prev.theme === "light" ? "dark" : "light",
    }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    // localStorageに保存（模擬的な非同期処理）
    setTimeout(() => {
      saveSettingsToStorage(settings);
      applyTheme(settings.theme);
      setSaving(false);
      showToast("設定を保存しました", "success");
    }, 300);
  };

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h2 className="text-2xl font-bold text-foreground">設定</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* アカウント情報 */}
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            <User className="h-5 w-5 text-muted-foreground" />
            <h3 className="text-lg font-semibold text-foreground">アカウント情報</h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="mb-1 block text-sm font-medium text-foreground">
                名前
              </label>
              <div className="rounded-md border border-input bg-muted/50 px-3 py-2 text-sm text-foreground">
                {user?.displayName ?? "-"}
              </div>
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-foreground">
                メールアドレス
              </label>
              <div className="rounded-md border border-input bg-muted/50 px-3 py-2 text-sm text-foreground">
                {user?.email ?? "-"}
              </div>
            </div>
          </div>
        </div>

        {/* 週報設定 */}
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            <Clock className="h-5 w-5 text-muted-foreground" />
            <h3 className="text-lg font-semibold text-foreground">週報設定</h3>
          </div>
          <div className="space-y-4">
            <div>
              <label
                htmlFor="weekly-day"
                className="mb-1 block text-sm font-medium text-foreground"
              >
                週報自動生成の曜日
              </label>
              <select
                id="weekly-day"
                value={settings.weeklyReportDay}
                onChange={(e) =>
                  setSettings((prev) => ({ ...prev, weeklyReportDay: e.target.value }))
                }
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              >
                {DAYS.map((day) => (
                  <option key={day.value} value={day.value}>
                    {day.label}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label
                htmlFor="timezone"
                className="mb-1 block text-sm font-medium text-foreground"
              >
                タイムゾーン
              </label>
              <select
                id="timezone"
                value={settings.timezone}
                onChange={(e) =>
                  setSettings((prev) => ({ ...prev, timezone: e.target.value }))
                }
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              >
                {TIMEZONES.map((tz) => (
                  <option key={tz} value={tz}>
                    {tz}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* テーマ設定 */}
        <div className="rounded-lg border border-border bg-card p-6 shadow-sm">
          <div className="mb-4 flex items-center gap-2">
            {settings.theme === "light" ? (
              <Sun className="h-5 w-5 text-muted-foreground" />
            ) : (
              <Moon className="h-5 w-5 text-muted-foreground" />
            )}
            <h3 className="text-lg font-semibold text-foreground">テーマ</h3>
          </div>
          <div className="flex items-center gap-4">
            <button
              type="button"
              onClick={handleThemeToggle}
              className={`flex items-center gap-2 rounded-md border px-4 py-2 text-sm font-medium transition-colors ${
                settings.theme === "light"
                  ? "border-primary bg-primary/10 text-primary"
                  : "border-border text-muted-foreground hover:border-primary"
              }`}
            >
              <Sun className="h-4 w-4" />
              ライト
            </button>
            <button
              type="button"
              onClick={handleThemeToggle}
              className={`flex items-center gap-2 rounded-md border px-4 py-2 text-sm font-medium transition-colors ${
                settings.theme === "dark"
                  ? "border-primary bg-primary/10 text-primary"
                  : "border-border text-muted-foreground hover:border-primary"
              }`}
            >
              <Moon className="h-4 w-4" />
              ダーク
            </button>
          </div>
        </div>

        {/* 保存ボタン */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="inline-flex items-center gap-2 rounded-md bg-primary px-6 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {saving ? (
              <>
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
                保存中...
              </>
            ) : (
              <>
                <Save className="h-4 w-4" />
                設定を保存
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
