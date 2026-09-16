import logging # registrar o que acontece no programa

logging.basicConfig(
    level=logging.INFO, # registrar mensagens INFO
    format="%(asctime)s - %(levelname)s - %(message)s"
)

arquivo_log = logging.FileHandler("execucao_bot.log")
logging.getLogger().addHandler(arquivo_log)


def processar_arquivo(caminho: str):
    try:
        with open(caminho, 'r') as arquivo:

            for linha in arquivo:
                logging.info(f"Linha lida: {linha.strip()}")

    except FileNotFoundError:
        logging.error(f"Arquivo {caminho} não encontrado.")

    except Exception as e:
        logging.error(f"Ocorreu um erro ao processar o arquivo {caminho}: {e}")

    finally:
        logging.info("Fim do processamento.")

processar_arquivo("EXEMPLOS/arquivos/texto.txt")