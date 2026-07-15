import { useQuery } from "@tanstack/react-query";
import {
  fetchAccountBalances,
  fetchMonthlyEvolution,
  fetchTotalsByCategory,
} from "./api";
import type { DateRangeParams } from "./api";

export function useTotalsByCategory(params: DateRangeParams) {
  return useQuery({
    queryKey: ["analytics", "totals-by-category", params],
    queryFn: () => fetchTotalsByCategory(params),
  });
}

export function useMonthlyEvolution(params: DateRangeParams) {
  return useQuery({
    queryKey: ["analytics", "monthly-evolution", params],
    queryFn: () => fetchMonthlyEvolution(params),
  });
}

export function useAccountBalances() {
  return useQuery({
    queryKey: ["analytics", "account-balances"],
    queryFn: fetchAccountBalances,
  });
}