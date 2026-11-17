"""Extrai NIF/CNPJ e valor total de faturas PDF e exporta para Excel."""

import re
from pathlib import Path

import pandas as pd
import pdfplumber


PASTA_FATURAS = Path(__file__).resolve().parent / "faturas"
ARQUIVO_SAIDA = Path(__file__).resolve().with_name("relatorio_faturas.xlsx")
COLUNAS = ["arquivo", "nif_cnpj", "valor_total"]

RE_NIF_CNPJ = re.compile(
    r"(?<!\d)(?:\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})(?!\d)"
)
RE_TOTAL_ROTULADO = re.compile(
    r"\b(?:total(?:\s+(?:a\s+pagar|da\s+fatura|devido|geral))?|valor\s+total)"
    r"\b\s*[:\-]?\s*"
    r"((?:R\$\s*)?(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d{2}|\.\d{2}))",
    re.IGNORECASE,
)
RE_VALOR = re.compile(
    r"(?<![\d.,/])"
    r"((?:R\$\s*)?(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d{2}|\.\d{2}))"
    r"(?![\d.,/-])"
)


def extrair_texto(caminho: Path) -> str:
    """Extrai e concatena o texto de todas as páginas do PDF."""
    with pdfplumber.open(caminho) as pdf:
        return "\n".join(pagina.extract_text() or "" for pagina in pdf.pages)


def extrair_dados(texto: str, arquivo: str) -> dict[str, str | None]:
    """Localiza identificador fiscal e valor total no texto da fatura."""
    identificador = re.search(RE_NIF_CNPJ, texto)
    valor = re.search(RE_TOTAL_ROTULADO, texto) or re.search(RE_VALOR, texto)
    return {
        "arquivo": arquivo,
        "nif_cnpj": identificador.group(0) if identificador else None,
        "valor_total": valor.group(1).strip() if valor else None,
    }


def processar_faturas(pasta: Path = PASTA_FATURAS) -> list[dict[str, str | None]]:
    """Lê todas as faturas PDF da pasta e retorna seus dados extraídos."""
    arquivos = sorted(pasta.glob("*.pdf"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo PDF encontrado em {pasta}")

    return [
        extrair_dados(extrair_texto(caminho), caminho.name)
        for caminho in arquivos
    ]


def salvar_excel(
    faturas: list[dict[str, str | None]], caminho: Path = ARQUIVO_SAIDA
) -> None:
    """Exporta os dados extraídos para uma planilha Excel."""
    pd.DataFrame(faturas, columns=COLUNAS).to_excel(caminho, index=False)


def executar() -> None:
    """Processa as faturas de exemplo e gera o relatório Excel."""
    faturas = processar_faturas()
    salvar_excel(faturas)
    print(f"{len(faturas)} faturas salvas em {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    executar()
