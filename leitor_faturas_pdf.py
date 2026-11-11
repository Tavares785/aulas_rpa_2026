"""
Lab 11 - Extração de Dados em PDFs, Filtros Regex e Exportação para Excel
=========================================================================

Robô que automatiza o pipeline de leitura de faturas em PDF:
  1. Extrai o texto de cada página usando pdfplumber.
  2. Aplica Expressões Regulares (re.search) para isolar:
       - NIF  : 9 dígitos numéricos
       - CNPJ : formato XX.XXX.XXX/XXXX-XX
       - Valor Total: padrão monetário (R$ 1.500,00 ou Total: 1500.00)
       - Data : formato DD/MM/AAAA (extração complementar)
  3. Armazena os dados de cada fatura em uma lista de dicionários.
  4. Converte a lista em um DataFrame do pandas e salva em relatorio_faturas.xlsx.

Bibliotecas necessárias:
    pip install pdfplumber pandas openpyxl
"""

import os
import re
import pdfplumber
import pandas as pd


# ---------------------------------------------------------------------------
# Expressões Regulares (re) para localizar padrões no texto bruto
# ---------------------------------------------------------------------------

# CNPJ (Brasil): formato XX.XXX.XXX/XXXX-XX  ->  prioritário
PADRAO_CNPJ = re.compile(r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})")

# NIF (Portugal): 9 dígitos consecutivos, preferencialmente após o rótulo "NIF"
PADRAO_NIF_ROTULADO = re.compile(r"NIF[:\s\-]*(\d{9})", re.IGNORECASE)
# Fallback: 9 dígitos isolados por limites de palavra (\b)
PADRAO_NIF_LIVRE = re.compile(r"\b(\d{9})\b")

# Valor Total com rótulo: "Total: 1500.00", "VALOR TOTAL: R$ 1.500,00", etc.
# \b evita que "Total" case com "Subtotal" (limite de palavra antes/depois).
PADRAO_VALOR_ROTULADO = re.compile(
    r"(?:VALOR\s*TOTAL|\bTotal\b)[:\s]*(?:R\$\s*)?([\d.,]+)",
    re.IGNORECASE,
)
# Valor Total sem rótulo, no formato brasileiro: "R$ 1.500,00"
PADRAO_VALOR_REAL = re.compile(r"R\$\s*([\d.]+,\d{2})")

# Data no formato DD/MM/AAAA (extração complementar citada nos objetivos)
PADRAO_DATA = re.compile(r"(\d{2}/\d{2}/\d{4})")


# ---------------------------------------------------------------------------
# Funções de extração por padrão
# ---------------------------------------------------------------------------

def extrair_nif_cnpj(texto):
    """
    Localiza o NIF (9 dígitos) ou CNPJ (XX.XXX.XXX/XXXX-XX) no texto.

    Prioriza o CNPJ formatado; caso não exista, procura o NIF rotulado
    (após a palavra "NIF") e, por fim, um NIF de 9 dígitos isolados.
    """
    # 1) Tenta o CNPJ no formato XX.XXX.XXX/XXXX-XX
    match_cnpj = PADRAO_CNPJ.search(texto)
    if match_cnpj:
        return match_cnpj.group(1)

    # 2) Tenta o NIF rotulado (ex.: "NIF: 123456789")
    match_nif_rot = PADRAO_NIF_ROTULADO.search(texto)
    if match_nif_rot:
        return match_nif_rot.group(1)

    # 3) Fallback: 9 dígitos isolados no texto
    match_nif_livre = PADRAO_NIF_LIVRE.search(texto)
    if match_nif_livre:
        return match_nif_livre.group(1)

    return None


def extrair_valor_total(texto):
    """
    Localiza o Valor Total monetário no texto.

    Aceita formatos como:
      - "Total: 1500.00"
      - "VALOR TOTAL: R$ 1.500,00"
      - "R$ 1.500,00"  (sem rótulo)
    """
    # 1) Tenta valor precedido por rótulo "Total"/"VALOR TOTAL"
    match_rot = PADRAO_VALOR_ROTULADO.search(texto)
    if match_rot:
        return match_rot.group(1)

    # 2) Fallback: valor no formato "R$ X.XXX,XX"
    match_real = PADRAO_VALOR_REAL.search(texto)
    if match_real:
        return match_real.group(1)

    return None


def extrair_data(texto):
    """Localiza uma data no formato DD/MM/AAAA (extração complementar)."""
    match = PADRAO_DATA.search(texto)
    if match:
        return match.group(1)
    return None


# ---------------------------------------------------------------------------
# Leitura de PDF com pdfplumber
# ---------------------------------------------------------------------------

def extrair_texto_pdf(caminho_pdf):
    """
    Usa pdfplumber para extrair o texto de cada página do PDF,
    concatenando todo o conteúdo em uma única string.
    """
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text() or ""
            texto_completo += texto_pagina + "\n"
    return texto_completo


def extrair_dados_fatura(texto, nome_arquivo="simulado"):
    """
    Aplica as regras de regex para isolar NIF/CNPJ, Valor Total e Data
    do texto bruto de uma fatura, retornando um dicionário estruturado.
    """
    return {
        "Arquivo": nome_arquivo,
        "NIF_CNPJ": extrair_nif_cnpj(texto),
        "Valor_Total": extrair_valor_total(texto),
        "Data": extrair_data(texto),
    }


