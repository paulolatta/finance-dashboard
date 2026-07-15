import type { ReactNode } from "react";
import { Link } from "@tanstack/react-router";

interface LayoutProps {
  children: ReactNode;
}

const NAV_ITEMS = [
  { to: "/", label: "Dashboard" },
  { to: "/transactions", label: "Transações" },
  { to: "/accounts", label: "Contas" },
  { to: "/categories", label: "Categorias" },
];

export function Layout({ children }: LayoutProps) {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <nav
        style={{
          width: "200px",
          borderRight: "1px solid #eee",
          padding: "1.5rem 1rem",
        }}
      >
        <h2 style={{ fontSize: "1.1rem", marginBottom: "1.5rem" }}>Finance Dashboard</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              style={{ textDecoration: "none", color: "#333", padding: "0.5rem" }}
              activeProps={{
                style: { fontWeight: "bold", background: "#f3f4f6", borderRadius: "6px" },
              }}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </nav>

      <main style={{ flex: 1 }}>{children}</main>
    </div>
  );
}