import type { TransactionType } from "./types";

export interface ImportPreviewItem {
  row_index: number;
  date: string;
  description: string;
  amount: number;
  type: TransactionType;
  suggested_category_id: string | null;
  suggested_category_name: string | null;
}

export interface ImportConfirmItem {
  date: string;
  description: string;
  amount: number;
  type: TransactionType;
  account_id: string;
  category_id: string;
}