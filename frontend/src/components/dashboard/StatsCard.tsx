import type { LucideIcon } from "lucide-react";

interface StatsCardProps {
  title: string;
  value: number | string;
  subtext?: string;
  icon: LucideIcon;
}

export function StatsCard({ title, value, subtext, icon: Icon }: StatsCardProps) {
  return (
    <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-muted-foreground">{title}</p>
          <p className="mt-1 text-2xl font-bold text-foreground">{value}</p>
          {subtext && (
            <p className="mt-1 text-xs text-muted-foreground">{subtext}</p>
          )}
        </div>
        <div className="rounded-md bg-primary/10 p-2">
          <Icon className="h-5 w-5 text-primary" />
        </div>
      </div>
    </div>
  );
}
