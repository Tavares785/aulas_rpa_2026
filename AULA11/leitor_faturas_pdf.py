import re
from pathlib import Path

import pdfplumber
import pandas as pd


PASTA_FATURAS = Path("AULA11/faturas")
ARQUIVO_EXCEL = "AULA11/relatorio_faturas.xlsx"


def extrair_dados(caminho_pdf):
    texto_completo = ""

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"

    # Localiza CNPJ ou NIF de 9 dígitos
    padrao_nif = r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b|\b\d{9}\b"
    nif = re.search(padrao_nif, texto_completo)

    # Localiza a linha que contém o valor total
    linha_total = re.search(
        r"(?:total(?:\s+a\s+pagar)?|valor\s+total)\s*:?\s*(.*)",
        texto_completo,
        re.IGNORECASE
    )

    valor_total = None

    if linha_total:
        padrao_valor = (
            r"R\$\s*[\d.]+,\d{2}"
            r"|R\$\s*\d+\.\d{2}"
            r"|\b\d{1,3}(?:\.\d{3})*,\d{2}\b"
            r"|\b\d+\.\d{2}\b"
        )
        valor_total = re.search(padrao_valor, linha_total.group(1))

    return {
        "fatura": caminho_pdf.name,
        "nif_cnpj": nif.group() if nif else "Não encontrado",
        "valor_total": valor_total.group() if valor_total else "Não encontrado"
    }


def main():
    resultados = []

    arquivos_pdf = sorted(PASTA_FATURAS.glob("*.pdf"))

    for arquivo in arquivos_pdf:
        try:
            dados = extrair_dados(arquivo)
            resultados.append(dados)
            print(dados)

        except Exception as erro:
            print(f"Erro ao ler {arquivo.name}: {erro}")

    if resultados:
        df = pd.DataFrame(resultados)
        df.to_excel(ARQUIVO_EXCEL, index=False)

        print("\nRelatório gerado com sucesso!")
        print(f"Total de faturas processadas: {len(resultados)}")
        print(f"Arquivo salvo em: {ARQUIVO_EXCEL}")
    else:
        print("Nenhuma fatura foi processada.")


if __name__ == "__main__":
    main()
