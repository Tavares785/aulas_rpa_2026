import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler(
    "execucao_bot.log",
    encoding="utf-8"
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def processar_arquivo(caminho: str) -> None:
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                logger.info("Linha lida: %s", linha.strip())

    except FileNotFoundError:
        logger.error("Arquivo não encontrado: %s", caminho)

    finally:
        logger.info("Tentativa de processamento finalizada.")

        
