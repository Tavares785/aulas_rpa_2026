import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("execucao_bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def processar_arquivo(caminho: str):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                logging.info(f"Linha lida: {linha.strip()}")
    
    except FileNotFoundError:
        logger.error("Arquivo não encontrado: {caminho}")

    finally:
        logger.info("Término da tentativa de processamento do arquivo")


processar_arquivo("dados.csv")