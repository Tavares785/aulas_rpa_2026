"""
Lab 13: Arquitetura Orientada a Filas (Queue), Processamento Assíncrono
e Resiliência.

Implementa arquitetura Produtor-Consumidor com fila (queue.Queue),
logging corporativo rotativo (RotatingFileHandler) e padrão de Retry
com tenacity para resiliência de rede.
"""

import csv
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import queue
import random
import time

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)


def configurar_logger():
    """Configura o logger com RotatingFileHandler de 1MB por arquivo."""
    diretorio_base = Path(__file__).resolve().parent
    caminho_log = diretorio_base / "app_rpa.log"

    logger = logging.getLogger("RPA_Queue_Bot")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = RotatingFileHandler(
            caminho_log,
            maxBytes=1024 * 1024,  # 1MB
            backupCount=3,
            encoding="utf-8",
        )
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = configurar_logger()


def converter_nota(valor_bruto):
    """Limpa e converte valor textual de nota para float. Inválidos = 0.0."""
    if not valor_bruto:
        return 0.0
    texto_limpo = str(valor_bruto).strip().replace(",", ".")
    try:
        return float(texto_limpo)
    except ValueError:
        return 0.0


def produtor(fila, limite=10):
    """Lê o CSV da AULA07 e adiciona os primeiros 'limite' alunos na fila."""
    caminho_csv = (
        Path(__file__).resolve().parent.parent / "AULA07" / "notas_alunos.csv"
    )

    if not caminho_csv.exists():
        logger.error("Arquivo %s não encontrado!", caminho_csv)
        return

    logger.info("Produtor: Lendo alunos do arquivo %s", caminho_csv)
    total_enfileirados = 0

    with open(caminho_csv, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f, delimiter=";")
        for linha in leitor:
            if total_enfileirados >= limite:
                break

            nome = linha.get("Nome", "").strip()
            ra = linha.get("RA", "").strip()

            registro = {
                "nome": nome,
                "ra": ra,
                "nota01": linha.get("Nota01", ""),
                "tf01": linha.get("TF01", ""),
                "nota02": linha.get("Nota02", ""),
                "tf02": linha.get("TF02", ""),
            }

            fila.put(registro)
            total_enfileirados += 1
            logger.info("Produtor: Aluno enfileirado -> %s (RA: %s)", nome, ra)

    logger.info(
        "Produtor: Finalizado o enfileiramento de %d alunos.",
        total_enfileirados
    )


class ErroConexaoPortal(Exception):
    """Exceção simulada de falha transitória de rede ao lançar nota."""

    pass


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(0.5),
    retry=retry_if_exception_type(ErroConexaoPortal),
    reraise=True,
)
def lancar_nota_portal(ra, media_final, status):
    """Simula o envio da nota ao portal acadêmico com retry resilience."""
    logger.info(
        "Tentando lançar nota no portal para RA: %s (Média: %.2f)...",
        ra,
        media_final,
    )
    # Simula 30% de chance de instabilidade de rede para ativar o retry
    if random.random() < 0.3:
        logger.warning(
            "Falha transitória de rede ao conectar no portal para RA: %s",
            ra
        )
        raise ErroConexaoPortal("Falha de timeout/conexão no portal acadêmico!")

    logger.info(
        "Sucesso! RA: %s registrado no portal com status: %s",
        ra,
        status
    )
    return True


def consumidor(fila):
    """Retira alunos da fila, limpa dados, calcula médias e lança no portal."""
    logger.info("Consumidor: Iniciando processamento dos itens da fila...")
    processados = 0

    while not fila.empty():
        try:
            aluno = fila.get(block=False)
        except queue.Empty:
            break

        nome = aluno["nome"]
        ra = aluno["ra"] or "N/A"

        nota01 = converter_nota(aluno["nota01"])
        tf01 = converter_nota(aluno["tf01"])
        nota02 = converter_nota(aluno["nota02"])
        tf02 = converter_nota(aluno["tf02"])

        # Média bimestral: nota peso 8 + TF peso 2
        # (nota * 0.8 + TF * 0.2 se nota na escala 0-10, ou soma direta)
        # Como no Lab 07 a nota vale até 8 e TF até 2: media = nota01 + tf01
        media_b1 = (nota01 * 0.8) + (tf01 * 0.2) if nota01 > 8 else (
            nota01 + tf01
        )
        media_b2 = (nota02 * 0.8) + (tf02 * 0.2) if nota02 > 8 else (
            nota02 + tf02
        )
        media_final = (media_b1 + media_b2) / 2.0

        status = "APROVADO" if media_final >= 6.0 else "REPROVADO"

        logger.info(
            "Aluno: %s | RA: %s | B1: %.2f | B2: %.2f | Final: %.2f | %s",
            nome,
            ra,
            media_b1,
            media_b2,
            media_final,
            status,
        )

        try:
            lancar_nota_portal(ra, media_final, status)
        except Exception as e:
            logger.error(
                "Falha definitiva ao lançar notas do RA %s após retentativas: %s",
                ra,
                e,
            )

        fila.task_done()
        processados += 1
        time.sleep(0.05)

    logger.info("Consumidor: Finalizado. Total processado: %d", processados)


def main():
    """Função orquestradora da arquitetura orientada a filas."""
    logger.info("=== Iniciando Robô de Lançamento com Filas e Resiliência ===")
    fila_alunos = queue.Queue()

    # 1. Produção: Enfileira os 10 primeiros alunos
    produtor(fila_alunos, limite=10)

    # 2. Consumo: Processa a fila, calcula médias e executa lançamentos com retry
    consumidor(fila_alunos)

    logger.info("=== Processamento concluído com sucesso! ===")


if __name__ == "__main__":
    main()
