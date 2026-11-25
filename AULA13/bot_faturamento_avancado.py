
import csv
import asyncio
import logging
import queue

from pathlib import Path
from logging.handlers import RotatingFileHandler

from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
    retry_if_exception_type,
    before_sleep_log
)

# ==================================================
# 1. CAMINHOS DOS ARQUIVOS
# ==================================================

PASTA_PROJETO = Path(__file__).resolve().parent.parent

ARQUIVO_CSV = PASTA_PROJETO / "TF-07" / "notas.csv"
ARQUIVO_LOG = Path(__file__).resolve().parent / "app_rpa.log"

fila_alunos = queue.Queue()
SENTINELA = object()

# ==================================================
# 2. CONFIGURAÇÃO DO LOG ROTATIVO
# ==================================================

logger = logging.getLogger("BOT_RPA")
logger.setLevel(logging.INFO)
logger.propagate = False

logger.handlers.clear()

handler = RotatingFileHandler(
    ARQUIVO_LOG,
    maxBytes=1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)

formato = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

handler.setFormatter(formato)
logger.addHandler(handler)

# ==================================================
# 3. LIMPEZA DAS NOTAS
# ==================================================

def limpar_nota(valor):

    if valor is None:
        return 0.0

    valor = str(valor).strip().upper()

    if valor in ("", "FALTOU", "N/A", "NA"):
        return 0.0

    try:
        return float(valor.replace(",", "."))

    except ValueError:
        logger.warning(
            "Valor inválido encontrado: %s. Considerado zero.",
            valor
        )
        return 0.0

# ==================================================
# 4. PRODUTOR: LEITURA DO CSV E ALIMENTAÇÃO DA FILA
# ==================================================

def produtor():

    logger.info("PRODUTOR: iniciando leitura do CSV.")

    try:

        if not ARQUIVO_CSV.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {ARQUIVO_CSV}"
            )

        with open(
            ARQUIVO_CSV,
            mode="r",
            encoding="utf-8-sig",
            newline=""
        ) as arquivo:

            leitor = csv.DictReader(
                arquivo,
                delimiter=";"
            )

            colunas_obrigatorias = {
                "Nome", "RA", "Nota01",
                "TF01", "Nota02", "TF02"
            }

            if not colunas_obrigatorias.issubset(
                set(leitor.fieldnames or [])
            ):
                raise ValueError(
                    "As colunas do CSV não correspondem "
                    "ao formato esperado."
                )

            quantidade = 0

            for aluno in leitor:

                if quantidade >= 10:
                    break

                fila_alunos.put(aluno)

                quantidade += 1

                logger.info(
                    "PRODUTOR: aluno %s adicionado à fila. RA: %s",
                    aluno.get("Nome", "").strip(),
                    aluno.get("RA", "").strip()
                )

        logger.info(
            "PRODUTOR: leitura finalizada. Total: %d alunos.",
            quantidade
        )

    except Exception:

        logger.exception(
            "PRODUTOR: erro durante a leitura do CSV."
        )

        raise

    finally:

        # Avisa o consumidor que não existem mais alunos.
        fila_alunos.put(SENTINELA)

# ==================================================
# 5. SIMULAÇÃO DE LANÇAMENTO NO PORTAL COM RETRY
# ==================================================

falha_rede_simulada = False

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    retry=retry_if_exception_type(ConnectionError),
    before_sleep=before_sleep_log(
        logger,
        logging.WARNING
    ),
    reraise=True
)
def lancar_nota_portal(nome, ra, media_final, situacao):

    global falha_rede_simulada

    logger.info(
        "PORTAL: tentando lançar nota do aluno %s.",
        nome
    )

    # Simula uma falha de rede na primeira tentativa.
    # O Tenacity fará automaticamente uma nova tentativa.

    if not falha_rede_simulada:

        falha_rede_simulada = True

        raise ConnectionError(
            "Falha simulada de conexão com o portal."
        )

    logger.info(
        "PORTAL: lançamento realizado com sucesso. "
        "Aluno: %s | RA: %s | Média: %.2f | Situação: %s",
        nome,
        ra,
        media_final,
        situacao
    )

# ==================================================
# 6. CONSUMIDOR: PROCESSAMENTO DOS ALUNOS
# ==================================================

def consumidor():

    logger.info("CONSUMIDOR: iniciado.")

    while True:

        aluno = fila_alunos.get()

        try:

            if aluno is SENTINELA:

                logger.info(
                    "CONSUMIDOR: fila finalizada."
                )

                break

            # Identificação do aluno
            nome = str(
                aluno.get("Nome", "")
            ).strip()

            ra = str(
                aluno.get("RA", "")
            ).strip()

            if not nome:
                nome = "Aluno sem nome"

            if not ra:
                ra = "RA não informado"

            # Limpeza das notas
            nota01 = limpar_nota(aluno.get("Nota01"))
            tf01 = limpar_nota(aluno.get("TF01"))

            nota02 = limpar_nota(aluno.get("Nota02"))
            tf02 = limpar_nota(aluno.get("TF02"))

            # Cálculo das médias bimestrais
            # Nota peso 8 + TF peso 2

            media_bimestre1 = (
                nota01 * 8 + tf01 * 2
            ) / 10

            media_bimestre2 = (
                nota02 * 8 + tf02 * 2
            ) / 10

            # Média final dos dois bimestres

            media_final = (
                media_bimestre1 + media_bimestre2
            ) / 2

            # Definição da situação

            if media_final >= 6:
                situacao = "APROVADO"
            else:
                situacao = "REPROVADO"

            # Registro do processamento

            logger.info(
                "ALUNO: %s | RA: %s | "
                "Média B1: %.2f | Média B2: %.2f | "
                "Média Final: %.2f | Situação: %s",
                nome,
                ra,
                media_bimestre1,
                media_bimestre2,
                media_final,
                situacao
            )

            # Lançamento no portal com retentativa

            try:

                lancar_nota_portal(
                    nome,
                    ra,
                    media_final,
                    situacao
                )

            except ConnectionError:

                logger.exception(
                    "PORTAL: falha definitiva após "
                    "3 tentativas para o aluno %s.",
                    nome
                )

        except Exception:

            logger.exception(
                "CONSUMIDOR: erro ao processar aluno."
            )

        finally:

            fila_alunos.task_done()

# ==================================================
# 7. EXECUÇÃO ASSÍNCRONA COM ASYNCIO
# ==================================================

async def main():

    logger.info("===================================")
    logger.info("INÍCIO DO LABORATÓRIO 13")
    logger.info("===================================")

    try:

        # Produtor e consumidor executados em threads
        # para não bloquear o loop assíncrono.

        await asyncio.gather(
            asyncio.to_thread(produtor),
            asyncio.to_thread(consumidor)
        )

        logger.info(
            "PROCESSAMENTO FINALIZADO COM SUCESSO."
        )

        print("\n===================================")
        print("LABORATÓRIO 13 FINALIZADO!")
        print("===================================")
        print("Alunos processados: confira o arquivo de log.")
        print(f"Arquivo de log: {ARQUIVO_LOG}")

    except Exception:

        logger.exception(
            "ERRO NA EXECUÇÃO PRINCIPAL DO BOT."
        )

        print("Ocorreu um erro. Consulte o arquivo de log.")

# ==================================================
# 8. INICIALIZAÇÃO DO PROGRAMA
# ==================================================

if __name__ == "__main__":

    asyncio.run(main())