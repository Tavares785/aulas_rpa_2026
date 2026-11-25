from pathlib import Path
import re
import pandas as pd
import pdfplumber


PADRAO_DOC = r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b|\b\d{9}\b"
PADRAO_VALOR = r"(?:valor\s*total|total(?:\s*a\s*pagar)?)\s*:?\s*(?:R\$\s*)?([\d.,]+)"

def extrair_dados_fatura(caminho_pdf: Path) -> dict:
    with pdfplumber.open(caminho_pdf) as pdf:
        texto = "\n".join(pagina.extract_text() or "" for pagina in pdf.pages)

    busca_doc = re.search(PADRAO_DOC, texto)
    busca_valor = re.search(PADRAO_VALOR, texto, re.IGNORECASE)

    return {
        "arquivo": caminho_pdf.name,
        "nif_cnpj": busca_doc.group(0) if busca_doc else None,
        "valor_total": busca_valor.group(1) if busca_valor else None,
    }


def main() -> None:
    pasta_faturas = Path(__file__).resolve().parent / "faturas"
    arquivos_pdf = sorted(pasta_faturas.glob("*.pdf"))

    dados = [extrair_dados_fatura(arquivo) for arquivo in arquivos_pdf]
    df = pd.DataFrame(dados)

    caminho_saida = Path(__file__).resolve().parent / "relatorio_faturas.xlsx"
    df.to_excel(caminho_saida, index=False)


if __name__ == "__main__":
    main()