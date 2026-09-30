import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def processar_arquivo(caminho: str) -> None:
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for numero_linha, linha in enumerate(arquivo, start=1):
                logger.info("Linha %d lida: %s", numero_linha, linha.rstrip())
    except FileNotFoundError:
        logger.error("Arquivo não encontrado: %s", caminho)
    finally:
        logger.info("Tentativa de processamento finalizada: %s", caminho)