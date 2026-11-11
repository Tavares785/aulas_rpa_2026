"""
AULA 11 - Extracao de Texto, Regex e Excel
Exemplo do PROFESSOR

Cenario (diferente do trabalho de casa): o Departamento Pessoal recebe o
espelho de ponto de cada colaborador em PDF. O robo le todos os PDFs da pasta
'espelhos', usa regex para isolar PIS, e-mail corporativo, competencia e horas
trabalhadas, e consolida tudo em 'espelho_ponto.xlsx'. Espelhos sem PIS vao
para a aba 'Pendencias' (excecao de negocio, revisao humana).

Entrada: lab-professor/AULA11/espelhos/espelho_*.pdf (ou .txt como fallback).
Para regerar os PDFs: python lab-professor/AULA11/gerar_faturas_pdf.py
Requer: pip install pdfplumber pandas openpyxl
"""
import re
from pathlib import Path
import pandas as pd
import pdfplumber


PASTA_ESPELHOS = Path(__file__).resolve().parent / "espelhos"
ARQUIVO_SAIDA = Path(__file__).resolve().parent / "espelho_ponto.xlsx"

# Padroes de Regex (explique cada grupo no quadro) ---------------------------
# PIS: 3 digitos . 5 digitos . 2 digitos - 1 digito verificador.
RE_PIS = re.compile(r"\d{3}\.\d{5}\.\d{2}-\d")
# E-mail corporativo: o rotulo 'E-mail:' evita pegar e-mails de outras linhas.
RE_EMAIL = re.compile(r"E-mail:\s*([\w.+-]+@[\w-]+\.[\w.-]+)")
# Colaborador: tudo ate o fim da linha apos o rotulo.
RE_NOME = re.compile(r"Colaborador:\s*(.+)")
# Competencia mm/aaaa.
RE_COMPETENCIA = re.compile(r"Competencia:\s*(\d{2}/\d{4})")
# Horas trabalhadas: ate 3 digitos de hora + 'h' + 2 digitos de minuto.
RE_HORAS = re.compile(r"Horas trabalhadas:\s*(\d{1,3}h\d{2})")


def ler_texto(caminho: Path) -> str:
    """Extrai o texto de um PDF (pdfplumber) ou le o .txt equivalente."""
    if caminho.suffix.lower() == ".pdf" and pdfplumber is not None:
        with pdfplumber.open(caminho) as pdf:
            return "\n".join((pagina.extract_text() or "") for pagina in pdf.pages)
    return caminho.read_text(encoding="utf-8")


def buscar(padrao: re.Pattern, texto: str):
    """Retorna o grupo capturado (ou o match inteiro) ou None se nao achar."""
    achado = padrao.search(texto)
    if achado is None:
        return None
    return achado.group(1) if padrao.groups else achado.group(0)


def extrair_espelho(texto: str, arquivo: str) -> dict:
    """Aplica as regex no texto de um espelho; campo ausente fica None."""
    return {
        "arquivo": arquivo,
        "colaborador": buscar(RE_NOME, texto),
        "pis": buscar(RE_PIS, texto),
        "email": buscar(RE_EMAIL, texto),
        "competencia": buscar(RE_COMPETENCIA, texto),
        "horas_trabalhadas": buscar(RE_HORAS, texto),
    }


def listar_arquivos(pasta: Path) -> list:
    """Prefere o PDF; usa o .txt apenas quando nao existe o PDF."""
    escolhidos = {}
    for caminho in sorted(pasta.glob("espelho_*")):
        if caminho.suffix.lower() in (".pdf", ".txt"):
            atual = escolhidos.get(caminho.stem)
            if atual is None or caminho.suffix.lower() == ".pdf":
                escolhidos[caminho.stem] = caminho
    return list(escolhidos.values())


def processar_pasta(pasta: Path) -> tuple:
    """Separa registros completos das pendencias."""
    validos, pendencias = [], []
    for caminho in listar_arquivos(pasta):
        registro = extrair_espelho(ler_texto(caminho), caminho.name)
        if registro["pis"] is None:
            pendencias.append({"arquivo": caminho.name, "motivo": "PIS ausente"})
        else:
            validos.append(registro)
    return validos, pendencias


def exportar_para_excel(validos: list, pendencias: list, caminho: Path) -> int:
    """Gera o Excel com as abas 'Espelhos' e 'Pendencias'."""
    print(pd.DataFrame(validos))
    print(pd.DataFrame(pendencias))
    # with pd.ExcelWriter(caminho) as escritor:
    #     pd.DataFrame(validos).to_excel(escritor, sheet_name="Espelhos", index=False)
    #     pd.DataFrame(pendencias).to_excel(escritor, sheet_name="Pendencias", index=False)
    # return len(validos)


if __name__ == "__main__":
    if not PASTA_ESPELHOS.is_dir():
        raise SystemExit(f"Pasta nao encontrada: {PASTA_ESPELHOS}")

    validos, pendencias = processar_pasta(PASTA_ESPELHOS)

    print("Espelhos de ponto extraidos:")
    for registro in validos:
        print(registro)
    print(f"\nPendencias para revisao humana: {len(pendencias)}")
    for p in pendencias:
        print(f"  - {p['arquivo']}: {p['motivo']}")

    # DICA DE AULA: sem Pandas, encerramos de forma graciosa com codigo 0.
    if pd is None:
        raise SystemExit(0)

    total = exportar_para_excel(validos, pendencias, ARQUIVO_SAIDA)
    print(f"\n'{ARQUIVO_SAIDA.name}' gerado com {total} linhas.")
