import glob
import os
import re
import pandas as pd
import pdfplumber


def extrair_dados_fatura(texto, nome_origem):
    """Aplica Regex no texto bruto para isolar NIF/CNPJ e Valor Total."""
    # 1. Regex para NIF (9 dígitos) ou CNPJ (XX.XXX.XXX/XXXX-XX)
    padrao_nif_cnpj = r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\b\d{9}\b)"
    match_doc = re.search(padrao_nif_cnpj, texto)
    nif_cnpj = match_doc.group(1) if match_doc else "Não encontrado"

    # 2. Regex para Valor Total (ex: Total: R$ 1.500,00 ou Total: 1500.00)
    padrao_valor = r"(?:Total|Valor Total)[:\s]*(?:R\$\s*)?([\d.,]+)"
    match_valor = re.search(padrao_valor, texto, re.IGNORECASE)
    valor_total = match_valor.group(1) if match_valor else "0,00"

    return {
        "origem": nome_origem,
        "nif_cnpj": nif_cnpj,
        "valor_total": valor_total,
    }


def main():
    dados_faturas = []

    # Procura por arquivos PDF reais na pasta atual (ou subpasta faturas/)
    arquivos_pdf = glob.glob("*.pdf") + glob.glob("faturas/*.pdf")

    if arquivos_pdf:
        print(f"Lendo {len(arquivos_pdf)} arquivo(s) PDF encontrados...\n")
        for caminho_pdf in arquivos_pdf:
            texto_completo = ""
            # Abre o PDF e extrai o texto de todas as páginas
            with pdfplumber.open(caminho_pdf) as pdf:
                for pagina in pdf.pages:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina:
                        texto_completo += texto_pagina + "\n"

            registro = extrair_dados_fatura(
                texto_completo, os.path.basename(caminho_pdf)
            )
            dados_faturas.append(registro)
    else:
        # Simulação caso não haja arquivos PDF físicos na pasta do projeto
        print(
            "Nenhum PDF encontrado na pasta. Executando com faturas simuladas...\n"
        )
        faturas_simuladas = [
            (
                "fatura_001.pdf",
                """
                FATURA DE SERVIÇOS #001
                Fornecedor: Tech Solutions LTDA
                CNPJ: 12.345.678/0001-99
                Data de Emissão: 10/11/2026
                Valor Total: R$ 1.500,00
                """,
            ),
            (
                "fatura_002.pdf",
                """
                INVOICE #9842
                Supplier: Lusitania Cloud SA
                NIF: 509123456
                Date: 12/11/2026
                Total: 2450.75
                """,
            ),
            (
                "fatura_003.pdf",
                """
                NOTA FISCAL DE SERVIÇO
                Empresa: Alfa Suprimentos S/A
                CNPJ: 98.765.432/0001-10
                Total: R$ 890,50
                """,
            ),
        ]

        for nome_arquivo, texto_simulado in faturas_simuladas:
            registro = extrair_dados_fatura(texto_simulado, nome_arquivo)
            dados_faturas.append(registro)

    # Converte a lista de dicionários em um DataFrame do pandas
    df = pd.DataFrame(dados_faturas)

    print("Dados extraídos:")
    print(df)

    # Exporta para o arquivo Excel solicitado
    arquivo_saida = "relatorio_faturas.xlsx"
    df.to_excel(arquivo_saida, index=False)
    print(f"\nSucesso! Arquivo '{arquivo_saida}' gerado com sucesso.")


if __name__ == "__main__":
    main()