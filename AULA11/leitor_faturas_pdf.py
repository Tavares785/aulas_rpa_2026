"""Extrai identificadores e valores totais de faturas PDF para Excel."""

import re
from pathlib import Path

import pandas as pd
import pdfplumber

PASTA_FATURAS = Path(__file__).resolve().parent / "faturas"
ARQUIVO_SAIDA = Path(__file__).resolve().parent / "relatorio_faturas.xlsx"
RE_IDENTIFICADOR = re.compile(
    r"(?:NIF|CNPJ)\s*:\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})",
    re.IGNORECASE,
)
RE_VALOR_TOTAL = re.compile(
    r"(?:VALOR\s+TOTAL|TOTAL(?:\s+A\s+PAGAR)?)\s*:\s*"
    r"(?P<moeda>R\$\s*)?"
    r"(?P<valor>\d{1,3}(?:\.\d{3})+,\d{2}|\d+,\d{2}|\d+(?:\.\d{2})?)",
    re.IGNORECASE,
)


def ler_texto(caminho: Path) -> str:
    """Extrai e concatena o texto de todas as páginas de um PDF."""
    with pdfplumber.open(caminho) as pdf:
        return "\n".join(pagina.extract_text() or "" for pagina in pdf.pages)


def extrair_dados(texto: str, arquivo: str) -> dict[str, str | None]:
    """Localiza o NIF/CNPJ e o valor total de uma fatura."""
    identificador = RE_IDENTIFICADOR.search(texto)
    valor_total = RE_VALOR_TOTAL.search(texto)

    valor = None
    if valor_total:
        moeda = valor_total.group("moeda") or ""
        valor = f"{moeda}{valor_total.group('valor')}".strip()

    return {
        "arquivo": arquivo,
        "nif_cnpj": identificador.group(1) if identificador else None,
        "valor_total": valor,
    }


def processar_faturas(pasta: Path = PASTA_FATURAS) -> list[dict[str, str | None]]:
    """Lê cada PDF da pasta e retorna um registro por fatura."""
    return [
        extrair_dados(ler_texto(caminho), caminho.name)
        for caminho in sorted(pasta.glob("*.pdf"))
    ]


def exportar_excel(
    faturas: list[dict[str, str | None]],
    caminho: Path = ARQUIVO_SAIDA,
) -> None:
    """Salva os registros em relatorio_faturas.xlsx."""
    colunas = ["arquivo", "nif_cnpj", "valor_total"]
    pd.DataFrame(faturas, columns=colunas).to_excel(caminho, index=False)


def executar() -> None:
    """Processa as faturas e gera o relatório Excel."""
    faturas = processar_faturas()
    exportar_excel(faturas, ARQUIVO_SAIDA)
    print(f"{len(faturas)} faturas salvas em {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    executar()
