"""
Laboratório 11: Extração de Dados em PDFs, Filtros Regex e Exportação para Excel
Aluno: Vinicius Montagner
RA: 6326020
"""

import os
import re
import pandas as pd
import pdfplumber


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_FATURAS = os.path.join(BASE_DIR, "faturas")
ARQUIVO_SAIDA = os.path.join(BASE_DIR, "relatorio_faturas.xlsx")


def extrair_texto_pdf(caminho_pdf):
    """Lê todas as páginas de um PDF e retorna o texto concatenado."""
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
    return texto_completo


def normalizar_valor(valor_bruto):
    """Converte string monetária (BR ou US) para float."""
    if "," in valor_bruto and "." in valor_bruto:
        return float(valor_bruto.replace(".", "").replace(",", "."))
    if "," in valor_bruto:
        return float(valor_bruto.replace(",", "."))
    return float(valor_bruto)


def extrair_dados_fatura(texto, nome_arquivo):
    """Aplica Regex (re.search) para isolar NIF/CNPJ, Data e Valor Total."""
    padrao_nif_cnpj = r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\b\d{9}\b)"
    padrao_valor = (
        r"(?:Total\s*a\s*pagar|Valor\s*Total|Total)[:\s]*R?\$?\s*"
        r"(\d{1,3}(?:[.,]\d{3})*[.,]\d{2}|\d+[.,]\d{2})"
    )
    padrao_data = r"(\d{2}/\d{2}/\d{4})"

    match_doc = re.search(padrao_nif_cnpj, texto)
    match_valor = re.search(padrao_valor, texto, re.IGNORECASE)
    match_data = re.search(padrao_data, texto)

    nif_cnpj = match_doc.group(1) if match_doc else "Não encontrado"
    data_emissao = match_data.group(1) if match_data else "Não encontrada"
    valor_total = (
        normalizar_valor(match_valor.group(1)) if match_valor else 0.0
    )

    return {
        "Arquivo": nome_arquivo,
        "NIF_CNPJ": nif_cnpj,
        "Data_Emissao": data_emissao,
        "Valor_Total": valor_total,
    }


def processar_faturas(pasta_pdfs=PASTA_FATURAS, arquivo_saida=ARQUIVO_SAIDA):
    """Lê os PDFs da pasta, extrai os campos e salva em Excel."""
    lista_faturas = []

    if not os.path.exists(pasta_pdfs):
        print(f"Pasta não encontrada: {pasta_pdfs}")
        return

    arquivos = [
        f for f in sorted(os.listdir(pasta_pdfs)) if f.lower().endswith(".pdf")
    ]

    for arquivo in arquivos:
        caminho_pdf = os.path.join(pasta_pdfs, arquivo)
        texto = extrair_texto_pdf(caminho_pdf)
        dados = extrair_dados_fatura(texto, arquivo)
        lista_faturas.append(dados)

    df = pd.DataFrame(lista_faturas)
    df.to_excel(arquivo_saida, index=False, engine="openpyxl")

    print("\n--- Resumo das Faturas Extraídas ---")
    print(df.to_string(index=False))
    print(f"\nRelatório salvo em: {arquivo_saida}")


if __name__ == "__main__":
    processar_faturas() 