# ---------------------------------------------------------------------------
# Dados simulados (fallback quando não há PDFs reais na pasta)
# ---------------------------------------------------------------------------

FATURAS_SIMULADAS = [
    {
        "arquivo": "fatura_001.pdf",
        "texto": (
            "FATURA Nº 2024/0001\n"
            "Data: 15/03/2024\n"
            "Fornecedor: Tech Solutions Lda\n"
            "NIF: 123456789\n"
            "Descrição: Serviços de consultoria\n"
            "Subtotal: 1.200,00\n"
            "Total: R$ 1.500,00\n"
        ),
    },
    {
        "arquivo": "fatura_002.pdf",
        "texto": (
            "NOTA FISCAL ELETRÔNICA\n"
            "CNPJ: 12.345.678/0001-99\n"
            "Data de emissão: 22/05/2024\n"
            "Razão Social: Comércio Geral Ltda\n"
            "Itens:\n"
            "  - Produto A  1.000,00\n"
            "  - Produto B  1.500,75\n"
            "VALOR TOTAL: 2500.75\n"
        ),
    },
    {
        "arquivo": "fatura_003.pdf",
        "texto": (
            "INVOICE #2024-003\n"
            "Supplier: Global Services Ltd\n"
            "NIF: 987654321\n"
            "Date: 10/07/2024\n"
            "Services rendered: 3.000,00\n"
            "Discount: 250,00\n"
            "R$ 3.250,00\n"
        ),
    },
    {
        "arquivo": "fatura_004.pdf",
        "texto": (
            "FATURA DE SERVIÇOS\n"
            "Empresa: Logística Express S.A.\n"
            "CNPJ: 98.765.432/0001-10\n"
            "Emissão: 05/09/2024\n"
            "Frete interestadual  4.200,00\n"
            "Seguro  300,00\n"
            "Total: R$ 4.500,00\n"
        ),
    },
    {
        "arquivo": "fatura_005.pdf",
        "texto": (
            "RECIBO\n"
            "Prestador: João Silva ME\n"
            "NIF 555666777\n"
            "Data: 30/11/2024\n"
            "Prestação de serviços contínuos\n"
            "Total: 890.50\n"
        ),
    },
]


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def processar_faturas(pasta_pdf="./faturas"):
    """
    Processa todas as faturas disponíveis:
      - Se existirem PDFs na pasta informada, extrai o texto de cada PDF.
      - Caso contrário, utiliza as faturas simuladas para demonstração.

    Retorna uma lista de dicionários com os dados extraídos de cada fatura.
    """
    dados_extraidos = []

    # --- Tentativa de leitura de PDFs reais ---
    if os.path.isdir(pasta_pdf):
        arquivos_pdf = [
            f for f in os.listdir(pasta_pdf) if f.lower().endswith(".pdf")
        ]
        if arquivos_pdf:
            print(f"[INFO] {len(arquivos_pdf)} PDF(s) encontrado(s) em '{pasta_pdf}'.")
            for nome in sorted(arquivos_pdf):
                caminho = os.path.join(pasta_pdf, nome)
                print(f"  -> Lendo: {nome}")
                try:
                    texto = extrair_texto_pdf(caminho)
                    dados = extrair_dados_fatura(texto, nome)
                    dados_extraidos.append(dados)
                except Exception as exc:
                    print(f"     [ERRO] Falha ao ler {nome}: {exc}")
            return dados_extraidos

    # --- Fallback: faturas simuladas ---
    print("[INFO] Nenhum PDF encontrado na pasta './faturas'.")
    print("[INFO] Utilizando faturas SIMULADAS para demonstração.\n")
    for fatura in FATURAS_SIMULADAS:
        print(f"  -> Simulando leitura: {fatura['arquivo']}")
        dados = extrair_dados_fatura(fatura["texto"], fatura["arquivo"])
        dados_extraidos.append(dados)

    return dados_extraidos


def main():
    """Executa o pipeline completo: extração -> DataFrame -> Excel."""
    print("=" * 60)
    print("Lab 11 - Leitor de Faturas em PDF")
    print("=" * 60)

    # 1) Extrair dados das faturas (PDF reais ou simuladas)
    dados = processar_faturas()

    if not dados:
        print("[AVISO] Nenhuma fatura foi processada. Encerrando.")
        return

    # 2) Exibir os dados extraídos no console
    print("\n" + "-" * 60)
    print("Dados extraídos:")
    print("-" * 60)
    for item in dados:
        print(item)

    # 3) Converter a lista de dicionários em DataFrame do pandas
    df = pd.DataFrame(dados)
    print("\n" + "-" * 60)
    print("DataFrame gerado:")
    print("-" * 60)
    print(df.to_string(index=False))

    # 4) Salvar em arquivo Excel
    arquivo_excel = "relatorio_faturas.xlsx"
    try:
        df.to_excel(arquivo_excel, index=False, sheet_name="Faturas")
        print(f"\n[OK] Relatório salvo em: {arquivo_excel}")
    except PermissionError:
        print(f"\n[ERRO] Não foi possível salvar '{arquivo_excel}'.")
        print("       O arquivo pode estar aberto em outro programa (ex: Excel).")
        print("       Feche-o e execute o script novamente.")
    print("=" * 60)


if __name__ == "__main__":
    main()
