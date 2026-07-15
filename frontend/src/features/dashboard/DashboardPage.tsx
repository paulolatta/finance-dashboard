import { FiltersBar } from "../../components/FiltersBar";
import { AccountBalanceCards } from "./AccountBalanceCards";
import { CategoryPieChart } from "./CategoryPieChart";
import { MonthlyEvolutionChart } from "./MonthlyEvolutionChart";

export function DashboardPage() {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Dashboard</h1>

      <FiltersBar />

      <div style={{ marginBottom: "2rem" }}>
        <AccountBalanceCards />
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "2rem",
        }}
      >
        <CategoryPieChart />
        <MonthlyEvolutionChart />
      </div>
    </div>
  );
}