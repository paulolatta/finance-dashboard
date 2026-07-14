export type AccountType = "checking" | "savings" | "credit_card" | "cash";

export interface Account {
  id: string;
  name: string;
  type: AccountType;
  initial_balance: number;
  created_at: string;
}