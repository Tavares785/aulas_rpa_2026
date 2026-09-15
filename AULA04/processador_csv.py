import logging

# Configuração do módulo logging para gravar no arquivo 'execucao_bot.log' e exibir no console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def processar_arquivo(caminho: str) -> None:
    """Abre o arquivo CSV fornecido, lê as linhas registrando logs e trata erros de arquivo não encontrado."""
    logging.info(f"Iniciando o processamento do arquivo: {caminho}")
    
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                # Remove espaços em branco e quebras de linha para o log ficar limpo
                linha_limpa = linha.strip()
                if linha_limpa:
                    logging.info(f"Linha lida: {linha_limpa}")
                    
    except FileNotFoundError:
        logging.error(f"Erro crítico: O arquivo '{caminho}' não foi encontrado.")
        
    finally:
        logging.info(f"Término da tentativa de processamento do arquivo: {caminho}")