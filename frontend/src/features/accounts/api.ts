import { apiClient } from "../../lib/api-client";
import type { Account } from "./types";

export async function fetchAccounts(): Promise<Account[]> {
  const { data } = await apiClient.get<Account[]>("/accounts/");
  return data;
}