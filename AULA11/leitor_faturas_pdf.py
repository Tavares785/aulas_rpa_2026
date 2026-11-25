"""
Lab 11 - Extração de Dados em PDFs, Filtros Regex e Exportação para Excel
Aluna: Joyce - RA 6326057

Fluxo do robô:
1. Lê o texto de cada página dos PDFs (pdfplumber) que estão na mesma
   pasta deste script (e na subpasta "faturas/", se existir).
2. Aplica Regex (re.search) para extrair NIF/CNPJ e Valor Total.
3. Guarda cada fatura em uma lista de dicionários.
4. Converte para DataFrame (pandas) e salva em "relatorio_faturas.xlsx".
"""

import os
import re
import logging

import pandas as pd
import pdfplumber

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Caminhos sempre relativos à pasta onde o script está (AULA11)
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTAS_FATURAS = [PASTA_BASE, os.path.join(PASTA_BASE, "faturas")]
ARQUIVO_SAIDA = os.path.join(PASTA_BASE, "relatorio_faturas.xlsx")

# --- Padrões Regex ----------------------------------------------------------
# CNPJ no formato XX.XXX.XXX/XXXX-XX
PADRAO_CNPJ = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"
# NIF: exatamente 9 dígitos seguidos (\b = borda da palavra)
PADRAO_NIF = r"\b\d{9}\b"
# Valor com R$ (ex: R$ 1.500,00)
PADRAO_VALOR_REAIS = r"R\$\s*(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})"
# Valor após a palavra Total (ex: Total: 1500.00)
PADRAO_VALOR_TOTAL = r"Total\s*:?\s*(\d+(?:[.,]\d{2})?)"


def extrair_texto_pdf(caminho_pdf):
    """Abre o PDF com pdfplumber e junta o texto de todas as páginas."""
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for numero, pagina in enumerate(pdf.pages, start=1):
            texto_pagina = pagina.extract_text() or ""
            nome = os.path.basename(caminho_pdf)
            logging.info(f"{nome} - página {numero} lida")
            texto_completo += texto_pagina + "\n"
    return texto_completo


def extrair_documento(texto):
    """Procura primeiro um CNPJ; se não achar, procura um NIF de 9 dígitos."""
    achado = re.search(PADRAO_CNPJ, texto)
    if achado:
        return achado.group()
    achado = re.search(PADRAO_NIF, texto)
    if achado:
        return achado.group()
    return None


def converter_valor(valor_texto):
    """Converte '1.500,00' ou '1500.00' em float (1500.0)."""
    if "," in valor_texto:
        valor_texto = valor_texto.replace(".", "").replace(",", ".")
    return float(valor_texto)


def extrair_valor(texto):
    """Procura valor com R$; se não achar, procura 'Total: 0000.00'."""
    achado = re.search(PADRAO_VALOR_REAIS, texto)
    if not achado:
        achado = re.search(PADRAO_VALOR_TOTAL, texto, re.IGNORECASE)
    if achado:
        return converter_valor(achado.group(1))
    return None


def carregar_faturas():
    """Retorna um dicionário {nome_arquivo: texto} com os PDFs encontrados."""
    textos = {}
    for pasta in PASTAS_FATURAS:
        if not os.path.isdir(pasta):
            continue
        for nome in sorted(os.listdir(pasta)):
            if nome.lower().endswith(".pdf"):
                caminho = os.path.join(pasta, nome)
                try:
                    textos[nome] = extrair_texto_pdf(caminho)
                except Exception as erro:
                    logging.error(f"Falha ao ler {nome}: {erro}")

    if not textos:
        logging.warning(f"Nenhum PDF encontrado em {PASTA_BASE}")
    return textos


def processar_faturas():
    """Aplica as regras Regex em cada fatura e monta a lista de dicionários."""
    resultados = []
    for arquivo, texto in carregar_faturas().items():
        documento = extrair_documento(texto)
        valor = extrair_valor(texto)
        status = "OK" if documento and valor is not None else "PENDENTE"

        resultados.append({
            "arquivo": arquivo,
            "nif_cnpj": documento,
            "valor_total": valor,
            "status": status,
        })
        logging.info(
            f"{arquivo}: documento={documento} valor={valor} status={status}"
        )
    return resultados


def salvar_excel(resultados, caminho=ARQUIVO_SAIDA):
    """Converte a lista em DataFrame e salva no Excel."""
    df = pd.DataFrame(resultados)
    df.to_excel(caminho, index=False, engine="openpyxl")
    logging.info(f"Relatório salvo em {caminho} ({len(df)} faturas)")
    return df


def main():
    resultados = processar_faturas()
    if not resultados:
        logging.error("Nada para exportar. Coloque os PDFs em faturas/.")
        return
    df = salvar_excel(resultados)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
