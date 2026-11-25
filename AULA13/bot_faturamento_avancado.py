"""
Lab 13 - Arquitetura Orientada a Filas, Processamento Concorrente e Resiliência.

Aluna: Emanuela Oliveira da Costa
RA: 6326085

Reaproveita o cenário do Lab 07 (Lançamento de Notas):
- Produtor: lê o CSV da AULA07 e coloca os 10 primeiros alunos na fila.
- Consumidores (workers): retiram alunos da fila, limpam os dados,
  calculam as médias e lançam a nota no portal (simulado).
- O lançamento simula falhas aleatórias de rede e usa tenacity (@retry)
  com até 3 tentativas.
- Toda a operação é auditada em app_rpa.log com RotatingFileHandler (1MB).

Regra de cálculo (mesma do Lab 07):
- Média do bimestre = Nota (peso 8) + TF (peso 2), ou seja,
  Nota (0 a 10) * 0.8 + TF (0 a 2).
- Média final = média dos dois bimestres.
- APROVADO se média final >= 6, senão REPROVADO.
- Valores inválidos (FALTOU, N/A, vazio etc.) contam como 0.
"""

import csv
import logging
import queue
import random
import re
import threading
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

CAMINHO_CSV = Path(__file__).resolve().parent.parent / "AULA07" / "notas_alunos.csv"
ARQUIVO_LOG = "app_rpa.log"
QTD_ALUNOS = 10
QTD_WORKERS = 3
CHANCE_FALHA_REDE = 0.3
MEDIA_APROVACAO = 6.0
NOTA_MAXIMA = 10.0
TF_MAXIMO = 2.0


def configurar_logging():
    """Configura o logger com RotatingFileHandler (1MB) e saída no console."""
    logger = logging.getLogger("bot_faturamento")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(threadName)s | %(message)s"
    )

    handler_arquivo = RotatingFileHandler(
        ARQUIVO_LOG, maxBytes=1 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    handler_arquivo.setFormatter(formato)

    handler_console = logging.StreamHandler()
    handler_console.setFormatter(formato)

    logger.addHandler(handler_arquivo)
    logger.addHandler(handler_console)
    return logger


logger = configurar_logging()


def converter_valor(valor, maximo):
    """Converte um valor sujo do CSV em float; inválidos viram 0."""
    if valor is None:
        return 0.0

    texto = valor.strip().replace(",", ".")
    try:
        numero = float(texto)
    except ValueError:
        return 0.0

    if numero < 0:
        return 0.0
    return min(numero, maximo)


def limpar_nome(nome):
    """Remove espaços extras e padroniza o nome em formato Título."""
    return " ".join((nome or "").split()).title()


def limpar_ra(ra):
    """Mantém apenas os dígitos do RA."""
    digitos = re.sub(r"\D", "", ra or "")
    return digitos if digitos else "SEM RA"


def calcular_media_bimestre(nota, tf):
    """Média do bimestre: Nota com peso 8 + TF com peso 2."""
    return nota * 0.8 + tf


def processar_aluno(linha):
    """Limpa os dados de um aluno e calcula médias e situação."""
    nota1 = converter_valor(linha.get("Nota01"), NOTA_MAXIMA)
    tf1 = converter_valor(linha.get("TF01"), TF_MAXIMO)
    nota2 = converter_valor(linha.get("Nota02"), NOTA_MAXIMA)
    tf2 = converter_valor(linha.get("TF02"), TF_MAXIMO)

    media1 = calcular_media_bimestre(nota1, tf1)
    media2 = calcular_media_bimestre(nota2, tf2)
    media_final = round((media1 + media2) / 2, 2)
    situacao = "APROVADO" if media_final >= MEDIA_APROVACAO else "REPROVADO"

    return {
        "nome": limpar_nome(linha.get("Nome")),
        "ra": limpar_ra(linha.get("RA")),
        "media_bim1": round(media1, 2),
        "media_bim2": round(media2, 2),
        "media_final": media_final,
        "situacao": situacao,
    }


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(0.5),
    retry=retry_if_exception_type(ConnectionError),
    before_sleep=lambda estado: logger.warning(
        "Falha de rede no lançamento (tentativa %s). Tentando novamente...",
        estado.attempt_number,
    ),
)
def lancar_nota_portal(aluno):
    """Simula o lançamento da nota no portal com falha aleatória de rede."""
    time.sleep(random.uniform(0.05, 0.2))
    if random.random() < CHANCE_FALHA_REDE:
        raise ConnectionError(f"Timeout ao lançar a nota de {aluno['nome']}")

    logger.info(
        "Nota lançada no portal: %s (RA %s) | Média final %.2f | %s",
        aluno["nome"], aluno["ra"], aluno["media_final"], aluno["situacao"],
    )
    return True


