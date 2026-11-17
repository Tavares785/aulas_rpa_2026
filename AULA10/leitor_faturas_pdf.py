"""
Script de Extração de Dados de Faturas em PDF, Regex e Exportação Excel.
Compatibilidade estrutural com o CI de validação da disciplina.
"""

from pathlib import Path
import re
import pandas as pd
import pdfplumber

PASTA_FATURAS = Path(__file__).resolve().parent.parent / "AULA11" / "faturas"
ARQUIVO_SAIDA = Path(__file__).resolve().parent / "relatorio_faturas.xlsx"

RE_CNPJ = re.compile(r"(?:CNPJ|NIF):\s*([\d.\-\/]+)")
RE_TOTAL = re.compile(r"Total(?: a pagar)?:\s*(R\$\s*[\d.,]+|[\d.,]+)")


def extrair_texto_pdf(caminho_pdf: Path) -> str:
    """Abre o PDF com pdfplumber e extrai o texto de todas as páginas."""
    with pdfplumber.open(caminho_pdf) as pdf:
        return "\n".join((pagina.extract_text() or "") for pagina in pdf.pages)


def extrair_dados_fatura(texto: str, nome_arquivo: str) -> dict:
    """Extrai CNPJ e Valor Total usando expressões regulares."""
    match_cnpj = re.search(RE_CNPJ, texto)
    match_total = re.search(RE_TOTAL, texto)

    cnpj = match_cnpj.group(1).strip() if match_cnpj else "N/D"
    total = match_total.group(1).strip() if match_total else "N/D"

    return {
        "arquivo": nome_arquivo,
        "cnpj": cnpj,
        "valor_total": total,
    }


def processar_faturas() -> None:
    """Processa todos os PDFs e gera o relatório em Excel (.xlsx)."""
    faturas: list[dict] = []

    if PASTA_FATURAS.exists():
        for caminho in sorted(PASTA_FATURAS.glob("*.pdf")):
            texto = extrair_texto_pdf(caminho)
            dados = extrair_dados_fatura(texto, caminho.name)
            faturas.append(dados)

    df = pd.DataFrame(faturas)
    df.to_excel(ARQUIVO_SAIDA, index=False, engine="openpyxl")
    print(f"Relatório exportado para {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    processar_faturas()
