export interface CategoryTotal {
  category_id: string;
  category_name: string;
  category_color: string;
  total: number;
}

export interface MonthlyEvolution {
  year: number;
  month: number;
  income: number;
  expense: number;
}

export interface AccountBalance {
  account_id: string;
  account_name: string;
  initial_balance: number;
  current_balance: number;
}