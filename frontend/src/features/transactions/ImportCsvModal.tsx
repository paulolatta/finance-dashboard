import { useState } from "react";
import { usePreviewImport, useConfirmImport } from "./importHooks";
import { useAccounts } from "../accounts/hooks";
import { useCategories } from "../categories/hooks";
import type { ImportPreviewItem } from "./importTypes";

interface ImportCsvModalProps {
  onClose: () => void;
}

// Estado local de cada linha, já com os campos que o usuário pode ajustar
interface ReviewRow extends ImportPreviewItem {
  category_id: string; // vazio se não teve sugestão, senão pré-preenchido
  include: boolean; // permite descartar uma linha específica antes de confirmar
}

export function ImportCsvModal({ onClose }: ImportCsvModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [rows, setRows] = useState<ReviewRow[]>([]);
  const [accountId, setAccountId] = useState("");

  const { data: accounts } = useAccounts();
  const { data: categories } = useCategories();

  const previewMutation = usePreviewImport();
  const confirmMutation = useConfirmImport();

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFile(e.target.files?.[0] ?? null);
  }

  function handlePreview() {
    if (!file) return;

    previewMutation.mutate(file, {
      onSuccess: (items) => {
        setRows(
          items.map((item) => ({
            ...item,
            category_id: item.suggested_category_id ?? "",
            include: true,
          }))
        );
      },
    });
  }

  function updateRow(rowIndex: number, changes: Partial<ReviewRow>) {
    setRows((prev) =>
      prev.map((row) => (row.row_index === rowIndex ? { ...row, ...changes } : row))
    );
  }

  function handleConfirm() {
    if (!accountId) {
      alert("Selecione a conta para importar as transações.");
      return;
    }

    const itemsToImport = rows
      .filter((row) => row.include)
      .map((row) => ({
        date: row.date,
        description: row.description,
        amount: row.amount,
        type: row.type,
        account_id: accountId,
        category_id: row.category_id,
      }));

    const missingCategory = itemsToImport.some((item) => !item.category_id);
    if (missingCategory) {
      alert("Existem linhas sem categoria selecionada.");
      return;
    }

    confirmMutation.mutate(itemsToImport, {
      onSuccess: () => onClose(),
    });
  }

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "1.5rem",
          borderRadius: "8px",
          width: "90%",
          maxWidth: "800px",
          maxHeight: "85vh",
          overflowY: "auto",
        }}
      >
        <h2>Importar CSV</h2>

        {/* Etapa 1: upload */}
        {rows.length === 0 && (
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            <input type="file" accept=".csv" onChange={handleFileChange} />
            <div style={{ display: "flex", gap: "0.5rem" }}>
              <button onClick={handlePreview} disabled={!file || previewMutation.isPending}>
                {previewMutation.isPending ? "Processando..." : "Analisar arquivo"}
              </button>
              <button onClick={onClose}>Cancelar</button>
            </div>
            {previewMutation.isError && (
              <p style={{ color: "red" }}>Erro ao processar o arquivo. Confira o formato do CSV.</p>
            )}
          </div>
        )}

        {/* Etapa 2: revisão */}
        {rows.length > 0 && (
          <div>
            <div style={{ marginBottom: "1rem" }}>
              <label>Importar para a conta:</label>
              <select value={accountId} onChange={(e) => setAccountId(e.target.value)}>
                <option value="">Selecione...</option>
                {accounts?.map((account) => (
                  <option key={account.id} value={account.id}>
                    {account.name}
                  </option>
                ))}
              </select>
            </div>

            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.9rem" }}>
              <thead>
                <tr>
                  <th style={{ textAlign: "left" }}>Incluir</th>
                  <th style={{ textAlign: "left" }}>Data</th>
                  <th style={{ textAlign: "left" }}>Descrição</th>
                  <th style={{ textAlign: "left" }}>Valor</th>
                  <th style={{ textAlign: "left" }}>Tipo</th>
                  <th style={{ textAlign: "left" }}>Categoria</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.row_index} style={{ opacity: row.include ? 1 : 0.4 }}>
                    <td>
                      <input
                        type="checkbox"
                        checked={row.include}
                        onChange={(e) => updateRow(row.row_index, { include: e.target.checked })}
                      />
                    </td>
                    <td>{new Date(row.date).toLocaleDateString("pt-BR")}</td>
                    <td>{row.description}</td>
                    <td>R$ {row.amount.toFixed(2)}</td>
                    <td>{row.type === "income" ? "Receita" : "Despesa"}</td>
                    <td>
                      <select
                        value={row.category_id}
                        onChange={(e) => updateRow(row.row_index, { category_id: e.target.value })}
                        style={{
                          borderColor: row.category_id ? undefined : "red",
                        }}
                      >
                        <option value="">Sem categoria</option>
                        {categories
                          ?.filter((c) => c.type === row.type)
                          .map((category) => (
                            <option key={category.id} value={category.id}>
                              {category.name}
                            </option>
                          ))}
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div style={{ display: "flex", gap: "0.5rem", marginTop: "1rem" }}>
              <button onClick={handleConfirm} disabled={confirmMutation.isPending}>
                {confirmMutation.isPending
                  ? "Importando..."
                  : `Confirmar importação (${rows.filter((r) => r.include).length} itens)`}
              </button>
              <button onClick={onClose}>Cancelar</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}