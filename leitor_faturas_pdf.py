import os
import re
import pdfplumber
import pandas as pd


def extrair_dados_texto(texto: str, origem: str = "Simulação") -> dict:
    """Aplica regex para isolar NIF/CNPJ e Valor Total de um texto."""
    # 1. Padrão NIF (9 dígitos) ou CNPJ (XX.XXX.XXX/XXXX-XX)
    padrao_nif_cnpj = r"\b(?:\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})\b"
    match_doc = re.search(padrao_nif_cnpj, texto)
    nif_cnpj = match_doc.group(0) if match_doc else "Não encontrado"

    # 2. Padrão Valor Total (ex: R$ 1.500,00 ou Total: 1500.00)
    padrao_valor = r"(?:R\$\s*|Total:\s*)(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})|\d+(?:[.,]\d{2})?)"
    match_valor = re.search(padrao_valor, texto, re.IGNORECASE)
    valor_total = match_valor.group(1) if match_valor else "0.00"

    return {
        "Origem": origem,
        "NIF_CNPJ": nif_cnpj,
        "Valor_Total": valor_total
    }


def processar_faturas(caminhos_pdfs: list = None) -> list:
    """Lê arquivos PDF reais ou simula faturas caso não haja arquivos."""
    faturas_extraidas = []

    # Se houver arquivos PDF informados e existentes, extrai com pdfplumber
    if caminhos_pdfs:
        for caminho in caminhos_pdfs:
            if os.path.exists(caminho):
                with pdfplumber.open(caminho) as pdf:
                    for num_pagina, pagina in enumerate(pdf.pages, start=1):
                        texto = pagina.extract_text() or ""
                        dados = extrair_dados_texto(texto, f"{caminho} (Pág. {num_pagina})")
                        faturas_extraidas.append(dados)

    # Caso nenhum PDF real tenha sido encontrado, simula a extração de páginas
    if not faturas_extraidas:
        paginas_simuladas = [
            "FATURA #001\nCliente CNPJ: 12.345.678/0001-99\nServiços de TI\nValor a pagar: R$ 1.500,00",
            "FATURA #002\nContribuinte NIF: 987654321\nConsultoria Técnica\nTotal: 1500.00",
            "FATURA #003\nEmpresa CNPJ: 45.987.321/0001-55\nLicença de Software\nTotal: R$ 3.250,50"
        ]
        for idx, texto_pagina in enumerate(paginas_simuladas, start=1):
            dados = extrair_dados_texto(texto_pagina, f"Fatura_Simulada_{idx}.pdf")
            faturas_extraidas.append(dados)

    return faturas_extraidas


def main():
    # Lista opcional de PDFs reais na pasta atual
    arquivos_pdf = [f for f in os.listdir(".") if f.lower().endswith(".pdf")]

    # 5. Armazena as informações em uma lista de dicionários
    lista_faturas = processar_faturas(arquivos_pdf)

    # 6. Converte a lista em DataFrame do pandas e salva em Excel
    df = pd.DataFrame(lista_faturas)
    arquivo_saida = "relatorio_faturas.xlsx"
    df.to_excel(arquivo_saida, index=False)

    print("Processamento concluído com sucesso!")
    print(df)


if __name__ == "__main__":
    main()
