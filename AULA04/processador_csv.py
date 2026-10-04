import csv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def processar_arquivo(caminho: str):
    try:
        logging.info(f"Iniciando tentativa de leitura do arquivo: {caminho}")
        
        with open(caminho, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                logging.info(f"Linha lida: {linha}")

    except FileNotFoundError:
        logging.error(f"Erro: O arquivo '{caminho}' não foi encontrado.")

    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado ao processar o arquivo: {e}")

    finally:
        logging.info("Tentativa de processamento finalizada.")


if __name__ == "__main__":
    processar_arquivo("arquivo_inexistente.csv")