import { useState } from "react";
import { TransactionsTable } from "./TransactionsTable";
import { TransactionForm } from "./TransactionForm";
import { useCreateTransaction } from "./hooks";

export function TransactionsPage() {
  const [isCreating, setIsCreating] = useState(false);
  const createMutation = useCreateTransaction();

  function handleCreate(data: Parameters<typeof createMutation.mutate>[0]) {
    createMutation.mutate(data, {
      onSuccess: () => setIsCreating(false),
    });
  }

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Transações</h1>

      {isCreating ? (
        <div style={{ marginBottom: "1.5rem", maxWidth: "400px" }}>
          <h3>Nova transação</h3>
          <TransactionForm
            onSubmit={handleCreate}
            onCancel={() => setIsCreating(false)}
            isSubmitting={createMutation.isPending}
          />
        </div>
      ) : (
        <button onClick={() => setIsCreating(true)} style={{ marginBottom: "1.5rem" }}>
          + Nova transação
        </button>
      )}

      <TransactionsTable />
    </div>
  );
}