import logging
from pathlib import Path

logger = logging.getLogger("processador_csv")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    file_handler = logging.FileHandler("execucao_bot.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def processar_arquivo(caminho: str):
    """Processa um arquivo CSV e registra logs de auditoria."""
    try:
        with Path(caminho).open("r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                logger.info("Linha lida: %s", linha.rstrip("\n"))
    except FileNotFoundError:
        logger.error("Arquivo não encontrado: %s", caminho)
    finally:
        logger.info("Tentativa de processamento encerrada para: %s", caminho)
