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
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                logging.info(f"Linha lida: {linha}")

    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {caminho}")

    finally:
        logging.info(f"Término da tentativa de processamento: {caminho}")