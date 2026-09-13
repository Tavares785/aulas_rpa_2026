"""
processador_csv.py
Lab 04 – Resiliência do Bot: Persistência, Exceções e Trilha de Auditoria

Objetivos:
- Manipular arquivos CSV com o gerenciador de contexto `with`.
- Tratar FileNotFoundError com try/except/finally.
- Gerar logs estruturados (INFO / ERROR / WARNING) gravados em arquivo e console.
"""

import logging
import pathlib

# ---------------------------------------------------------------------------
# Configuração do logging
# ---------------------------------------------------------------------------
# Formato: 2026-09-13 14:35:22 | INFO | mensagem
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# O log é gravado no mesmo diretório do script para facilitar auditoria.
LOG_FILE = pathlib.Path(__file__).parent / "execucao_bot.log"

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        # Grava em arquivo
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        # Exibe no console
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------
def processar_arquivo(caminho: str) -> None:
    """Lê um arquivo CSV linha a linha com auditoria completa por logs.

    Args:
        caminho: Caminho absoluto ou relativo para o arquivo CSV.
    """
    logger.info("=" * 60)
    logger.info("Iniciando processamento do arquivo: %s", caminho)

    try:
        with open(caminho, encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

        total = len(linhas)
        logger.info("Arquivo aberto com sucesso. Total de linhas: %d", total)

        for numero, linha in enumerate(linhas, start=1):
            conteudo = linha.rstrip("\n")
            logger.info("Linha %d: %s", numero, conteudo)

        logger.info("Processamento concluído. %d linha(s) lida(s).", total)

    except FileNotFoundError:
        logger.error(
            "Arquivo não encontrado: '%s'. "
            "Verifique se o caminho está correto.",
            caminho,
        )
    except PermissionError:
        logger.error(
            "Sem permissão para ler o arquivo: '%s'.", caminho
        )
    except Exception as excecao:
        logger.error(
            "Erro inesperado ao processar '%s': %s", caminho, excecao
        )
    finally:
        logger.info(
            "Tentativa de processamento finalizada para: %s", caminho
        )
        logger.info("=" * 60)


# ---------------------------------------------------------------------------
# Execução direta (opcional – não é executado durante os testes unitários)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Exemplo com arquivo válido
    csv_exemplo = pathlib.Path(__file__).parent.parent / "EXEMPLOS" / "arquivos" / "dados.csv"
    processar_arquivo(str(csv_exemplo))

    # Exemplo com arquivo inexistente para demonstrar o tratamento de erro
    processar_arquivo("/caminho/inexistente/fake.csv")
