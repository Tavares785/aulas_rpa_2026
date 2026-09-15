"""
Processador de CSV com tratamento de exceções e logging.

Este módulo implementa leitura resiliente de arquivos CSV com:
- Tratamento de exceções (FileNotFoundError)
- Logging estruturado em arquivo e console
- Rastreamento de execução do bot
"""

import logging
import os

# Configurar logging
log_file = "execucao_bot.log"
log_format = "%(asctime)s - %(levelname)s - %(message)s"
date_format = "%d/%m/%Y %H:%M:%S"

# Handler para arquivo
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

# Configurar logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

logger = logging.getLogger(__name__)


def processar_arquivo(caminho: str):
    """
    Processa um arquivo CSV com tratamento de exceções e logging.
    
    Abre o arquivo especificado, lê suas linhas e registra cada uma em log.
    Trata exceções de arquivo não encontrado e registra o término da operação.
    
    Args:
        caminho (str): Caminho do arquivo CSV a ser processado
        
    Returns:
        None
    """
    try:
        logger.info(f"Iniciando processamento do arquivo: {caminho}")
        
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            
            for numero_linha, linha in enumerate(linhas, start=1):
                conteudo = linha.strip()
                logger.info(f"Linha {numero_linha}: {conteudo}")
            
            logger.info(f"Total de {len(linhas)} linhas processadas do arquivo {caminho}")
    
    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {caminho}")
    
    except Exception as e:
        logger.error(f"Erro ao processar arquivo {caminho}: {type(e).__name__} - {e}")
    
    finally:
        logger.info(f"Término da tentativa de processamento do arquivo: {caminho}")
