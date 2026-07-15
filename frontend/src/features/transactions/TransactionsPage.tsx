import { useState } from "react";
import { TransactionsTable } from "./TransactionsTable";
import { TransactionForm } from "./TransactionForm";
import { ImportCsvModal } from "./ImportCsvModal";
import { useCreateTransaction } from "./hooks";
import { FiltersBar } from "../../components/FiltersBar";

export function TransactionsPage() {
  const [isCreating, setIsCreating] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const createMutation = useCreateTransaction();

  function handleCreate(data: Parameters<typeof createMutation.mutate>[0]) {
    createMutation.mutate(data, {
      onSuccess: () => setIsCreating(false),
    });
  }

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Transações</h1>

      <FiltersBar />

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1.5rem" }}>
        <button onClick={() => setIsCreating(true)}>+ Nova transação</button>
        <button onClick={() => setIsImporting(true)}>Importar CSV</button>
      </div>

      {isCreating && (
        <div style={{ marginBottom: "1.5rem", maxWidth: "400px" }}>
          <h3>Nova transação</h3>
          <TransactionForm
            onSubmit={handleCreate}
            onCancel={() => setIsCreating(false)}
            isSubmitting={createMutation.isPending}
          />
        </div>
      )}

      {isImporting && <ImportCsvModal onClose={() => setIsImporting(false)} />}

      <TransactionsTable />
    </div>
  );
}