import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
def processar_arquivo(caminho: str):
    logging.info(f"Iniciando tentativa de processamento do arquivo: {caminho}")

    try:
        with open(caminho, mode='r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

    for num, linha in enumerate(linhas, start=1):
        linha_limpa = linha.strip()
        logging.info(f"Linha {num} lida com sucesso: {linha_limpa}")
    
    except FileNotFoundError:
    logging.error(f"Erro crítico: O arquivo '{caminho} não foi encontrado.")

    finally:
    logging.info(f"Finalizada a tentativa de processamento para o arquivo: {caminho}\n")

    if __name__ == "__main__":
        processar_arquivo("arquivo_inexistente.csv .")


