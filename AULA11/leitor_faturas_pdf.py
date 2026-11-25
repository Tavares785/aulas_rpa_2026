"""
Lab 11 - Extracao de Dados em PDFs, Filtros Regex e Exportacao para Excel

Robo que le as faturas em PDF da pasta faturas/, extrai com expressoes
regulares o NIF/CNPJ do fornecedor e o valor total, e salva a tabela
consolidada em relatorio_faturas.xlsx.

Requer: pip install pdfplumber pandas openpyxl
"""
import re
from pathlib import Path

import pandas as pd
import pdfplumber

PASTA_BASE = Path(__file__).parent
PASTA_FATURAS = PASTA_BASE / "faturas"
ARQUIVO_EXCEL = PASTA_BASE / "relatorio_faturas.xlsx"

# CNPJ no formato XX.XXX.XXX/XXXX-XX
RE_CNPJ = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
# NIF: exatamente 9 digitos (sem fazer parte de um numero maior)
RE_NIF = re.compile(r"(?<![\d.,/])\d{9}(?![\d.,/])")
# Valor total: linha com "Total" (Total:, Total a pagar:, VALOR TOTAL:)
# seguida de valor com ou sem "R$", em formato BR (1.500,00) ou ponto (1500.00).
RE_TOTAL = re.compile(
    r"total[^\n\d]*?(?:R\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+(?:[.,]\d{2})?)",
    re.IGNORECASE,
)
RE_EMISSAO = re.compile(r"(?:Emissao|Data)\s*:\s*(\d{2}/\d{2}/\d{4})", re.IGNORECASE)
RE_FORNECEDOR = re.compile(r"(?:Fornecedor|Razao Social)\s*:\s*(.+)", re.IGNORECASE)


def extrair_texto_pdf(caminho: Path) -> str:
    """Le todas as paginas do PDF e junta o texto."""
    with pdfplumber.open(caminho) as pdf:
        return "\n".join(pagina.extract_text() or "" for pagina in pdf.pages)


def converter_valor(texto: str) -> float:
    """Converte '1.500,00' ou '1500.00' para float."""
    if "," in texto:  # formato brasileiro: ponto = milhar, virgula = decimal
        texto = texto.replace(".", "").replace(",", ".")
    return float(texto)


def extrair_documento(texto: str) -> tuple[str | None, str | None]:
    """Retorna (documento, tipo), priorizando CNPJ e depois NIF."""
    cnpj = RE_CNPJ.search(texto)
    if cnpj:
        return cnpj.group(), "CNPJ"
    nif = RE_NIF.search(texto)
    if nif:
        return nif.group(), "NIF"
    return None, None


def extrair_total(texto: str) -> float | None:
    """Usa a ultima ocorrencia de 'Total' (o total geral fica no fim)."""
    ocorrencias = RE_TOTAL.findall(texto)
    return converter_valor(ocorrencias[-1]) if ocorrencias else None


def buscar(padrao: re.Pattern, texto: str) -> str | None:
    achado = re.search(padrao, texto)
    return achado.group(1).strip() if achado else None


def processar_fatura(caminho: Path) -> dict:
    texto = extrair_texto_pdf(caminho)
    documento, tipo = extrair_documento(texto)
    total = extrair_total(texto)
    return {
        "arquivo": caminho.name,
        "fornecedor": buscar(RE_FORNECEDOR, texto),
        "tipo_documento": tipo,
        "nif_cnpj": documento,
        "data_emissao": buscar(RE_EMISSAO, texto),
        "valor_total": total,
        "status": "OK" if documento and total is not None else "REVISAR",
    }


def main() -> None:
    pdfs = sorted(PASTA_FATURAS.glob("*.pdf"))
    if not pdfs:
        print(f"Nenhum PDF encontrado em {PASTA_FATURAS}")
        return

    faturas: list[dict] = []
    for caminho in pdfs:
        try:
            faturas.append(processar_fatura(caminho))
        except Exception as erro:  # PDF corrompido nao derruba o lote
            print(f"[ERRO] {caminho.name}: {erro}")
            faturas.append({"arquivo": caminho.name, "status": f"ERRO: {erro}"})

    df = pd.DataFrame(faturas)
    print(df.to_string(index=False))

    df.to_excel(ARQUIVO_EXCEL, index=False, sheet_name="Faturas")
    revisar = (df["status"] != "OK").sum()
    print(f"\n{len(df)} faturas salvas em {ARQUIVO_EXCEL.name} ({revisar} para revisar)")


if __name__ == "__main__":
    main()
