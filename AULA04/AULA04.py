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
  
    logger.info("Iniciando processamento do arquivo: %s", caminho)

    try:
        with open(caminho, mode="r", encoding="utf-8") as arquivo:
            for numero_linha, linha in enumerate(arquivo, start=1):
                conteudo = linha.strip()
                logger.info("Linha %d lida: %s", numero_linha, conteudo)

    except FileNotFoundError:
        logger.error("Arquivo não encontrado: %s", caminho)

    except Exception as erro:
        logger.error("Erro inesperado ao processar '%s': %s", caminho, erro)

    finally:
        logger.info("Tentativa de processamento do arquivo '%s' finalizada.", caminho)


if __name__ == "__main__":
    processar_arquivo("dados.csv")
    processar_arquivo("arquivo_que_nao_existe.csv")