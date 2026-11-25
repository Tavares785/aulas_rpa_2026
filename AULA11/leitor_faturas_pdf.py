
import re
import pdfplumber
import pandas as pd
from pathlib import Path


# Caminho da pasta onde estão as faturas
PASTA_FATURAS = Path(__file__).parent / "faturas"

# Lista que armazenará os dados extraídos
faturas_extraidas = []


def extrair_dados_pdf(caminho_pdf):
    """
    Lê todas as páginas de um PDF e extrai
    NIF/CNPJ, valor total e data.
    """

    texto_completo = ""

    try:
        with pdfplumber.open(caminho_pdf) as pdf:

            for pagina in pdf.pages:
                texto = pagina.extract_text()

                if texto:
                    texto_completo += texto + "\n"

        # Expressão regular para CNPJ
        regex_cnpj = (
            r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"
        )

        # Expressão regular para NIF de 9 dígitos
        regex_nif = r"\b\d{9}\b"

        # Procura primeiro o CNPJ
        resultado_nif = re.search(
            regex_cnpj, texto_completo
        )

        if not resultado_nif:
            resultado_nif = re.search(
                regex_nif, texto_completo
            )

        nif_cnpj = (
            resultado_nif.group()
            if resultado_nif
            else "Não encontrado"
        )

        # Expressão regular para valores monetários
        regex_valor = (
            r"(?:valor\s+total|total)\s*[:\-]?\s*"
            r"(R\$\s*[\d.]+,\d{2}|[\d.]+,\d{2}|"
            r"\d+(?:\.\d{2})?)"
            r"|"
            r"(R\$\s*[\d.]+,\d{2})"
        )

        resultado_valor = re.search(
            regex_valor,
            texto_completo,
            re.IGNORECASE
        )

        if resultado_valor:
            valor_total = (
                resultado_valor.group(1)
                or resultado_valor.group(2)
            )
        else:
            valor_total = "Não encontrado"

        # Expressão regular para datas
        regex_data = (
            r"\b\d{2}/\d{2}/\d{4}\b"
        )

        resultado_data = re.search(
            regex_data, texto_completo
        )

        data = (
            resultado_data.group()
            if resultado_data
            else "Não encontrada"
        )

        # Dicionário com os dados da fatura
        dados_fatura = {
            "Arquivo": caminho_pdf.name,
            "NIF/CNPJ": nif_cnpj,
            "Valor Total": valor_total,
            "Data": data
        }

        print(f"Fatura processada: {caminho_pdf.name}")

        return dados_fatura

    except Exception as erro:
        print(f"Erro ao ler {caminho_pdf.name}: {erro}")
        return None


def main():

    print("=" * 50)
    print("   ROBÔ DE EXTRAÇÃO DE FATURAS EM PDF")
    print("=" * 50)

    # Verifica se a pasta existe
    if not PASTA_FATURAS.exists():
        print("A pasta de faturas não foi encontrada!")
        return

    # Localiza todos os arquivos PDF
    arquivos_pdf = list(PASTA_FATURAS.glob("*.pdf"))

    if not arquivos_pdf:
        print("Nenhum arquivo PDF encontrado na pasta.")
        return

    print(f"\nTotal de PDFs encontrados: {len(arquivos_pdf)}")

    # Processa cada arquivo PDF
    for arquivo in arquivos_pdf:

        dados = extrair_dados_pdf(arquivo)

        if dados:
            faturas_extraidas.append(dados)

    # Cria o DataFrame
    df = pd.DataFrame(
        faturas_extraidas,
        columns=[
            "Arquivo",
            "NIF/CNPJ",
            "Valor Total",
            "Data"
        ]
    )

    # Exporta os dados para Excel
    caminho_excel = (
        Path(__file__).parent / "relatorio_faturas.xlsx"
    )

    df.to_excel(
        caminho_excel,
        index=False,
        engine="openpyxl"
    )

    print("\n" + "=" * 50)
    print("PROCESSAMENTO FINALIZADO!")
    print("=" * 50)

    print("\nDados extraídos:")
    print(df.to_string(index=False))

    print(f"\nRelatório salvo em: {caminho_excel}")


if __name__ == "__main__":
    main()
