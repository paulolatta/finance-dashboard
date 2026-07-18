import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { useFiltersStore } from "../../stores/filtersStore";
import { useTotalsByCategory } from "./hooks";
import { Card } from "../../components/ui";
import type { CategoryTotal } from "./types";

export function CategoryPieChart() {
  const { startDate, endDate } = useFiltersStore();

  const { data, isLoading } = useTotalsByCategory({
    start_date: new Date(startDate).toISOString(),
    end_date: new Date(endDate).toISOString(),
  });

  return (
    <Card>
      <h3 style={{ marginBottom: "var(--space-4)" }}>Gastos por categoria</h3>

      {isLoading && <p style={{ color: "var(--color-text-secondary)" }}>Carregando...</p>}
      {!isLoading && (!data || data.length === 0) && (
        <p style={{ color: "var(--color-text-secondary)" }}>
          Nenhuma despesa encontrada no período selecionado.
        </p>
      )}

      {data && data.length > 0 && (
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie
              data={data}
              dataKey="total"
              nameKey="category_name"
              cx="50%"
              cy="50%"
              outerRadius={90}
              label={(props: any) => {
                const item = props as CategoryTotal;
                return `${item.category_name}: R$ ${item.total.toFixed(0)}`;
              }}
            >
              {data.map((entry) => (
                <Cell key={entry.category_id} fill={entry.category_color} />
              ))}
            </Pie>
            <Tooltip formatter={(value: number | string) => `R$ ${Number(value).toFixed(2)}`} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      )}
    </Card>
  );
}