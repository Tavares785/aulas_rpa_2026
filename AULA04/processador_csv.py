import logging
import pathlib

# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def processar_arquivo(caminho):
    """
    Processa um arquivo CSV, registrando as operações no log.
    
    Args:
        caminho: Caminho para o arquivo CSV a processar
    """
    try:
        arquivo = pathlib.Path(caminho)
        
        if not arquivo.exists():
            logger.warning(f"Arquivo não encontrado: {caminho}")
            return
        
        logger.info(f"Iniciando processamento do arquivo: {caminho}")
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            logger.info(f"Arquivo processado com sucesso. Total de linhas: {len(linhas)}")
            
    except FileNotFoundError:
        logger.error(f"Erro ao acessar arquivo: {caminho}")
        # Não relança a exceção - trata internamente
    except Exception as e:
        logger.error(f"Erro ao processar arquivo: {e}")
