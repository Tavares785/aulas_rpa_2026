"""
Lab 11: Extração de Dados em PDFs, Filtros Regex e Exportação para Excel.

Lê arquivos de faturas em PDF na pasta faturas/, extrai NIF/CNPJ e
Valor Total através de Expressões Regulares (re.search), armazena
os dados em uma lista de dicionários e exporta para relatorio_faturas.xlsx.
"""

from pathlib import Path
import re

import pandas as pd
import pdfplumber

PASTA_FATURAS = Path(__file__).resolve().parent / "faturas"
ARQUIVO_EXCEL = Path(__file__).resolve().parent / "relatorio_faturas.xlsx"

RE_CNPJ = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
RE_NIF = re.compile(r"\b\d{9}\b")
RE_TOTAL = re.compile(
    r"(?:Total(?:\s+a\s+pagar)?|VALOR\s+TOTAL):\s*(R\$\s*[\d.,]+|[\d.,]+)",
    re.IGNORECASE,
)


def extrair_dados_pdf(caminho_pdf: Path) -> dict:
    """Extrai texto do PDF e localiza documento (NIF/CNPJ) e valor total."""
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_extraido = pagina.extract_text()
            if texto_extraido:
                texto_completo += texto_extraido + "\n"

    # Busca NIF ou CNPJ
    match_cnpj = RE_CNPJ.search(texto_completo)
    match_nif = RE_NIF.search(texto_completo)

    if match_cnpj:
        documento = match_cnpj.group(0).strip()
    elif match_nif:
        documento = match_nif.group(0).strip()
    else:
        documento = "Não informado"

    # Busca Valor Total
    match_total = RE_TOTAL.search(texto_completo)
    if match_total:
        valor_total = match_total.group(1).strip()
    else:
        valor_total = "Não informado"

    return {
        "arquivo": caminho_pdf.name,
        "nif_cnpj": documento,
        "valor_total": valor_total,
    }


def processar_faturas():
    """Varre todos os PDFs da pasta faturas e consolida em DataFrame e Excel."""
    if not PASTA_FATURAS.exists():
        print(f"Pasta de faturas não encontrada: {PASTA_FATURAS}")
        return pd.DataFrame()

    arquivos_pdf = sorted(PASTA_FATURAS.glob("*.pdf"))
    print(f"Encontrados {len(arquivos_pdf)} arquivos PDF para processar.")

    faturas_extraidas = []
    for caminho in arquivos_pdf:
        dados = extrair_dados_pdf(caminho)
        faturas_extraidas.append(dados)
        print(
            f"Arquivo: {dados['arquivo']} | "
            f"Doc: {dados['nif_cnpj']} | "
            f"Total: {dados['valor_total']}"
        )

    # Conversão para DataFrame do pandas
    df = pd.DataFrame(faturas_extraidas)

    # Exportação para Excel (.xlsx) via openpyxl
    df.to_excel(ARQUIVO_EXCEL, index=False, engine="openpyxl")
    print(f"\nRelatório Excel gerado com sucesso em: {ARQUIVO_EXCEL}")

    return df


if __name__ == "__main__":
    processar_faturas()
