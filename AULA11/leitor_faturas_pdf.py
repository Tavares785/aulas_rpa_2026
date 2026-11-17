import os
import re
import pandas as pd
import pdfplumber


def extrair_texto_pdf(caminho_pdf: str) -> str:
    """Abre um arquivo PDF e concatena o texto de todas as suas páginas."""
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
    return texto_completo


def extrair_dados_fatura(texto: str, nome_arquivo: str) -> dict:
    """Aplica Expressões Regulares para extrair NIF/CNPJ, Data e Valor Total."""

    # Padrão para CNPJ (XX.XXX.XXX/XXXX-XX) ou NIF (espero que funcione) (9 dígitos isolados)
    padrao_doc = r"\b(?:\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})\b"
    match_doc = re.search(padrao_doc, texto)
    nif_cnpj = match_doc.group(0) if match_doc else "Não encontrado"

    # Padrão para Data (DD/MM/AAAA ou DD-MM-AAAA)
    padrao_data = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"
    match_data = re.search(padrao_data, texto)
    data_emissao = match_data.group(0) if match_data else "Não encontrada"

    # Padrão para Valor Total
    # Captura formatos como: "R$ 1.500,00", "Total: 1500.00", "Valor Total R$ 250,50"
    padrao_valor = r"(?:Total|Valor Total|R\$|€|\$)\s*:?\s*(?:R\$|€|\$)?\s*([\d.,]+)"
    match_valor = re.search(padrao_valor, texto, re.IGNORECASE)
    valor_total = match_valor.group(1) if match_valor else "0,00"

    return {
        "Arquivo": nome_arquivo,
        "NIF_CNPJ": nif_cnpj,
        "Data_Emissao": data_emissao,
        "Valor_Total": valor_total,
    }


def processar_pasta_faturas(pasta_entrada: str, arquivo_saida: str):
    """Lê todos os PDFs de uma pasta, extrai os dados e salva em Excel."""
    dados_consolidados = []

    # Só pra n dar merda
    if not os.path.exists(pasta_entrada):
        os.makedirs(pasta_entrada)
        print(
            f"Pasta '{pasta_entrada}' criada. Coloque seus PDFs nela e rode novamente."
        )
        return

    arquivos = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(".pdf")]

    if not arquivos:
        print(f"Nenhum arquivo PDF encontrado na pasta '{pasta_entrada}'.")
        return

    for arquivo in arquivos:
        caminho_completo = os.path.join(pasta_entrada, arquivo)
        print(f"Processando: {arquivo}...")

        texto_bruto = extrair_texto_pdf(caminho_completo)
        registro = extrair_dados_fatura(texto_bruto, arquivo)
        dados_consolidados.append(registro)

    # Espero que essa desgraça exporte pra excel
    df = pd.DataFrame(dados_consolidados)
    df.to_excel(arquivo_saida, index=False, engine="openpyxl")
    print(f"\nSucesso! Relatório gerado em: {arquivo_saida}")


if __name__ == "__main__":
    PASTA_FATURAS = "./faturas_pdf"
    ARQUIVO_EXCEL = "relatorio_faturas.xlsx"

    processar_pasta_faturas(PASTA_FATURAS, ARQUIVO_EXCEL)
