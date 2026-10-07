import logging


FORMATO_LOG = "%(asctime)s - %(levelname)s - %(message)s"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatador = logging.Formatter(FORMATO_LOG)

    arquivo_handler = logging.FileHandler("execucao_bot.log", encoding="utf-8")
    arquivo_handler.setFormatter(formatador)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatador)

    logger.addHandler(arquivo_handler)
    logger.addHandler(console_handler)

logger.propagate = False


def processar_arquivo(caminho: str):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                logger.info("Linha lida: %s", linha.rstrip("\n"))
    except FileNotFoundError:
        logger.error("Arquivo nao encontrado: %s", caminho)
    finally:
        logger.info("Termino da tentativa de processamento: %s", caminho)
