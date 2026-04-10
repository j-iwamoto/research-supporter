import { createContext, useContext, useState, useCallback, type ReactNode } from "react";

interface User {
  uid: string;
  email: string;
  displayName: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: () => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>({
    uid: "demo-user",
    email: "demo@example.com",
    displayName: "デモユーザー",
  });
  const [loading] = useState(false);

  const login = useCallback(async () => {
    // TODO: Firebase Google認証を実装
    setUser({
      uid: "demo-user",
      email: "demo@example.com",
      displayName: "デモユーザー",
    });
  }, []);

  const logout = useCallback(async () => {
    // TODO: Firebase ログアウトを実装
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
