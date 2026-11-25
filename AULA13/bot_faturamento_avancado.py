"""
AULA 13 - Arquitetura Orientada a Filas (Queue), Processamento Assincrono e Resiliencia
Bot de Faturamento e Lancamento de Notas com Queue, Logging Rotativo e Tenacity

Aluno: Kaua David Dantas Mendonca
RA: 6326260
"""

import csv
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import queue
import random
from typing import Any
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

NOME_ARQUIVO_LOG = "app_rpa.log"

# Configuracao de log corporativo com RotatingFileHandler (limite de 1MB por arquivo)
logger = logging.getLogger("RPA_AULA13")
logger.setLevel(logging.INFO)

# Evita duplicacao de handlers caso re-executado
if not logger.handlers:
    rotacao_handler = RotatingFileHandler(
        NOME_ARQUIVO_LOG,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    formatador = logging.Formatter(
        "%(asctime)s [%(levelname)s] [Thread/Queue] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    rotacao_handler.setFormatter(formatador)
    logger.addHandler(rotacao_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatador)
    logger.addHandler(console_handler)


def limpar_valor_nota(valor_bruto: Any) -> float:
    """Limpa e converte campos de notas e TFs tratando dados sujos (virgulas, faltas, nulos)."""
    if valor_bruto is None:
        return 0.0

    texto = str(valor_bruto).strip().replace(",", ".")
    if not texto:
        return 0.0

    # Palavras-chave que indicam ausencia ou invalidade
    if texto.upper() in {"FALTOU", "FALTA", "N/A", "NONE", "NULL", "-"}:
        return 0.0

    try:
        return float(texto)
    except ValueError:
        return 0.0


def localizar_arquivo_csv() -> Path:
    """Localiza o arquivo notas_alunos.csv nas pastas do projeto."""
    locais = [
        Path("AULA07/notas_alunos.csv"),
        Path("../AULA07/notas_alunos.csv"),
        Path(__file__).resolve().parent.parent / "AULA07" / "notas_alunos.csv"
    ]
    for caminho in locais:
        if caminho.exists():
            return caminho
    return Path("AULA07/notas_alunos.csv")


def produtor(fila: queue.Queue, caminho_csv: Path, limite: int = 10) -> int:
    """Le o CSV da AULA07 e enfileira os primeiros alunos para processamento."""
    logger.info(f"[PRODUTOR] Iniciando leitura do arquivo: {caminho_csv}")

    if not caminho_csv.exists():
        logger.warning(f"[PRODUTOR] Arquivo {caminho_csv} nao encontrado. Gerando dados de contingencia.")
        registros_simulados = [
            {"Nome": f"Aluno Teste {i}", "RA": f"10000{i}", "Nota01": "7,5", "TF01": "1,5", "Nota02": "8,0", "TF02": "1,8"}
            for i in range(1, limite + 1)
        ]
        for reg in registros_simulados:
            fila.put(reg)
            logger.info(f"[PRODUTOR] Aluno enfileirado: {reg['Nome']} (RA: {reg['RA']})")
        return len(registros_simulados)

    total_enfileirados = 0
    with open(caminho_csv, mode="r", encoding="utf-8-sig") as arq:
        leitor = csv.DictReader(arq, delimiter=";")
        for linha in leitor:
            if total_enfileirados >= limite:
                break
            fila.put(linha)
            nome_aluno = " ".join(linha.get("Nome", "").split()).title()
            ra_aluno = linha.get("RA", "").strip()
            logger.info(f"[PRODUTOR] Aluno #{total_enfileirados + 1} enfileirado: {nome_aluno} (RA: {ra_aluno})")
            total_enfileirados += 1

    logger.info(f"[PRODUTOR] Carga finalizada com sucesso. Total na fila: {total_enfileirados}")
    return total_enfileirados


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.05, min=0.05, max=0.5),
    retry=retry_if_exception_type(ConnectionError),
    reraise=True
)
def lancar_nota_portal(aluno: dict[str, Any]) -> bool:
    """Simula o lancamento das notas no portal academico com mecanismo de Retry resiliente."""
    # Simula instabilidade de rede transiente (30% de chance de falha transiente)
    if random.random() < 0.30:
        logger.warning(
            f"[RETRY-TRIGGER] Falha temporaria de conexao com o portal para o aluno: {aluno['nome']} (tentando novamente...)"
        )
        raise ConnectionError("Timeout de conexao com o portal de notas.")

    logger.info(
        f"[PORTAL-OK] Nota lancada com sucesso no portal! Aluno: {aluno['nome']} "
        f"| Media: {aluno['media_final']} | Situacao: {aluno['situacao']}"
    )
    return True


