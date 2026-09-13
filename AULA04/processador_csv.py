import logging

# Configuração do logger para gravar no arquivo execucao_bot.log e exibir no console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def processar_arquivo(caminho: str) -> None:
    """Abre um arquivo, lê suas linhas gravando logs e trata exceções."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                logging.info(f"Linha lida: {linha.strip()}")
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado no caminho: {caminho}")
    finally:
        logging.info("Tentativa de processamento finalizada.")


if __name__ == "__main__":
    # Teste de arquivo existente (crie um arquivo dados.csv para testar se desejar)
    processar_arquivo("dados.csv")
    
    # Teste de arquivo inexistente para disparar a exceção do FileNotFoundError
    processar_arquivo("arquivo_inexistente.csv")
    