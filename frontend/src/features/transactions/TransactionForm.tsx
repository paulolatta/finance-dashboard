import { useState } from "react";
import { useAccounts } from "../accounts/hooks";
import { useCategories } from "../categories/hooks";
import type { TransactionType } from "./types";

interface TransactionFormProps {
  onSubmit: (data: {
    description: string;
    amount: number;
    date: string;
    type: TransactionType;
    account_id: string;
    category_id: string;
  }) => void;
  onCancel?: () => void;
  isSubmitting?: boolean;
}

const TRANSACTION_TYPES: { value: TransactionType; label: string }[] = [
  { value: "expense", label: "Despesa" },
  { value: "income", label: "Receita" },
];

export function TransactionForm({ onSubmit, onCancel, isSubmitting }: TransactionFormProps) {
  const { data: accounts } = useAccounts();
  const { data: categories } = useCategories();

  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [date, setDate] = useState(() => new Date().toISOString().slice(0, 10));
  const [type, setType] = useState<TransactionType>("expense");
  const [accountId, setAccountId] = useState("");
  const [categoryId, setCategoryId] = useState("");

  // Filtra categorias pelo tipo selecionado (income/expense), já que não faz
  // sentido mostrar "Salário" numa transação de despesa, por exemplo.
  const filteredCategories = categories?.filter((c) => c.type === type) ?? [];

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!accountId || !categoryId) {
      alert("Selecione uma conta e uma categoria.");
      return;
    }

    onSubmit({
      description,
      amount: parseFloat(amount) || 0,
      date: new Date(date).toISOString(),
      type,
      account_id: accountId,
      category_id: categoryId,
    });
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
      <div>
        <label>Descrição</label>
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
          style={{ display: "block", width: "100%" }}
        />
      </div>

      <div>
        <label>Valor</label>
        <input
          type="number"
          step="0.01"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
          style={{ display: "block", width: "100%" }}
        />
      </div>

      <div>
        <label>Data</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
          style={{ display: "block", width: "100%" }}
        />
      </div>

      <div>
        <label>Tipo</label>
        <select
          value={type}
          onChange={(e) => {
            setType(e.target.value as TransactionType);
            setCategoryId(""); // reseta categoria ao trocar tipo, evita categoria incompatível
          }}
          style={{ display: "block", width: "100%" }}
        >
          {TRANSACTION_TYPES.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>Conta</label>
        <select
          value={accountId}
          onChange={(e) => setAccountId(e.target.value)}
          required
          style={{ display: "block", width: "100%" }}
        >
          <option value="">Selecione...</option>
          {accounts?.map((account) => (
            <option key={account.id} value={account.id}>
              {account.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>Categoria</label>
        <select
          value={categoryId}
          onChange={(e) => setCategoryId(e.target.value)}
          required
          style={{ display: "block", width: "100%" }}
        >
          <option value="">Selecione...</option>
          {filteredCategories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
      </div>

      <div style={{ display: "flex", gap: "0.5rem" }}>
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Salvando..." : "Salvar"}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel}>
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
}