def ler_csv():
    """Lê o CSV da AULA07 tentando codificações comuns."""
    for codificacao in ("utf-8-sig", "latin-1"):
        try:
            with open(CAMINHO_CSV, encoding=codificacao, newline="") as arquivo:
                return list(csv.DictReader(arquivo, delimiter=";"))
        except UnicodeDecodeError:
            continue
    return []


def produtor(fila, quantidade=QTD_ALUNOS):
    """Lê o CSV e adiciona os primeiros alunos na fila."""
    logger.info("Produtor iniciado. Lendo %s", CAMINHO_CSV)
    linhas = ler_csv()

    for linha in linhas[:quantidade]:
        fila.put(linha)
        logger.info("Aluno enfileirado: %s", limpar_nome(linha.get("Nome")))

    logger.info("Produtor finalizado: %d aluno(s) na fila.", min(quantidade, len(linhas)))


def consumidor(fila, resultados, trava):
    """Worker que retira alunos da fila, processa e lança a nota."""
    while True:
        linha = fila.get()
        if linha is None:
            fila.task_done()
            break

        try:
            aluno = processar_aluno(linha)
            try:
                lancar_nota_portal(aluno)
                aluno["status_lancamento"] = "LANÇADO"
            except (RetryError, ConnectionError) as erro:
                aluno["status_lancamento"] = "FALHOU"
                logger.error(
                    "Lançamento de %s falhou após 3 tentativas: %s", aluno["nome"], erro
                )

            with trava:
                resultados.append(aluno)
        except Exception as erro:
            logger.exception("Erro inesperado ao processar o aluno %s: %s", linha, erro)
        finally:
            fila.task_done()


def exibir_relatorio(resultados):
    """Imprime o resumo final do processamento."""
    print("\n" + "=" * 86)
    print(f"{'NOME':<28}{'RA':<10}{'BIM 1':>7}{'BIM 2':>7}{'FINAL':>8}  {'SITUAÇÃO':<11}LANÇAMENTO")
    print("-" * 86)
    for aluno in resultados:
        print(
            f"{aluno['nome']:<28}{aluno['ra']:<10}"
            f"{aluno['media_bim1']:>7.2f}{aluno['media_bim2']:>7.2f}"
            f"{aluno['media_final']:>8.2f}  {aluno['situacao']:<11}"
            f"{aluno['status_lancamento']}"
        )
    print("=" * 86)

    aprovados = sum(1 for a in resultados if a["situacao"] == "APROVADO")
    falhas = sum(1 for a in resultados if a["status_lancamento"] == "FALHOU")
    print(f"Total: {len(resultados)} | Aprovados: {aprovados} | "
          f"Reprovados: {len(resultados) - aprovados} | Falhas de lançamento: {falhas}")


def main():
    logger.info("=== Bot de Lançamento de Notas (Fila + Retry) iniciado ===")

    if not CAMINHO_CSV.exists():
        logger.error("Arquivo CSV não encontrado: %s", CAMINHO_CSV)
        return

    fila = queue.Queue()
    resultados = []
    trava = threading.Lock()

    workers = [
        threading.Thread(
            target=consumidor, args=(fila, resultados, trava), name=f"Worker-{i}"
        )
        for i in range(1, QTD_WORKERS + 1)
    ]
    for worker in workers:
        worker.start()

    produtor(fila)

    for _ in workers:
        fila.put(None)

    fila.join()
    for worker in workers:
        worker.join()

    resultados.sort(key=lambda a: int(a["ra"]) if a["ra"].isdigit() else float("inf"))
    exibir_relatorio(resultados)
    logger.info("=== Processamento finalizado: %d aluno(s) ===", len(resultados))


if __name__ == "__main__":
    main()
