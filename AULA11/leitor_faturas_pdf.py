import pathlib
import re
import pandas as pd
import pdfplumber

PASTA_FATURAS = pathlib.Path(__file__).parent / "faturas"
ARQUIVO_SAIDA = pathlib.Path(__file__).parent / "relatorio_faturas.xlsx"

REGEX_DOCUMENTO = re.compile(r"\b(?:\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})\b")
REGEX_VALOR_TOTAL = re.compile(
    r"(?:Total(?:\s+a\s+pagar)?|VALOR\s+TOTAL)\s*:\s*(?:R\$\s*)?([\d.,]+)",
    re.IGNORECASE,
)
REGEX_DATA = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")
REGEX_FORNECEDOR = re.compile(
    r"(?:Fornecedor|Razao\s+Social)\s*:\s*(.+)",
    re.IGNORECASE,
)


def extrair_texto_pdf(caminho_pdf: pathlib.Path) -> str:
    """Lê todas as páginas de um arquivo PDF e concatena o texto."""
    paginas = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                paginas.append(texto)
    return "\n".join(paginas)


def normalizar_valor(valor_str: str | None) -> float | None:
    """Converte strings monetárias ('1.500,00' ou '1200.50') para float."""
    if not valor_str:
        return None
    if "," in valor_str:
        valor_limpo = valor_str.replace(".", "").replace(",", ".")
    else:
        valor_limpo = valor_str
    try:
        return float(valor_limpo)
    except ValueError:
        return None


def analisar_fatura(caminho_pdf: pathlib.Path) -> dict:
    """Extrai os campos estruturados de uma fatura via Expressões Regulares."""
    texto = extrair_texto_pdf(caminho_pdf)

    match_doc = re.search(REGEX_DOCUMENTO, texto)
    match_valor = re.search(REGEX_VALOR_TOTAL, texto)
    match_data = re.search(REGEX_DATA, texto)
    match_forn = re.search(REGEX_FORNECEDOR, texto)

    valor_bruto = match_valor.group(1) if match_valor else None

    return {
        "arquivo": caminho_pdf.name,
        "fornecedor": match_forn.group(1).strip() if match_forn else "Não identificado",
        "nif_cnpj": match_doc.group(0) if match_doc else "Não informado",
        "data_emissao": match_data.group(1) if match_data else "Não informada",
        "valor_bruto": valor_bruto if valor_bruto else "Não informado",
        "valor_total": normalizar_valor(valor_bruto),
    }


def processar_faturas(pasta: pathlib.Path, saida_xlsx: pathlib.Path) -> pd.DataFrame:
    """Processa todos os PDFs da pasta e exporta a tabela para Excel."""
    registros = []
    for arquivo_pdf in sorted(pasta.glob("*.pdf")):
        dados = analisar_fatura(arquivo_pdf)
        registros.append(dados)

    df = pd.DataFrame(registros)
    df.to_excel(saida_xlsx, index=False)
    return df


if __name__ == "__main__":
    df_resultado = processar_faturas(PASTA_FATURAS, ARQUIVO_SAIDA)
    print(df_resultado.to_string(index=False))
    print(f"\nRelatório salvo com sucesso em: {ARQUIVO_SAIDA}")
    
