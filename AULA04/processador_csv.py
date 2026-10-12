import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def processar_arquivo(caminho: str):
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            for i, linha in enumerate(linhas, 1):
                logging.info(f"Linha {i} lida: {linha.strip()}")
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {caminho}")
    finally:
        logging.info(f"Tentativa de processamento do arquivo {caminho} finalizada.")

if __name__ == "__main__":
    processar_arquivo("dados.txt")