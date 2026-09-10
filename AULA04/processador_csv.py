import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def processar_arquivo(caminho: str):
    try:
        with open("ile.csv", "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                logging.info(linha.strip())

    except FileNotFoundError:
        logging.error("Arquivo não encontrado")

    finally:
        logging.info("Término da tentativa de processamento.")
processar_arquivo("ile.csv")