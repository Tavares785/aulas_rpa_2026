"""
Lab 07 - Lançamento de Notas com RPA.

Lê o CSV de notas, calcula a média e simula o lançamento.
RA: 6326138
"""

import csv
import time

import pyautogui

# Configurações de segurança do pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

CSV_PATH = "AULA07/notas_alunos.csv"
NOTA_COLS = ["Nota01", "Nota02"]


def parse_nota(valor):
    """Converte string de nota para float, retorna 0 se inválido."""
    if valor is None:
        return 0.0
    v = valor.strip().replace(",", ".")
    try:
        resultado = float(v)
        return resultado
    except ValueError:
        return 0.0


def ler_alunos(caminho_csv):
    """Lê o CSV e retorna lista de dicts com matricula e nota."""
    lista = []
    with open(caminho_csv, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            ra = row.get("RA", "").strip()
            notas = [parse_nota(row.get(col, "")) for col in NOTA_COLS]
            nota_final = sum(notas) / len(notas) if notas else 0.0
            lista.append({
                "matricula": ra,
                "nota": round(nota_final, 2),
            })
    return lista


alunos = ler_alunos(CSV_PATH)


def lancar_notas(lista_alunos):
    """Simula o lançamento de notas (apenas log, sem ação real)."""
    print("=" * 50)
    print("SIMULAÇÃO DE LANÇAMENTO DE NOTAS")
    print("=" * 50)
    for aluno in lista_alunos:
        matricula = aluno["matricula"]
        nota = aluno["nota"]
        status = "APROVADO" if nota >= 5 else "REPROVADO"
        print(
            f"Matrícula: {matricula:<12} "
            f"Nota: {nota:>5.2f}  "
            f"Status: {status}"
        )
        time.sleep(0)  # placeholder para simulação
    print("=" * 50)
    print(f"Total de alunos processados: {len(lista_alunos)}")
    print("Lançamento simulado com sucesso.")


if __name__ == "__main__":
    lancar_notas(alunos)
