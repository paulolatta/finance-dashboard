import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { useFiltersStore } from "../../stores/filtersStore";
import { useTotalsByCategory } from "./hooks";

export function CategoryPieChart() {
  const { startDate, endDate } = useFiltersStore();

  const { data, isLoading } = useTotalsByCategory({
    start_date: new Date(startDate).toISOString(),
    end_date: new Date(endDate).toISOString(),
  });

  if (isLoading) return <p>Carregando gráfico...</p>;

  if (!data || data.length === 0) {
    return <p>Nenhuma despesa encontrada no período selecionado.</p>;
  }

  return (
    <div>
      <h3>Gastos por categoria</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            dataKey="total"
            nameKey="category_name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={(entry) => `${entry.category_name}: R$ ${entry.total.toFixed(0)}`}
          >
            {data.map((entry) => (
              <Cell key={entry.category_id} fill={entry.category_color} />
            ))}
          </Pie>
          <Tooltip formatter={(value: number) => `R$ ${value.toFixed(2)}`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}