import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formato = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

arquivo_log = logging.FileHandler(
    "execucao_bot.log",
    encoding="utf-8"
)

console = logging.StreamHandler()

arquivo_log.setFormatter(formato)
console.setFormatter(formato)

logger.addHandler(arquivo_log)
logger.addHandler(console)


def processar_arquivo(caminho: str):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                logger.info(f"Linha lida: {linha}")

    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {caminho}")

    finally:
        logger.info("Término da tentativa de processamento.")


processar_arquivo("dados.csv")