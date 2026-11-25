"""
Módulo de Arquitetura Orientada a Filas, Processamento e Resiliência.

Lab 13:
- Padrão Produtor-Consumidor utilizando queue.Queue.
- Registro corporativo de auditoria com RotatingFileHandler em app_rpa.log.
- Tratamento resiliente de falhas transientes com Retry Pattern via biblioteca tenacity.
- Limpeza e cálculo de médias dos alunos da AULA07.
"""

from __future__ import annotations

import csv
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import queue
import random

from tenacity import retry, stop_after_attempt, wait_fixed

# Configuração do Logger Corporativo com RotatingFileHandler (limite de 1MB por arquivo)
LOG_FILE = "app_rpa.log"
logger = logging.getLogger("RPA_Faturamento_Avancado")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def encontrar_caminho_csv() -> Path:
    """Localiza o arquivo CSV de notas da AULA07 independentemente do diretório de execução."""
    caminho_local = Path("AULA07/notas_alunos.csv")
    if caminho_local.exists():
        return caminho_local
    caminho_relativo = Path(__file__).resolve().parent.parent / "AULA07" / "notas_alunos.csv"
    return caminho_relativo


def converter_nota(valor: str) -> float:
    """Limpa e converte valores numéricos de nota. Valores inválidos contam como 0.0."""
    if not valor:
        return 0.0
    texto = valor.strip().replace(",", ".")
    try:
        nota = float(texto)
        return max(0.0, min(10.0, nota))
    except ValueError:
        return 0.0


@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.1), reraise=True)
def lancar_nota_portal(aluno: dict) -> bool:
    """Simula o envio da nota ao portal acadêmico com retry automático em caso de falha de rede."""
    # Simula instabilidade de rede (chance de falha transiente)
    if random.random() < 0.2:
        logger.warning(
            f"Instabilidade de rede ao lançar nota de '{aluno['nome']}'. Tentando novamente..."
        )
        raise ConnectionError("Timeout temporário de conexão com o portal acadêmico.")

    logger.info(
        f"[PORTAL OK] Nota lançada para '{aluno['nome']}' | "
        f"Média Final: {aluno['media_final']:.2f} | Situação: {aluno['situacao']}"
    )
    return True


def produtor(fila: queue.Queue, caminho_csv: Path, limite: int = 10) -> None:
    """Lê o arquivo CSV da AULA07 e enfileira os primeiros 'limite' registros de alunos."""
    logger.info(f"[PRODUTOR] Iniciando leitura do arquivo: {caminho_csv}")
    if not caminho_csv.exists():
        logger.error(f"[PRODUTOR] Arquivo de dados não encontrado: {caminho_csv}")
        return

    with open(caminho_csv, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f, delimiter=";")
        contador = 0
        for linha in leitor:
            if contador >= limite:
                break
            aluno = {
                "nome": linha.get("Nome", "").strip(),
                "ra": linha.get("RA", "").strip(),
                "nota01": linha.get("Nota01", ""),
                "tf01": linha.get("TF01", ""),
                "nota02": linha.get("Nota02", ""),
                "tf02": linha.get("TF02", "")
            }
            fila.put(aluno)
            logger.info(f"[PRODUTOR] Aluno '{aluno['nome']}' (RA: {aluno['ra']}) adicionado à fila.")
            contador += 1

    logger.info(f"[PRODUTOR] Carga concluída. Total de alunos enfileirados: {contador}")


def consumidor(fila: queue.Queue) -> None:
    """Worker que retira alunos da fila, processa médias, define situação e lança no portal."""
    logger.info("[CONSUMIDOR] Worker iniciado. Processando itens da fila...")
    while not fila.empty():
        aluno = fila.get()
        try:
            n1 = converter_nota(aluno["nota01"])
            tf1 = converter_nota(aluno["tf01"])
            n2 = converter_nota(aluno["nota02"])
            tf2 = converter_nota(aluno["tf02"])

            # Cálculo de média ponderada por bimestre: nota peso 8 + TF peso 2
            b1 = (n1 * 0.8) + (tf1 * 0.2)
            b2 = (n2 * 0.8) + (tf2 * 0.2)
            media_final = (b1 + b2) / 2.0
            situacao = "APROVADO" if media_final >= 6.0 else "REPROVADO"

            aluno_processado = {
                "nome": aluno["nome"],
                "ra": aluno["ra"],
                "b1": round(b1, 2),
                "b2": round(b2, 2),
                "media_final": round(media_final, 2),
                "situacao": situacao
            }

            try:
                lancar_nota_portal(aluno_processado)
            except Exception as erro:
                logger.error(
                    f"[CONSUMIDOR] Falha definitiva após 3 tentativas para '{aluno['nome']}': {erro}"
                )
        finally:
            fila.task_done()

    logger.info("[CONSUMIDOR] Todos os alunos da fila foram processados.")


def main() -> None:
    """Ponto de entrada do script: inicializa a fila, produtor e consumidor."""
    random.seed(42)  # Garante previsibilidade nos testes
    logger.info("=== INÍCIO DA EXECUÇÃO DO BOT DE FATURAMENTO / NOTAS AVANÇADO ===")

    caminho_csv = encontrar_caminho_csv()
    fila_alunos: queue.Queue = queue.Queue()

    produtor(fila_alunos, caminho_csv=caminho_csv, limite=10)
    consumidor(fila_alunos)
    fila_alunos.join()

    logger.info("=== EXECUÇÃO FINALIZADA COM SUCESSO ===")
    print("Processamento finalizado com sucesso! Consulte 'app_rpa.log' para auditoria.")


if __name__ == "__main__":
    main()

