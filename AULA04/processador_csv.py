import logging
import sys

# Configuração do logging (Arquivo e Console)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)  # Exibe no console
    ]
)
 
 
def processar_arquivo(caminho: str):
    try:
        # Gerenciador de contexto 'with' para fechar o arquivo automaticamente
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                # Grava log INFO para cada linha lida
                logging.info(f"Linha lida: {linha.strip()}")
                
    except FileNotFoundError:
        # Captura erro se o arquivo não existir e grava log de ERROR
        logging.error(f"Erro: O arquivo '{caminho}' não foi encontrado.")
        
    finally:
        # Bloco que sempre executa no final, independentemente de erro
        logging.info("Término da tentativa de processamento do arquivo.")


# Código para testar a função caso você queira rodar localmente:
if __name__ == "__main__":
    processar_arquivo("teste.csv")
