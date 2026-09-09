import logging

format_log = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(
    level=logging.INFO,
    format=format_log,
    handlers=[
        logging.FileHandler('execucao_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


def processar_arquivo(caminho: str):
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                logging.info(f'Processando linha: {linha.strip()}')
    except FileNotFoundError:
        logging.error(f'Arquivo no caminho {caminho} não encontrado.')

    finally:
        logging.info(f'Terminado o processamento do arquivo: {caminho}')


if __name__ == '__main__':
    caminho_arquivo = 'EXEMPLOS/arquivos/dados.csv'
    processar_arquivo(caminho_arquivo)
