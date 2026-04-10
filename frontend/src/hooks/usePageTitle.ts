import { useEffect } from "react";

export function usePageTitle(title: string) {
  useEffect(() => {
    const prev = document.title;
    document.title = `${title} | 研究管理`;
    return () => {
      document.title = prev;
    };
  }, [title]);
}
