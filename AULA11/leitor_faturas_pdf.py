"""
Lab 11: Extração de Dados em PDFs, Filtros Regex e Exportação para Excel
Disciplina: Automação Robótica de Processos (RPA)

Pipeline automatizado para:
1. Leitura de faturas em PDF na pasta 'faturas' usando pdfplumber.
2. Extração de padrões com Expressões Regulares (re.search):
   - NIF/CNPJ: 9 dígitos numéricos ou formato XX.XXX.XXX/XXXX-XX
   - Valor Total: Padrão numérico monetário (ex: R$ 1.500,00 ou Total: 1200.50)
   - Fornecedor / Razão Social e Data de Emissão (quando disponíveis)
3. Estruturação em lista de dicionários.
4. Conversão para DataFrame do pandas e exportação para Excel ('relatorio_faturas.xlsx').
"""

import re
from pathlib import Path
import pandas as pd
import pdfplumber

# Definição dos caminhos das pastas e arquivos
DIRETORIO_ATUAL = Path(__file__).resolve().parent
PASTA_FATURAS = DIRETORIO_ATUAL / "faturas"
ARQUIVO_EXCEL = DIRETORIO_ATUAL / "relatorio_faturas.xlsx"

# Expressões Regulares compiladas para isolar os padrões solicitados
# NIF / CNPJ: padrão de 9 dígitos numéricos (NIF) ou XX.XXX.XXX/XXXX-XX (CNPJ)
RE_CNPJ_NIF = re.compile(
    r"(?:CNPJ|NIF)?\s*:?\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\b\d{9}\b)"
)

# Valor Total: padrão numérico monetário (com R$ ou prefixo Total / Valor Total)
RE_VALOR_TOTAL = re.compile(
    r"(?:total(?: a pagar)?|valor total)\s*:\s*(R\$\s*[\d.,]+|[\d.,]+)",
    re.IGNORECASE,
)

# Fornecedor / Razão Social
RE_FORNECEDOR = re.compile(
    r"(?:Fornecedor|Razao Social)\s*:\s*(.+)",
    re.IGNORECASE,
)

# Data de Emissão
RE_DATA = re.compile(
    r"(?:Emissao|Data)\s*:\s*(\d{2}/\d{2}/\d{4})",
    re.IGNORECASE,
)


def extrair_texto_pdf(caminho_pdf: Path) -> str:
    """Extrai todo o texto não estruturado de todas as páginas do PDF."""
    texto_completo = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            conteudo = pagina.extract_text()
            if conteudo:
                texto_completo.append(conteudo)
    return "\n".join(texto_completo)


def processar_fatura(caminho_pdf: Path) -> dict:
    """Aplica regras de regex no texto extraído de uma fatura PDF."""
    texto = extrair_texto_pdf(caminho_pdf)

    match_doc = RE_CNPJ_NIF.search(texto)
    match_valor = RE_VALOR_TOTAL.search(texto)
    match_fornecedor = RE_FORNECEDOR.search(texto)
    match_data = RE_DATA.search(texto)

    return {
        "arquivo": caminho_pdf.name,
        "fornecedor": match_fornecedor.group(1).strip() if match_fornecedor else "Não informado",
        "nif_cnpj": match_doc.group(1).strip() if match_doc else "Não informado",
        "valor_total": match_valor.group(1).strip() if match_valor else "Não informado",
        "data_emissao": match_data.group(1).strip() if match_data else "Não informado",
    }


def main():
    print("=" * 60)
    print(" INICIANDO PROCESSAMENTO DE FATURAS EM PDF (LAB 11) ")
    print("=" * 60)

    if not PASTA_FATURAS.exists():
        print(f"Erro: Pasta de faturas não encontrada em: {PASTA_FATURAS}")
        return

    arquivos_pdf = sorted(PASTA_FATURAS.glob("*.pdf"))
    if not arquivos_pdf:
        print(f"Nenhum arquivo PDF encontrado em: {PASTA_FATURAS}")
        return

    print(f"Total de faturas encontradas: {len(arquivos_pdf)}\n")

    lista_faturas = []
    for pdf_path in arquivos_pdf:
        print(f"Lendo e processando: {pdf_path.name}...")
        dados = processar_fatura(pdf_path)
        lista_faturas.append(dados)

    print("\n" + "-" * 60)
    print(" RESUMO DOS DADOS EXTRAÍDOS ")
    print("-" * 60)

    # Conversão para DataFrame do pandas
    df = pd.DataFrame(lista_faturas)
    print(df.to_string(index=False))

    # Exportação para arquivo Excel
    df.to_excel(ARQUIVO_EXCEL, index=False)
    print("-" * 60)
    print(f"Relatório exportado com sucesso para: {ARQUIVO_EXCEL.name}")
    print("=" * 60)


if __name__ == "__main__":
    main()

