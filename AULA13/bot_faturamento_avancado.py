"""
Lab 13 - Filas, Retry e Logs rotativos
RA: 6326012

Reaproveita o CSV do Lab 07: o produtor coloca os 10 primeiros alunos
numa fila, o consumidor limpa os dados, calcula a media e lanca a nota
no "portal" (simulado, com falha aleatoria de rede e retry com tenacity).
"""
import csv
import logging
import queue
import random
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path

from tenacity import RetryError, retry, stop_after_attempt, wait_fixed

ARQUIVO_CSV = Path(__file__).parent.parent / "AULA07" / "notas_alunos.csv"
QTD_ALUNOS = 10

handler = RotatingFileHandler("app_rpa.log", maxBytes=1024 * 1024, backupCount=3, encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger = logging.getLogger("bot_notas")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())


def limpar_numero(valor, maximo):
    # "FALTOU", "N/A", vazio ou texto invalido contam como 0
    valor = (valor or "").strip().replace(",", ".")
    try:
        numero = float(valor)
    except ValueError:
        return 0.0
    return min(max(numero, 0.0), maximo)


def limpar_ra(valor):
    digitos = re.sub(r"\D", "", valor or "")
    return digitos.lstrip("0") or "nao informado"


def limpar_nome(valor):
    return " ".join((valor or "").split()).title()


def produtor(fila):
    with open(ARQUIVO_CSV, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        for i, linha in enumerate(leitor):
            if i >= QTD_ALUNOS:
                break
            fila.put(linha)
            logger.info("Produtor: aluno %s adicionado na fila", limpar_nome(linha["Nome"]))


def calcular_resultado(linha):
    # nota vale ate 8 pontos (peso 8) e o TF ate 2 pontos (peso 2)
    bim1 = limpar_numero(linha["Nota01"], 10) * 0.8 + limpar_numero(linha["TF01"], 2)
    bim2 = limpar_numero(linha["Nota02"], 10) * 0.8 + limpar_numero(linha["TF02"], 2)
    media = round((bim1 + bim2) / 2, 2)
    situacao = "APROVADO" if media >= 6 else "REPROVADO"
    return media, situacao


@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5))
def lancar_nota_portal(aluno):
    # simula instabilidade de rede: 30% de chance de falhar
    if random.random() < 0.3:
        logger.warning("Falha de rede ao lancar a nota de %s, tentando de novo...", aluno["nome"])
        raise ConnectionError("portal indisponivel")
    logger.info("Nota lancada no portal: %s | RA %s | media %.2f | %s",
                aluno["nome"], aluno["ra"], aluno["media"], aluno["situacao"])


def consumidor(fila):
    lancados = 0
    while not fila.empty():
        linha = fila.get()
        media, situacao = calcular_resultado(linha)
        aluno = {
            "nome": limpar_nome(linha["Nome"]),
            "ra": limpar_ra(linha["RA"]),
            "media": media,
            "situacao": situacao,
        }
        try:
            lancar_nota_portal(aluno)
            lancados += 1
        except RetryError:
            logger.error("Nao foi possivel lancar a nota de %s apos 3 tentativas", aluno["nome"])
        fila.task_done()
    return lancados


def main():
    logger.info("Inicio do processamento")
    fila = queue.Queue()
    produtor(fila)
    lancados = consumidor(fila)
    logger.info("Fim do processamento: %d de %d notas lancadas", lancados, QTD_ALUNOS)


if __name__ == "__main__":
    main()
