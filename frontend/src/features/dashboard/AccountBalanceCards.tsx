import { useAccountBalances } from "./hooks";

export function AccountBalanceCards() {
  const { data, isLoading } = useAccountBalances();

  if (isLoading) return <p>Carregando saldos...</p>;

  if (!data || data.length === 0) {
    return <p>Nenhuma conta cadastrada.</p>;
  }

  return (
    <div>
      <h3>Saldo por conta</h3>
      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
        {data.map((account) => (
          <div
            key={account.account_id}
            style={{
              border: "1px solid #eee",
              borderRadius: "8px",
              padding: "1rem",
              minWidth: "180px",
            }}
          >
            <p style={{ margin: 0, fontSize: "0.85rem", color: "#666" }}>
              {account.account_name}
            </p>
            <p
              style={{
                margin: "0.25rem 0 0",
                fontSize: "1.3rem",
                fontWeight: "bold",
                color: account.current_balance >= 0 ? "#22C55E" : "#EF4444",
              }}
            >
              R$ {account.current_balance.toFixed(2)}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}