import logging
import os

# Configuração do módulo de logging para gravar em arquivo e exibir no console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def processar_arquivo(caminho: str) -> None:
    """
    Lê um arquivo CSV/TXT linha por linha, registrando logs de auditoria
    e tratando exceções de arquivo não encontrado.
    """
    logging.info(f"Iniciando tentativa de processamento do arquivo: {caminho}")
    
    try:
        # Uso do gerenciador de contexto 'with' para abertura segura do arquivo
        with open(caminho, mode="r", encoding="utf-8") as arquivo:
            for numero_linha, linha in enumerate(arquivo, start=1):
                conteudo = linha.strip()
                logging.info(f"Linha {numero_linha} lida com sucesso: {conteudo}")
                
    except FileNotFoundError:
        logging.error(f"Erro: O arquivo '{caminho}' não foi encontrado.")
        
    except Exception as e:
        logging.error(f"Erro inesperado ao processar o arquivo '{caminho}': {e}")
        
    finally:
        logging.info(f"Término da tentativa de processamento do arquivo: {caminho}")


if __name__ == "__main__":
    # Exemplo de teste com arquivo inexistente (gera log ERROR)
    processar_arquivo("dados_inexistentes.csv")

    # Exemplo de teste com arquivo existente (gera logs INFO)
    caminho_teste = "dados_exemplo.csv"
    
    # Criando um arquivo temporário de teste se ele não existir
    if not os.path.exists(caminho_teste):
        with open(caminho_teste, "w", encoding="utf-8") as f:
            f.write("id,transacao,valor\n")
            f.write("1,TRX1001,150.00\n")
            f.write("2,TRX1002,230.50\n")
            
    processar_arquivo(caminho_teste)



