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

  if (isLoading) return <p>Carregando gráfico...</p>;

  if (!data || data.length === 0) {
    return <p>Nenhuma transação encontrada no período selecionado.</p>;
  }

  const chartData = data.map((item) => ({
    label: `${MONTH_LABELS[item.month - 1]}/${item.year}`,
    Receita: item.income,
    Despesa: item.expense,
  }));

  return (
    <div>
      <h3>Evolução mensal</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis />
          <Tooltip formatter={(value: number) => `R$ ${value.toFixed(2)}`} />
          <Legend />
          <Bar dataKey="Receita" fill="#22C55E" />
          <Bar dataKey="Despesa" fill="#EF4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}