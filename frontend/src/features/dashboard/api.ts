import { apiClient } from "../../lib/api-client";
import type { AccountBalance, CategoryTotal, MonthlyEvolution } from "./types";

export interface DateRangeParams {
  start_date: string;
  end_date: string;
}

export async function fetchTotalsByCategory(
  params: DateRangeParams
): Promise<CategoryTotal[]> {
  const { data } = await apiClient.get<CategoryTotal[]>(
    "/analytics/totals-by-category",
    { params }
  );
  return data;
}

export async function fetchMonthlyEvolution(
  params: DateRangeParams
): Promise<MonthlyEvolution[]> {
  const { data } = await apiClient.get<MonthlyEvolution[]>(
    "/analytics/monthly-evolution",
    { params }
  );
  return data;
}

export async function fetchAccountBalances(): Promise<AccountBalance[]> {
  const { data } = await apiClient.get<AccountBalance[]>("/analytics/account-balances");
  return data;
}