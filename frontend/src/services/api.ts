const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// 開発用ダミートークン（将来Firebase Auth等に置き換え）
const DEV_TOKEN = "dev-dummy-token";

function getAuthHeaders(): Record<string, string> {
  return {
    Authorization: `Bearer ${DEV_TOKEN}`,
  };
}

export async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}
