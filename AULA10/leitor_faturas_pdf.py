"""
AULA 10 / AULA 11 - Extracao de Dados em PDFs, Filtros Regex e Exportacao para Excel
Leitor de Faturas em PDF

Aluno: Kaua David Dantas Mendonca
RA: 6326260
"""

import re
from pathlib import Path
import pandas as pd
import pdfplumber

ARQUIVO_EXCEL = Path(__file__).resolve().parent / "relatorio_faturas.xlsx"

# Padroes de Expressao Regular
RE_CNPJ_NIF = re.compile(
    r"(?:CNPJ|NIF):\s*([0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2}|[0-9]{9})"
)
RE_VALOR_TOTAL = re.compile(
    r"(?:VALOR TOTAL|Total a pagar|Total):\s*(?:R\$\s*)?"
    r"([0-9]{1,3}(?:[\.,][0-9]{3})*(?:[\.,][0-9]{2})?|[0-9]+(?:[\.,][0-9]{2})?)"
)
RE_FORNECEDOR = re.compile(
    r"(?:Fornecedor|Razao Social):\s*(.+)"
)
RE_EMISSAO = re.compile(
    r"(?:Emissao|Data):\s*([0-9]{2}/[0-9]{2}/[0-9]{4})"
)


def extrair_dados_pdf(caminho_pdf: Path) -> dict:
    """Abre um arquivo PDF com pdfplumber e extrai os campos usando regex."""
    with pdfplumber.open(caminho_pdf) as pdf:
        texto_completo = "\n".join(
            (pagina.extract_text() or "") for pagina in pdf.pages
        )

    match_cnpj = re.search(RE_CNPJ_NIF, texto_completo)
    match_valor = re.search(RE_VALOR_TOTAL, texto_completo)
    match_fornecedor = re.search(RE_FORNECEDOR, texto_completo)
    match_emissao = re.search(RE_EMISSAO, texto_completo)

    return {
        "arquivo": caminho_pdf.name,
        "fornecedor": match_fornecedor.group(1).strip() if match_fornecedor else "N/D",
        "cnpj_nif": match_cnpj.group(1).strip() if match_cnpj else "N/D",
        "emissao": match_emissao.group(1).strip() if match_emissao else "N/D",
        "valor_total": match_valor.group(1).strip() if match_valor else "N/D"
    }


def localizar_arquivos_pdf() -> list[Path]:
    """Localiza as faturas em PDF nas pastas do projeto."""
    diretorio_atual = Path(__file__).resolve().parent
    pastas_busca = [
        diretorio_atual / "faturas",
        diretorio_atual.parent / "AULA11" / "faturas",
        diretorio_atual.parent / "lab-professor" / "AULA11" / "espelhos",
        Path("faturas")
    ]

    arquivos: list[Path] = []
    for pasta in pastas_busca:
        if pasta.exists():
            pdfs = sorted(pasta.glob("*.pdf"))
            if pdfs:
                arquivos.extend(pdfs)
                break

    return arquivos


def processar_faturas() -> pd.DataFrame:
    """Processa todas as faturas encontradas e consolida em DataFrame."""
    arquivos = localizar_arquivos_pdf()
    registros: list[dict] = []

    if not arquivos:
        print("Nenhum arquivo PDF encontrado. Criando dados demonstrativos...")
        registros = [
            {
                "arquivo": "fatura_001.pdf",
                "fornecedor": "Tech Solucoes em TI Ltda",
                "cnpj_nif": "12.345.678/0001-95",
                "emissao": "05/03/2026",
                "valor_total": "1.500,00"
            },
            {
                "arquivo": "fatura_002.pdf",
                "fornecedor": "Lusitana Componentes S.A.",
                "cnpj_nif": "501964843",
                "emissao": "12/03/2026",
                "valor_total": "1200.50"
            }
        ]
    else:
        print(f"Encontrados {len(arquivos)} arquivo(s) PDF para processar.")
        for caminho in arquivos:
            dados = extrair_dados_pdf(caminho)
            registros.append(dados)
            print(f"  {dados['arquivo']} -> CNPJ/NIF: {dados['cnpj_nif']} | Total: {dados['valor_total']}")

    df = pd.DataFrame(registros)
    return df


def exportar_para_excel(df: pd.DataFrame, caminho_saida: Path) -> None:
    """Exporta o DataFrame para uma planilha Excel (.xlsx)."""
    df.to_excel(caminho_saida, index=False, engine="openpyxl")
    print(f"\nRelatorio consolidado exportado com sucesso em: {caminho_saida}")


def main() -> None:
    """Fluxo principal do leitor de faturas."""
    print("=" * 60)
    print("PROCESSAMENTO DE FATURAS EM PDF COM REGEX E EXCEL")
    print("=" * 60)

    df_faturas = processar_faturas()
    exportar_para_excel(df_faturas, ARQUIVO_EXCEL)


if __name__ == "__main__":
    main()
