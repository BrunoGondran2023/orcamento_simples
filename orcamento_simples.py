import pandas as pd
import locale
from typing import List, Dict

# Configurar o locale para pt_BR
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class Orcamento:
    def __init__(self) -> None:
        """Inicializa a classe com listas vazias para receitas e despesas e um dicionário para categorias."""
        self.receitas: List[Dict[str, float]] = []
        self.despesas: List[Dict[str, float]] = []
        self.categorias: Dict[str, float] = {}

    def adicionar_receita(self, descricao: str, valor: float) -> None:
        """Adiciona uma nova receita ao orçamento."""
        if valor <= 0:
            raise ValueError('O valor da receita deve ser positivo.')
        self.receitas.append({'descricao': descricao, 'valor': valor})

    def adicionar_despesa(self, descricao: str, valor: float, categoria: str) -> None:
        """Adiciona uma nova despesa ao orçamento."""
        if valor <= 0:
            raise ValueError('O valor da despesa deve ser positivo.')
        self.despesas.append({'descricao': descricao, 'valor': valor, 'categoria': categoria})
        if categoria not in self.categorias:
            self.categorias[categoria] = 0
        self.categorias[categoria] += valor

    def calcular_saldo(self) -> str:
        """Calcula o saldo atual do orçamento."""
        total_receitas = sum(receita['valor'] for receita in self.receitas)
        total_despesas = sum(despesa['valor'] for despesa in self.despesas)
        saldo = total_receitas - total_despesas
        return locale.currency(saldo, grouping=True)

    def gerar_relatorio(self) -> pd.DataFrame:
        """Gera um relatório detalhado das receitas e despesas."""
        receitas_df = pd.DataFrame(self.receitas)
        despesas_df = pd.DataFrame(self.despesas)
        relatorio = pd.concat([receitas_df, despesas_df], keys=['Receitas', 'Despesas'])
        relatorio['valor'] = relatorio['valor'].apply(lambda x: locale.format_string("%.2f", x, grouping=True))
        return relatorio

    def prever_saldo(self, periodo: int) -> str:
        """
        Prevê se o saldo será positivo ou negativo em um determinado período (meses).
        Considera a média das receitas e despesas atuais.
        """
        if not self.receitas or not self.despesas:
            raise ValueError("Insira pelo menos uma receita e uma despesa para prever o saldo.")

        media_receitas = sum(receita['valor'] for receita in self.receitas) / len(self.receitas)
        media_despesas = sum(despesa['valor'] for despesa in self.despesas) / len(self.despesas)

        saldo_atual = sum(receita['valor'] for receita in self.receitas) - sum(despesa['valor'] for despesa in self.despesas)
        saldo_futuro = saldo_atual + (media_receitas - media_despesas) * periodo

        return f"\nPrevisão de saldo para {periodo} meses: {locale.currency(saldo_futuro, grouping=True)}"

# Exemplo de uso
if __name__ == "__main__":
    orcamento = Orcamento()
    orcamento.adicionar_receita("Salário", 5000.50)
    orcamento.adicionar_despesa("Aluguel", 1500.75, "Moradia")
    orcamento.adicionar_despesa("Supermercado", 500.25, "Alimentação")

    print(f"\nSaldo: {orcamento.calcular_saldo()}\n")
    print(orcamento.gerar_relatorio().to_string(index=False))
    print(orcamento.prever_saldo(6))  # Previsão para 6 meses
