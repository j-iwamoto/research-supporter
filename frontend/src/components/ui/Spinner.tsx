interface SpinnerProps {
  text?: string;
}

export function Spinner({ text = "読み込み中..." }: SpinnerProps) {
  return (
    <div className="flex items-center justify-center py-12">
      <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      <span className="ml-2 text-sm text-muted-foreground">{text}</span>
    </div>
  );
}
