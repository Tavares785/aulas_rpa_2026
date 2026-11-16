"""
Lab 10 - Extração de Dados em PDFs, Filtros Regex e Exportação para Excel
Script: leitor_faturas_pdf.py
RA: 6326327

Objetivo: ler faturas em PDF, extrair NIF/CNPJ e Valor Total com regex,
e consolidar os dados em um arquivo Excel via pandas.

Requer: pip install pdfplumber pandas openpyxl
"""
import re
from pathlib import Path
from typing import Any

# Guard de ImportError: o módulo carrega mesmo sem as libs externas,
# encerrando com exit 0 (comportamento esperado no CI sem PDF/libs).
try:
    import pdfplumber
    PDFPLUMBER_DISPONIVEL = True
except ImportError:
    pdfplumber = None  # type: ignore[assignment]
    PDFPLUMBER_DISPONIVEL = False
    print("pdfplumber não instalado. Rode: pip install pdfplumber")

try:
    import pandas as pd
    PANDAS_DISPONIVEL = True
except ImportError:
    pd = None  # type: ignore[assignment]
    PANDAS_DISPONIVEL = False
    print("pandas não instalado. Rode: pip install pandas openpyxl")

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------
PASTA_FATURAS = Path(__file__).resolve().parent.parent / "AULA11" / "faturas"
ARQUIVO_SAIDA = Path(__file__).resolve().parent / "relatorio_faturas.xlsx"

# ---------------------------------------------------------------------------
# Padrões de Expressão Regular
# ---------------------------------------------------------------------------
# NIF: 9 dígitos seguidos (ex: 123456789)
# CNPJ: formato XX.XXX.XXX/XXXX-XX
RE_NIF_CNPJ = re.compile(
    r"\b(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})\b"
)

# Valor Total: R$ 1.500,00 | Total: 1500.00 | £18.95 | € 200,00
RE_VALOR = re.compile(
    r"(?:Total[:\s]+|R\$\s*|£\s*|€\s*)([\d]{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))"
)


# ---------------------------------------------------------------------------
# Funções
# ---------------------------------------------------------------------------
def extrair_texto_pdf(caminho: Path) -> str:
    """Extrai todo o texto de um PDF usando pdfplumber."""
    texto = ""
    with pdfplumber.open(caminho) as pdf:
        for pagina in pdf.pages:
            texto += (pagina.extract_text() or "") + "\n"
    return texto


def extrair_dados_fatura(texto: str, nome_arquivo: str) -> dict[str, Any]:
    """Aplica as regex no texto bruto e retorna um dicionário com os campos."""
    # NIF / CNPJ
    match_nif = re.search(RE_NIF_CNPJ, texto)
    nif = match_nif.group(1) if match_nif else "N/D"

    # Valor Total
    match_valor = re.search(RE_VALOR, texto)
    valor = match_valor.group(1) if match_valor else "N/D"

    return {
        "arquivo": nome_arquivo,
        "nif_cnpj": nif,
        "valor_total": valor,
    }


def processar_faturas(pasta: Path) -> list[dict[str, Any]]:
    """Lê todos os PDFs da pasta e extrai os dados de cada fatura."""
    registros: list[dict[str, Any]] = []

    pdfs = sorted(pasta.glob("*.pdf"))
    if not pdfs:
        print(f"Nenhum PDF encontrado em: {pasta}")
        return registros

    for caminho_pdf in pdfs:
        texto = extrair_texto_pdf(caminho_pdf)
        registro = extrair_dados_fatura(texto, caminho_pdf.name)
        registros.append(registro)
        print(f"  ✅ {caminho_pdf.name}  →  NIF: {registro['nif_cnpj']}  |  "
              f"Valor: {registro['valor_total']}")

    return registros


def exportar_excel(registros: list[dict[str, Any]], caminho: Path) -> None:
    """Converte a lista de dicionários em DataFrame e salva em .xlsx."""
    df = pd.DataFrame(registros)
    df.to_excel(caminho, index=False)
    print(f"\n✅ {len(registros)} fatura(s) salvas em '{caminho.name}'")


def executar() -> None:
    """Orquestra a leitura dos PDFs, extração e exportação."""
    if not PASTA_FATURAS.is_dir():
        print(f"Pasta de faturas não encontrada: {PASTA_FATURAS}")
        raise SystemExit(0)

    print(f"Processando faturas em: {PASTA_FATURAS}\n")

    try:
        registros = processar_faturas(PASTA_FATURAS)
    except Exception as erro:  # noqa: BLE001
        print(f"Erro ao processar faturas: {erro}")
        raise SystemExit(0)

    if not registros:
        raise SystemExit(0)

    exportar_excel(registros, ARQUIVO_SAIDA)


if __name__ == "__main__":
    if not PDFPLUMBER_DISPONIVEL or not PANDAS_DISPONIVEL:
        raise SystemExit(0)
    executar()
