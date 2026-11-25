
import logging
import re
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pdfplumber


PASTA_FATURAS = Path(__file__).resolve().parent / "faturas"
ARQUIVO_EXCEL = Path(__file__).resolve().parent / "relatorio_faturas.xlsx"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def extrair_texto(caminho_pdf):
    """Extrai o texto de todas as páginas de um PDF."""
    textos = []

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()

            if texto:
                textos.append(texto)

    return "\n".join(textos)


def extrair_dados(texto, nome_arquivo):
    """Localiza fornecedor, documento, data e valor usando Regex."""

    fornecedor = re.search(
        r"(?:Fornecedor|Raz[aã]o Social):\s*(.+)",
        texto,
        re.IGNORECASE
    )

    documento = re.search(
        r"(?:CNPJ|NIF):\s*"
        r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})",
        texto,
        re.IGNORECASE
    )

    data = re.search(
        r"(?:Emiss[aã]o|Data):\s*(\d{2}/\d{2}/\d{4})",
        texto,
        re.IGNORECASE
    )

    total = re.search(
        r"(?:VALOR\s+TOTAL|TOTAL(?:\s+A\s+PAGAR)?)"
        r"\s*:?\s*(?:R\$\s*)?"
        r"([\d.]+,\d{2}|\d+\.\d{2})",
        texto,
        re.IGNORECASE
    )

    valor_total = None

    if total:
        valor = total.group(1)

        if "," in valor:
            valor = valor.replace(".", "").replace(",", ".")

        valor_total = float(Decimal(valor))

    return {
        "arquivo": nome_arquivo,
        "fornecedor": fornecedor.group(1).strip()
        if fornecedor else "Não identificado",
        "documento": documento.group(1)
        if documento else "Não identificado",
        "data_emissao": data.group(1)
        if data else "Não identificada",
        "valor_total": valor_total
    }


def salvar_excel(dados):
    """Organiza os dados e exporta para Excel."""

    df = pd.DataFrame(dados)

    with pd.ExcelWriter(ARQUIVO_EXCEL, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Relatorio"
        )

        planilha = writer.sheets["Relatorio"]
        planilha.column_dimensions["A"].width = 22
        planilha.column_dimensions["B"].width = 38
        planilha.column_dimensions["C"].width = 25
        planilha.column_dimensions["D"].width = 20
        planilha.column_dimensions["E"].width = 18

        for celula in planilha["E"][1:]:
            celula.number_format = '"R$" #,##0.00'

    logging.info("Relatório Excel salvo em: %s", ARQUIVO_EXCEL)


def main():
    logging.info("Iniciando leitura das faturas PDF.")

    arquivos_pdf = sorted(PASTA_FATURAS.glob("*.pdf"))

    if not arquivos_pdf:
        logging.warning("Nenhum arquivo PDF encontrado na pasta faturas.")
        return

    dados_faturas = []

    for arquivo in arquivos_pdf:
        try:
            logging.info("Lendo arquivo: %s", arquivo.name)

            texto = extrair_texto(arquivo)

            dados = extrair_dados(texto, arquivo.name)

            dados_faturas.append(dados)

        except Exception:
            logging.exception(
                "Erro ao processar o arquivo %s",
                arquivo.name
            )

    if not dados_faturas:
        logging.warning("Nenhuma fatura foi processada.")
        return

    salvar_excel(dados_faturas)

    print("\n===== RELATÓRIO DE FATURAS =====")

    for fatura in dados_faturas:
        print(f"\nArquivo: {fatura['arquivo']}")
        print(f"Fornecedor: {fatura['fornecedor']}")
        print(f"Documento: {fatura['documento']}")
        print(f"Data: {fatura['data_emissao']}")
        print(f"Valor total: {fatura['valor_total']}")

    logging.info(
        "Processamento concluído. Total de faturas: %s",
        len(dados_faturas)
    )


if __name__ == "__main__":
    main()
