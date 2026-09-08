import csv
from pathlib import Path

def carregar_transacoes(caminho_csv):
    """Lê o arquivo CSV e retorna uma lista de dicionários."""
    transacoes = []
    with open(caminho_csv, mode="r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            transacoes.append({
                "id": linha["id"],
                "valor": float(linha["transacao"]),
                "status_inicial": linha["status"]
            })
    return transacoes

def classificar_transacao(valor):
    """Aplica as regras de negócio sobre o valor da transação."""
    if valor <= 0:
        return "REJEITADO_ERRO"
    elif valor > 10000.0:
        return "ENCAMINHADO_AUDITORIA"
    return "APROVADO"

if __name__ == "__main__":
    caminho = Path(__file__).parent.parent / "dados csv" / "dados_transacoes.csv"
    dados = carregar_transacoes(caminho)
    print(f"=== MÓDULO AULA 03: {len(dados)} TRANSAÇÕES CARREGADAS ===")
