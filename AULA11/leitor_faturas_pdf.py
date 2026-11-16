"""
AULA 11 - Extracao de Dados em PDFs, Filtros Regex e Exportacao para Excel

O robo le todas as faturas em PDF da pasta 'faturas', extrai o texto de cada
pagina com pdfplumber, aplica Expressoes Regulares (re.search) para isolar o
NIF/CNPJ do fornecedor e o Valor Total, guarda cada fatura em uma lista de
dicionarios e exporta tudo para 'relatorio_faturas.xlsx' com pandas.

Requer: pip install pdfplumber pandas openpyxl
"""
import re
from pathlib import Path

import pandas as pd
import pdfplumber


PASTA_FATURAS = Path(__file__).resolve().parent / "faturas"
ARQUIVO_SAIDA = Path(__file__).resolve().parent / "relatorio_faturas.xlsx"

# Padroes de Regex -----------------------------------------------------------
# NIF/CNPJ: formato CNPJ XX.XXX.XXX/XXXX-XX ou NIF com 9 digitos numericos.
RE_NIF_CNPJ = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b|\b\d{9}\b")
# Valor Total: linha com a palavra 'total' seguida de ':' e um valor monetario,
# com ou sem 'R$' (ex: 'R$ 1.500,00', 'Total: 1500.00', 'VALOR TOTAL: R$ 3.640,90').
RE_VALOR_TOTAL = re.compile(
    r"total[^:\n]*:\s*(?:R\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+(?:[.,]\d{2})?)",
    re.IGNORECASE,
)
# Data de emissao no formato dd/mm/aaaa (rotulo 'Emissao:' ou 'Data:').
RE_DATA = re.compile(r"(?:Emissao|Data):\s*(\d{2}/\d{2}/\d{4})", re.IGNORECASE)
# Fornecedor: tudo ate o fim da linha apos o rotulo.
RE_FORNECEDOR = re.compile(r"(?:Fornecedor|Razao Social):\s*(.+)", re.IGNORECASE)


def extrair_texto_pdf(caminho: Path) -> str:
    """Extrai o texto de todas as paginas de um PDF."""
    with pdfplumber.open(caminho) as pdf:
        return "\n".join((pagina.extract_text() or "") for pagina in pdf.pages)


def buscar(padrao: re.Pattern, texto: str):
    """Aplica re.search; retorna o grupo capturado (ou o match) ou None."""
    achado = re.search(padrao, texto)
    if achado is None:
        return None
    return achado.group(1) if padrao.groups else achado.group(0)


def converter_valor(valor_texto):
    """Converte '1.500,00' ou '1200.50' para float (None se ausente)."""
    if valor_texto is None:
        return None
    if "," in valor_texto:
        valor_texto = valor_texto.replace(".", "").replace(",", ".")
    return float(valor_texto)


def extrair_fatura(texto: str, arquivo: str) -> dict:
    """Aplica as regex no texto de uma fatura e monta o dicionario."""
    nif_cnpj = buscar(RE_NIF_CNPJ, texto)
    valor_total = converter_valor(buscar(RE_VALOR_TOTAL, texto))
    status = "OK" if nif_cnpj and valor_total is not None else "PENDENTE"
    return {
        "arquivo": arquivo,
        "fornecedor": buscar(RE_FORNECEDOR, texto),
        "data_emissao": buscar(RE_DATA, texto),
        "nif_cnpj": nif_cnpj,
        "valor_total": valor_total,
        "status": status,
    }


def processar_faturas(pasta: Path) -> list:
    """Le cada PDF da pasta e retorna uma lista de dicionarios."""
    faturas = []
    for caminho in sorted(pasta.glob("*.pdf")):
        texto = extrair_texto_pdf(caminho)
        faturas.append(extrair_fatura(texto, caminho.name))
    return faturas


def exportar_excel(faturas: list, caminho: Path) -> pd.DataFrame:
    """Converte a lista em DataFrame e salva em Excel."""
    df = pd.DataFrame(faturas)
    df.to_excel(caminho, index=False, sheet_name="Faturas")
    return df


if __name__ == "__main__":
    if not PASTA_FATURAS.is_dir():
        raise SystemExit(f"Pasta nao encontrada: {PASTA_FATURAS}")

    faturas = processar_faturas(PASTA_FATURAS)
    df = exportar_excel(faturas, ARQUIVO_SAIDA)

    print(df.to_string(index=False))
    print(f"\n'{ARQUIVO_SAIDA.name}' gerado com {len(df)} faturas.")
