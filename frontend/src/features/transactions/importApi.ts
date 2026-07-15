import { apiClient } from "../../lib/api-client";
import type { Transaction } from "./types";
import type { ImportPreviewItem, ImportConfirmItem } from "./importTypes";

export async function previewImport(file: File): Promise<ImportPreviewItem[]> {
  const formData = new FormData();
  formData.append("file", file);

  const { data } = await apiClient.post<ImportPreviewItem[]>(
    "/transactions/import/preview",
    formData,
    { headers: { "Content-Type": "multipart/form-data" } }
  );
  return data;
}

export async function confirmImport(items: ImportConfirmItem[]): Promise<Transaction[]> {
  const { data } = await apiClient.post<Transaction[]>("/transactions/import/confirm", {
    items,
  });
  return data;
}