def consumidor(fila: queue.Queue) -> list[dict[str, Any]]:
    """Consome alunos da fila, limpa dados, calcula medias e lanca no portal com retry."""
    logger.info("[CONSUMIDOR] Worker iniciado. Aguardando itens da fila...")
    resultados: list[dict[str, Any]] = []

    while not fila.empty():
        item = fila.get()

        nome = " ".join(item.get("Nome", "").split()).title()
        ra = item.get("RA", "").strip()

        nota01 = limpar_valor_nota(item.get("Nota01"))
        tf01 = limpar_valor_nota(item.get("TF01"))
        nota02 = limpar_valor_nota(item.get("Nota02") or item.get("Notao2"))
        tf02 = limpar_valor_nota(item.get("TF02"))

        # Regra de negocio: Nota peso 8 + TF peso 2 por bimestre. Media final = media dos 2 bimestres.
        bimestre_1 = (nota01 * 0.8) + tf01
        bimestre_2 = (nota02 * 0.8) + tf02
        media_final = round((bimestre_1 + bimestre_2) / 2.0, 2)
        situacao = "APROVADO" if media_final >= 6.0 else "REPROVADO"

        aluno_processado = {
            "nome": nome,
            "ra": ra,
            "b1": round(bimestre_1, 2),
            "b2": round(bimestre_2, 2),
            "media_final": media_final,
            "situacao": situacao
        }

        # Executa lancamento no portal com tratamento de retry resiliente
        try:
            lancar_nota_portal(aluno_processado)
        except Exception as erro:
            logger.error(
                f"[FALHA-CRITICA] Aluno {nome} (RA: {ra}) excedeu o limite de 3 tentativas: {erro}"
            )

        resultados.append(aluno_processado)
        fila.task_done()

    logger.info(f"[CONSUMIDOR] Todos os {len(resultados)} alunos foram processados pela fila.")
    return resultados


def main() -> None:
    """Orquestra o pipeline Produtor-Consumidor orientado a filas."""
    logger.info("=" * 60)
    logger.info("INICIANDO BOT DE FATURAMENTO / NOTAS AVANCADO (LAB 13)")
    logger.info("=" * 60)

    # Inicializa a fila sincronizada
    fila_alunos: queue.Queue = queue.Queue()
    caminho_csv = localizar_arquivo_csv()

    # 1. Fase Produtor: Adiciona os 10 primeiros alunos
    total_produzido = produtor(fila_alunos, caminho_csv, limite=10)

    # 2. Fase Consumidor: Processa itens da fila e lanca no portal
    resultados = consumidor(fila_alunos)

    # Exibicao de sumario no terminal
    print("\n" + "=" * 65)
    print(f"{'RELATORIO FINAL DE PROCESSAMENTO DA FILA':^65}")
    print("=" * 65)
    print(f"{'NOME':<25} | {'RA':<10} | {'B1':<5} | {'B2':<5} | {'MEDIA':<5} | {'STATUS'}")
    print("-" * 65)

    for r in resultados:
        print(
            f"{r['nome']:<25} | {r['ra']:<10} | {r['b1']:<5.2f} | "
            f"{r['b2']:<5.2f} | {r['media_final']:<5.2f} | {r['situacao']}"
        )

    print("=" * 65)
    print(f"Total de registros processados: {len(resultados)} / {total_produzido}")
    print(f"Arquivo de log gravado em: {Path(NOME_ARQUIVO_LOG).resolve()}\n")


if __name__ == "__main__":
    main()
