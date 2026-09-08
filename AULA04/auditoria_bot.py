import csv
import sys
from pathlib import Path

# Importando o módulo modular da Aula 03
sys.path.append(str(Path(__file__).parent.parent / "AULA03"))
try:
    from processador_dados import carregar_transacoes, classificar_transacao
except ImportError:
    pass

def executar_auditoria(arquivo_entrada, arquivo_saida):
    print("=== AULA 04: EXECUTANDO BOT COM AUDITORIA E EXCEÇÕES ===")
    
    try:
        transacoes = carregar_transacoes(arquivo_entrada)
        resultados = []

        for item in transacoes:
            valor = item["valor"]
            status_final = classificar_transacao(valor)
            
            resultados.append({
                "id": item["id"],
                "valor": valor,
                "status_final": status_final
            })
            print(f"[LOG] ID {item['id']}: R$ {valor} -> Status: {status_final}")

        colunas = ["id", "valor", "status_final"]
        with open(arquivo_saida, mode="w", newline="", encoding="utf-8") as arq_out:
            escritor = csv.DictWriter(arq_out, fieldnames=colunas)
            escritor.writeheader()
            escritor.writerows(resultados)
            
        print(f"\n[SUCESSO] Relatório de auditoria salvo em '{arquivo_saida}'.")

    except FileNotFoundError:
        print(f"[ERRO CRÍTICO] O arquivo '{arquivo_entrada}' não foi localizado.")
    except Exception as e:
        print(f"[FALHA INESPERADA] Ocorreu um erro durante a execução: {e}")

if __name__ == "__main__":
    raiz = Path(__file__).parent.parent
    caminho_in = raiz / "dados csv" / "dados_transacoes.csv"
    caminho_out = Path(__file__).parent / "relatorio_auditoria.csv"
    executar_auditoria(caminho_in, caminho_out)
