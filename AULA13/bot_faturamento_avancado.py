"""
AULA 13 - Arquitetura Orientada a Filas (Queue), Processamento Assíncrono e Resiliência

Bot de lançamento avançado de notas que reaproveita a base da AULA07
(`AULA07/notas_alunos.csv`) aplicando:
1. Logging corporativo com rotação automática (`RotatingFileHandler` em `app_rpa.log`, 1 MB).
2. Arquitetura Produtor-Consumidor utilizando `queue.Queue`.
3. Processamento concorrente/assíncrono de workers com `asyncio`.
4. Padrão de resiliência (*Retry Pattern*) com `tenacity` (até 3 tentativas)
   para tolerância a falhas aleatórias de rede ao lançar notas no portal.
"""
from __future__ import annotations

import asyncio
import csv
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import queue
import random
from typing import Any

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# ---------------------------------------------------------------------------
# Configurações gerais
# ---------------------------------------------------------------------------
LOG_FILE = "app_rpa.log"
LOG_MAX_BYTES = 1 * 1024 * 1024  # 1 MB por arquivo
LOG_BACKUP_COUNT = 3

CAMINHO_CSV = Path(__file__).resolve().parent.parent / "AULA07" / "notas_alunos.csv"
LIMITE_ALUNOS = 10
NUM_WORKERS = 3
MEDIA_APROVACAO = 6.0
PROBABILIDADE_FALHA_REDE = 0.35
VALORES_INVALIDOS = {"", "FALTOU", "FALTA", "N/A", "NA", "NONE", "-"}


# ---------------------------------------------------------------------------
# 1. Configuração de Logging Rotativo (RotatingFileHandler)
# ---------------------------------------------------------------------------

def configurar_logger() -> logging.Logger:
    """Configura o logger com RotatingFileHandler (1 MB) em app_rpa.log e saída no terminal."""
    log = logging.getLogger("bot_faturamento_avancado")
    log.setLevel(logging.INFO)
    log.propagate = False

    if not log.handlers:
        formato = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(formato)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formato)

        log.addHandler(file_handler)
        log.addHandler(stream_handler)

    return log


logger = configurar_logger()


# ---------------------------------------------------------------------------
# 2. Higienização de dados e cálculo de médias
# ---------------------------------------------------------------------------

def limpar_nome(valor: str | None) -> str:
    """Remove espaços extras e padroniza a capitalização do nome do aluno."""
    partes = (valor or "").split()
    return " ".join(partes).title() if partes else "SEM NOME"


def limpar_ra(valor: str | None) -> str:
    """Normaliza o RA removendo espaços, prefixos ('RA'), sufixos e zeros à esquerda."""
    texto = (valor or "").strip().upper()
    if not texto:
        return "SEM_RA"

    texto = texto.split("-")[0]
    if texto.startswith("RA"):
        texto = texto[2:]

    digitos = "".join(ch for ch in texto if ch.isdigit()).lstrip("0")
    return digitos or "SEM_RA"


def limpar_nota(valor: str | None, limite_maximo: float) -> float:
    """Converte uma nota/TF suja para float; valores inválidos contam como 0.0."""
    texto = (valor or "").strip()
    if texto.upper() in VALORES_INVALIDOS:
        return 0.0

    texto_normalizado = texto.replace(",", ".")
    try:
        numero = float(texto_normalizado)
    except ValueError:
        return 0.0

    return max(0.0, min(numero, limite_maximo))


def calcular_resultado_aluno(aluno_bruto: dict[str, str]) -> dict[str, Any]:
    """
    Limpa os campos do aluno e calcula as médias bimestrais e a média final.

    Regras (base AULA07):
    - Nota (0..10) tem peso 8 (fator 0.8) + TF (0..2) tem peso 2 (soma direta até 2.0).
    - Média final = média aritmética dos dois bimestres.
    - Status: APROVADO se média final >= 6.0, senão REPROVADO.
    """
    nome = limpar_nome(aluno_bruto.get("Nome"))
    ra = limpar_ra(aluno_bruto.get("RA"))

    nota01 = limpar_nota(aluno_bruto.get("Nota01"), limite_maximo=10.0)
    tf01 = limpar_nota(aluno_bruto.get("TF01"), limite_maximo=2.0)
    nota02 = limpar_nota(aluno_bruto.get("Nota02"), limite_maximo=10.0)
    tf02 = limpar_nota(aluno_bruto.get("TF02"), limite_maximo=2.0)

    media_b1 = round(nota01 * 0.8 + tf01, 2)
    media_b2 = round(nota02 * 0.8 + tf02, 2)
    media_final = round((media_b1 + media_b2) / 2, 2)
    status = "APROVADO" if media_final >= MEDIA_APROVACAO else "REPROVADO"

    return {
        "nome": nome,
        "ra": ra,
        "media_b1": media_b1,
        "media_b2": media_b2,
        "media_final": media_final,
        "status": status,
    }


