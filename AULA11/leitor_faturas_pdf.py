
import pdfplumber
import pandas as pd
import re
import os

# Caminho da pasta com as faturas
PASTA_FATURAS = "AULA11/faturas"

# Lista para armazenar os dados extraídos
dados_faturas = []


def extrair_dados_pdf(caminho_pdf):
    """Extrai CNPJ/NIF e valor total de uma fatura PDF."""

    texto_completo = ""

    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()

                if texto:
                    texto_completo += texto + "\n"

        # Procurando CNPJ ou NIF
        padrao_documento = r'\b(?:\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})\b'
        documentos = re.findall(padrao_documento, texto_completo)

        documento = documentos[0] if documentos else "Não identificado"

        # Procurando valor total
        padrao_valor = (
            r'(?:R\$\s*[\d.]+,\d{2}|'
            r'Total\s*:?\s*[\d.]+[,.]\d{2})'
        )

        valores = re.findall(
            padrao_valor,
            texto_completo,
            flags=re.IGNORECASE
        )

        valor_total = valores[-1] if valores else "Não identificado"

        return {
            "arquivo": os.path.basename(caminho_pdf),
            "cnpj_nif": documento,
            "valor_total": valor_total
        }

    except Exception as erro:
        print(f"Erro ao processar {caminho_pdf}: {erro}")

        return {
            "arquivo": os.path.basename(caminho_pdf),
            "cnpj_nif": "Erro na leitura",
            "valor_total": "Erro na leitura"
        }


def processar_faturas():
    """Percorre os PDFs e gera o relatório Excel."""

    print("Iniciando leitura das faturas...")

    if not os.path.exists(PASTA_FATURAS):
        print("Pasta de faturas não encontrada.")
        return

    arquivos = [
        arquivo
        for arquivo in os.listdir(PASTA_FATURAS)
        if arquivo.lower().endswith(".pdf")
    ]

    if not arquivos:
        print("Nenhum arquivo PDF encontrado.")
        return

    for arquivo in arquivos:
        caminho_pdf = os.path.join(PASTA_FATURAS, arquivo)

        print(f"Processando: {arquivo}")

        resultado = extrair_dados_pdf(caminho_pdf)
        dados_faturas.append(resultado)

    # Criando DataFrame
    df = pd.DataFrame(dados_faturas)

    # Exportando para Excel
    df.to_excel(
        "AULA11/relatorio_faturas.xlsx",
        index=False
    )

    print("\n===== RELATÓRIO DE FATURAS =====")
    print(df.to_string(index=False))

    print("\nRelatório Excel gerado com sucesso!")


if __name__ == "__main__":
    processar_faturas()
