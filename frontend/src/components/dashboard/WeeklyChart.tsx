interface WeeklyChartProps {
  data: { weekOf: string; count: number }[];
}

export function WeeklyChart({ data }: WeeklyChartProps) {
  const maxCount = Math.max(...data.map((d) => d.count), 1);

  return (
    <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
      <h3 className="mb-4 text-sm font-medium text-foreground">週次推移（過去4週間）</h3>
      <div className="flex items-end gap-3" style={{ height: "160px" }}>
        {data.map((item) => {
          const heightPercent = (item.count / maxCount) * 100;
          return (
            <div key={item.weekOf} className="flex flex-1 flex-col items-center gap-1">
              <span className="text-xs font-medium text-foreground">{item.count}</span>
              <div className="relative w-full flex-1">
                <div
                  className="absolute bottom-0 w-full rounded-t-md bg-primary transition-all"
                  style={{ height: `${heightPercent}%`, minHeight: item.count > 0 ? "4px" : "0px" }}
                />
              </div>
              <span className="text-xs text-muted-foreground">
                {item.weekOf.replace(/^\d{4}-/, "")}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
