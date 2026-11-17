"""
Lab 11 - Extracao de dados de PDFs com Regex e exportacao para Excel
RA: 6326012

Le as faturas em PDF da pasta faturas/, acha o NIF/CNPJ e o valor total
de cada uma com expressoes regulares e salva tudo em um Excel.
"""
import re
from pathlib import Path

import pandas as pd
import pdfplumber

PASTA_FATURAS = Path(__file__).parent / "faturas"
ARQUIVO_EXCEL = "relatorio_faturas.xlsx"

# CNPJ no formato XX.XXX.XXX/XXXX-XX ou NIF com 9 digitos
REGEX_DOCUMENTO = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\b\d{9}\b"
# linha do total: "Total: 1200.50", "Total a pagar: R$ 1.500,00", "VALOR TOTAL: R$ 3.640,90"
REGEX_TOTAL = r"total[^:\n]*:\s*(?:R\$\s*)?([\d.,]+)"


def ler_texto_pdf(caminho):
    texto = ""
    with pdfplumber.open(caminho) as pdf:
        for pagina in pdf.pages:
            texto += (pagina.extract_text() or "") + "\n"
    return texto


def converter_valor(valor):
    # formato brasileiro (1.500,00) vira 1500.00
    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")
    return float(valor)


def extrair_dados(texto):
    documento = re.search(REGEX_DOCUMENTO, texto)
    total = re.search(REGEX_TOTAL, texto, re.IGNORECASE)
    return {
        "nif_cnpj": documento.group() if documento else "nao encontrado",
        "valor_total": converter_valor(total.group(1)) if total else None,
    }


def main():
    faturas = []
    for caminho in sorted(PASTA_FATURAS.glob("*.pdf")):
        texto = ler_texto_pdf(caminho)
        dados = extrair_dados(texto)
        dados = {"arquivo": caminho.name, **dados}
        print(f"{dados['arquivo']} | {dados['nif_cnpj']} | {dados['valor_total']}")
        faturas.append(dados)

    df = pd.DataFrame(faturas)
    df.to_excel(ARQUIVO_EXCEL, index=False)
    print(f"\n{len(faturas)} faturas processadas. Relatorio salvo em {ARQUIVO_EXCEL}")


if __name__ == "__main__":
    main()
