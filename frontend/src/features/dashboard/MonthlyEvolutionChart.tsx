import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useFiltersStore } from "../../stores/filtersStore";
import { useMonthlyEvolution } from "./hooks";
import { Card } from "../../components/ui";

const MONTH_LABELS = [
  "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
  "Jul", "Ago", "Set", "Out", "Nov", "Dez",
];

export function MonthlyEvolutionChart() {
  const { startDate, endDate } = useFiltersStore();

  const { data, isLoading } = useMonthlyEvolution({
    start_date: new Date(startDate).toISOString(),
    end_date: new Date(endDate).toISOString(),
  });

  const chartData = data?.map((item) => ({
    label: `${MONTH_LABELS[item.month - 1]}/${item.year}`,
    Receita: item.income,
    Despesa: item.expense,
  }));

  return (
    <Card>
      <h3 style={{ marginBottom: "var(--space-4)" }}>Evolução mensal</h3>

      {isLoading && <p style={{ color: "var(--color-text-secondary)" }}>Carregando...</p>}
      {!isLoading && (!chartData || chartData.length === 0) && (
        <p style={{ color: "var(--color-text-secondary)" }}>
          Nenhuma transação encontrada no período selecionado.
        </p>
      )}

      {chartData && chartData.length > 0 && (
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
            <XAxis dataKey="label" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip formatter={(value: number | string) => `R$ ${Number(value).toFixed(2)}`} />
            <Legend />
            <Bar dataKey="Receita" fill="var(--color-success)" radius={[4, 4, 0, 0]} />
            <Bar dataKey="Despesa" fill="var(--color-danger)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </Card>
  );
}