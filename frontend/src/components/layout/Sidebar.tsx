import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  FileText,
  CalendarDays,
  Lightbulb,
  Settings,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { to: "/", label: "ダッシュボード", icon: LayoutDashboard },
  { to: "/logs", label: "日報", icon: FileText },
  { to: "/weekly", label: "週報", icon: CalendarDays },
  { to: "/ideas", label: "アイデア", icon: Lightbulb },
  { to: "/settings", label: "設定", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="flex h-full w-60 flex-col border-r border-border bg-sidebar-background">
      <div className="flex h-14 items-center border-b border-border px-4">
        <span className="text-lg font-bold text-sidebar-primary">
          研究管理
        </span>
      </div>
      <nav className="flex-1 space-y-1 p-3">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-sidebar-accent text-sidebar-accent-foreground"
                  : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              )
            }
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
