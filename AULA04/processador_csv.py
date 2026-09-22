import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("execucao_bot.log"),
        logging.StreamHandler()
    ]
)


def processar_arquivo(caminho: str):
    try:
        with open(caminho, mode="r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                logging.info(f"Linha lida: {linha}")
    except FileNotFoundError: 
        logging.error(f"Arquivo não encontrado: {caminho}")
    finally:
        logging.info("Tentativa de processamento finalizada")


processar_arquivo("pneumoultramicroscopiosilicovulcanicoconiotico.csv")
