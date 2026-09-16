import logging


logger = logging.getLogger()

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler("execucao_bot.log")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def processar_arquivo(caminho: str):
    try:
        with open(caminho, "r") as arquivo:
            for linha in arquivo:
                logger.info(f"Linha lida: {linha.strip()}")

    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {caminho}")

    finally:
        logger.info("Término da tentativa de processamento.")

processar_arquivo("cliente.csv")

