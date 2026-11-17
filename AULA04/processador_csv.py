import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    formato = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    arquivo_handler = logging.FileHandler("execucao_bot.log", encoding="utf-8")
    arquivo_handler.setFormatter(formato)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formato)

    logger.addHandler(arquivo_handler)
    logger.addHandler(console_handler)


def processar_arquivo(caminho: str):
    """Le um arquivo e registra cada linha processada."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                logger.info("Linha lida: %s", linha.rstrip("\n"))
    except FileNotFoundError:
        logger.error("Arquivo nao encontrado: %s", caminho)
    finally:
        logger.info("Fim da tentativa de processamento: %s", caminho)