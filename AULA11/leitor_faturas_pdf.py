
import re
from pathlib import Path

import pdfplumber
import pandas as pd

# Pasta onde estão os PDFs
PASTA_FATURAS = Path(__file__).parent / "faturas"

# Expressões regulares para localizar NIF/CNPJ e valores
PADRAO_DOCUMENTO = re.compile(
    r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b|\b\d{9}\b"
)

PADRAO_VALOR = re.compile(
    r"R\$\s*[\d.]+,\d{2}|\b\d+\.\d{2}\b"
)

def extrair_dados(caminho_pdf):
    """Lê um PDF e extrai o documento fiscal e o valor total."""
    texto = ""

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() or ""
            texto += "\n"

    documento = PADRAO_DOCUMENTO.search(texto)

    # Prioriza o valor que aparece na linha do total
    linha_total = re.search(
        r"(?im)^.*(?:total|valor total|total a pagar).*$",
        texto
    )

    valor = None
    if linha_total:
        resultado_valor = PADRAO_VALOR.search(linha_total.group())
        if resultado_valor:
            valor = resultado_valor.group()

    # Se não encontrar na linha do total, procura no texto inteiro
    if valor is None:
        valores = PADRAO_VALOR.findall(texto)
        if valores:
            valor = valores[-1]

    return {
        "arquivo": caminho_pdf.name,
        "nif_cnpj": documento.group() if documento else "Não identificado",
        "valor_total": valor if valor else "Não identificado"
    }

def main():
    resultados = []

    arquivos_pdf = sorted(PASTA_FATURAS.glob("*.pdf"))

    if not arquivos_pdf:
        print("Nenhum arquivo PDF encontrado na pasta faturas.")
        return

    for arquivo in arquivos_pdf:
        try:
            dados = extrair_dados(arquivo)
            resultados.append(dados)
            print(f"Arquivo processado: {arquivo.name}")
        except Exception as erro:
            print(f"Erro ao processar {arquivo.name}: {erro}")

    if resultados:
        tabela = pd.DataFrame(resultados)
        caminho_excel = Path(__file__).parent / "relatorio_faturas.xlsx"
        tabela.to_excel(caminho_excel, index=False)

        print(f"\nRelatório criado com sucesso: {caminho_excel}")

if __name__ == "__main__":
    main()