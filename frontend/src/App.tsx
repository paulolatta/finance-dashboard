import { useAccounts } from "./features/accounts/hooks";

function App() {
  const { data: accounts, isLoading, error } = useAccounts();

  if (isLoading) return <p>Carregando contas...</p>;
  if (error) return <p>Erro ao buscar contas: {String(error)}</p>;

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Contas</h1>
      <ul>
        {accounts?.map((account) => (
          <li key={account.id}>
            {account.name} — {account.type} — R$ {account.initial_balance}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;