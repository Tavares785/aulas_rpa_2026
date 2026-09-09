import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

file_handler = logging.FileHandler('execucao_bot.log', encoding='utf-8')
file_handler.setFormatter(formato)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formato)
logger.addHandler(console_handler)

def processar_arquivo(caminho: str):
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                conteudo_linha = linha.strip()
                logging.info(f"Linha lida com sucesso: {conteudo_linha}")
                
    except FileNotFoundError:
        logging.error(f"ERRO CRÍTICO: Arquivo não encontrado no caminho: {caminho}")
        
    finally:  # Correção do 'Finally' para minúsculo
        logging.info("Fim da tentativa de processamento.")

if __name__ == "__main__":
    print("--- TESTE 1: Arquivo que Não existe ---")
    processar_arquivo("dados_clientes.csv")
