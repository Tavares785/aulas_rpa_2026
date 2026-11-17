import re
from pathlib import Path
import pandas as pd
import pdfplumber


PASTA_FATURAS = Path(__file__).resolve().parent / "faturas"
ARQUIVO_SAIDA = Path(__file__).resolve().parent / "relatorio_faturas.xlsx"

RE_NIF_CNPJ = re.compile(
    r"\b(?:NIF|CNPJ)\s*[:.]?\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})\b",
    re.IGNORECASE,
)
RE_TOTAL = re.compile(
    r"\btotal(?:\s+a\s+pagar)?\s*:\s*"
    r"((?:R\$\s*)?(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d{2}|\.\d{2}))",
    re.IGNORECASE,
)
RE_VALOR_COM_REAIS = re.compile(
    r"R\$\s*(?:\d{1,3}(?:\.\d{3})+|\d+),\d{2}",
    re.IGNORECASE,
)


def extrair_texto_pdf(caminho: Path) -> str:
    with pdfplumber.open(caminho) as pdf:
        return "\n".join(pagina.extract_text() or "" for pagina in pdf.pages)


def extrair_dados_fatura(texto: str, nome_arquivo: str) -> dict[str, str | None]:
    nif_cnpj = RE_NIF_CNPJ.search(texto)
    total = RE_TOTAL.search(texto)
    if total is not None:
        valor_total = total.group(1)
    else:
        valores_com_reais = list(RE_VALOR_COM_REAIS.finditer(texto))
        valor_total = valores_com_reais[-1].group(0) if valores_com_reais else None

    return {
        "arquivo": nome_arquivo,
        "nif_cnpj": nif_cnpj.group(1) if nif_cnpj else None,
        "valor_total": valor_total,
    }


def processar_faturas(pasta: Path) -> list[dict[str, str | None]]:
    if not pasta.is_dir():
        raise FileNotFoundError(f"Pasta de faturas não encontrada: {pasta}")

    registros = []
    for caminho in sorted(pasta.glob("*.pdf")):
        texto = extrair_texto_pdf(caminho)
        registros.append(extrair_dados_fatura(texto, caminho.name))
    return registros


def main() -> None:
    registros = processar_faturas(PASTA_FATURAS)
    relatorio = pd.DataFrame(
        registros,
        columns=["arquivo", "nif_cnpj", "valor_total"],
    )
    relatorio.to_excel(ARQUIVO_SAIDA, index=False)
    print(f"Relatório salvo em {ARQUIVO_SAIDA} ({len(registros)} faturas).")


if __name__ == "__main__":
    main()