# ---------------------------------------------------------------------------
# 3. Lançamento no portal com Retry Pattern (tenacity)
# ---------------------------------------------------------------------------

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.2, min=0.2, max=1.0),
    retry=retry_if_exception_type(ConnectionError),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def lancar_nota_portal(registro: dict[str, Any]) -> None:
    """
    Simula o envio da nota calculada para o portal acadêmico.

    Possui falha aleatória de rede (ConnectionError) para exercitar o Retry
    automático via tenacity (até 3 tentativas com backoff exponencial).
    """
    if random.random() < PROBABILIDADE_FALHA_REDE:
        raise ConnectionError(
            f"Falha temporária de rede ao lançar nota de {registro['nome']} (RA {registro['ra']})."
        )

    logger.info(
        "[PORTAL OK] %s | RA: %s | B1: %.2f | B2: %.2f | Final: %.2f | %s",
        registro["nome"],
        registro["ra"],
        registro["media_b1"],
        registro["media_b2"],
        registro["media_final"],
        registro["status"],
    )


# ---------------------------------------------------------------------------
# 4. Arquitetura Produtor-Consumidor (queue.Queue + asyncio)
# ---------------------------------------------------------------------------

def produtor(caminho_csv: Path, fila: queue.Queue[dict[str, str]], limite: int = LIMITE_ALUNOS) -> int:
    """Lê o CSV da AULA07 (separador ';') e enfileira os `limite` primeiros alunos."""
    if not caminho_csv.exists():
        raise FileNotFoundError(f"Base de notas não encontrada: {caminho_csv}")

    enfileirados = 0
    with caminho_csv.open(mode="r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        for linha in leitor:
            if enfileirados >= limite:
                break
            fila.put(linha)
            enfileirados += 1
            logger.info(
                "[PRODUTOR] Enfileirado (%d/%d): %s",
                enfileirados,
                limite,
                limpar_nome(linha.get("Nome")),
            )

    logger.info("[PRODUTOR] Carga concluída: %d aluno(s) adicionado(s) na fila.", enfileirados)
    return enfileirados


async def consumidor(
    worker_id: int,
    fila: queue.Queue[dict[str, str]],
    resumo: dict[str, int],
) -> None:
    """Worker assíncrono que retira alunos da fila, calcula médias e lança no portal."""
    while True:
        try:
            aluno_bruto = fila.get(block=False)
        except queue.Empty:
            break

        try:
            registro = calcular_resultado_aluno(aluno_bruto)
            await asyncio.sleep(0.05)  # Simula latência de I/O assíncrono
            await asyncio.to_thread(lancar_nota_portal, registro)

            resumo["sucesso"] += 1
            if registro["status"] == "APROVADO":
                resumo["aprovados"] += 1
            else:
                resumo["reprovados"] += 1
        except ConnectionError as erro:
            resumo["falhas"] += 1
            logger.error(
                "[WORKER-%d] Falha definitiva após 3 tentativas (%s): %s",
                worker_id,
                limpar_nome(aluno_bruto.get("Nome")),
                erro,
            )
        finally:
            fila.task_done()


async def executar_pipeline(caminho_csv: Path = CAMINHO_CSV, limite: int = LIMITE_ALUNOS) -> dict[str, int]:
    """Orquestra a fila Produtor-Consumidor com workers assíncronos."""
    logger.info("=== Iniciando Bot de Faturamento Avançado (Lab 13) ===")
    fila: queue.Queue[dict[str, str]] = queue.Queue()
    total = produtor(caminho_csv, fila, limite=limite)

    resumo = {
        "total": total,
        "sucesso": 0,
        "falhas": 0,
        "aprovados": 0,
        "reprovados": 0,
    }

    workers = [consumidor(i, fila, resumo) for i in range(1, NUM_WORKERS + 1)]
    await asyncio.gather(*workers)
    fila.join()

    logger.info(
        "=== Resumo Final | Total: %d | Sucesso: %d | Falhas: %d | Aprovados: %d | Reprovados: %d ===",
        resumo["total"],
        resumo["sucesso"],
        resumo["falhas"],
        resumo["aprovados"],
        resumo["reprovados"],
    )
    return resumo


def main() -> None:
    """Ponto de entrada do bot."""
    asyncio.run(executar_pipeline())


if __name__ == "__main__":
    main()
