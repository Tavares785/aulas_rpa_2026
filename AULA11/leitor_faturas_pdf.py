"""
Script de Leitura e Extração de Faturas em PDF com Expressões Regulares e Exportação para Excel.
Laboratório 11 - RPA
"""

from pathlib import Path
import re
import openpyxl  # noqa: F401
import pandas as pd
import pdfplumber

DIRETORIO_ATUAL = Path(__file__).resolve().parent
PASTA_FATURAS = DIRETORIO_ATUAL / "faturas"
ARQUIVO_SAIDA = DIRETORIO_ATUAL / "relatorio_faturas.xlsx"

# Expressões Regulares
# NIF (9 dígitos numéricos) ou CNPJ (XX.XXX.XXX/XXXX-XX)
RE_NIF_CNPJ = re.compile(
    r"(?:(?:CNPJ|NIF)[:\s]*)?(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\b\d{9}\b)",
    re.IGNORECASE,
)

# Valor Total (ex: R$ 1.500,00 ou Total: 1500.00)
RE_VALOR_TOTAL = re.compile(
    r"(?:VALOR\s+TOTAL|Total(?:\s+a\s+pagar)?):\s*(R\$\s*[\d.,]+|[\d.,]+)",
    re.IGNORECASE,
)


def extrair_texto_pdf(caminho_pdf: Path) -> str:
    """
    Abre o PDF com pdfplumber e extrai o texto de cada página simulando a leitura.
    """
    texto_paginas = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_paginas.append(texto)
    return "\n".join(texto_paginas)


def extrair_dados_fatura(texto: str, nome_arquivo: str) -> dict:
    """
    Aplica regras de Expressões Regulares (re.search) para isolar:
    - NIF/CNPJ: 9 dígitos numéricos ou XX.XXX.XXX/XXXX-XX
    - Valor Total: Padrão numérico monetário
    """
    match_doc = re.search(RE_NIF_CNPJ, texto)
    match_total = re.search(RE_VALOR_TOTAL, texto)

    nif_cnpj = match_doc.group(1).strip() if match_doc else "Não informado"
    valor_total = match_total.group(1).strip() if match_total else "Não informado"

    return {
        "arquivo": nome_arquivo,
        "nif_cnpj": nif_cnpj,
        "valor_total": valor_total,
    }


def processar_faturas(pasta_faturas: Path = PASTA_FATURAS, arquivo_saida: Path = ARQUIVO_SAIDA) -> pd.DataFrame:
    """
    Processa todos os PDFs na pasta de faturas, extrai os dados estruturados
    em lista de dicionários, converte para DataFrame e salva em relatório Excel (.xlsx).
    """
    faturas: list[dict] = []

    if not pasta_faturas.exists():
        raise FileNotFoundError(f"Pasta de faturas não encontrada: {pasta_faturas}")

    arquivos_pdf = sorted(pasta_faturas.glob("*.pdf"))
    if not arquivos_pdf:
        print(f"Nenhum arquivo PDF encontrado em {pasta_faturas}")

    for caminho in arquivos_pdf:
        texto = extrair_texto_pdf(caminho)
        dados = extrair_dados_fatura(texto, caminho.name)
        faturas.append(dados)
        print(f"Processado '{caminho.name}': NIF/CNPJ={dados['nif_cnpj']}, Total={dados['valor_total']}")

    df = pd.DataFrame(faturas)
    df.to_excel(arquivo_saida, index=False, engine="openpyxl")
    print(f"\n[SUCESSO] Relatório de faturas exportado para: {arquivo_saida}")
    return df


if __name__ == "__main__":
    processar_faturas()
