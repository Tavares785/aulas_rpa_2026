import logging


FORMATO_LOG = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=FORMATO_LOG,
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def processar_arquivo(caminho: str):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                logger.info("Linha lida: %s", linha.rstrip("\n"))
    except FileNotFoundError:
        logger.error("Arquivo não encontrado: %s", caminho)
    finally:
        logger.info("Término da tentativa de processamento: %s", caminho)