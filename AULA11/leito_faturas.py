import os
import re
import pdfplumber
import pandas as pd

# Pasta onde estão os PDFs
import os

PASTA_FATURAS = os.path.join(
    os.path.dirname(__file__),
    "faturas"
)

# Lista que armazenará os dados extraídos
faturas = []

# Regex para CNPJ
regex_cnpj = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"

# Regex para o valor total da fatura
regex_total = (
    r"(?:Total a pagar|Total|Valor Total|TOTAL)"
    r"\s*:\s*"
    r"(R\$\s?[\d\.]+,\d{2}|[\d\.]+\.\d{2})"
)

# Percorre todos os arquivos da pasta
for arquivo in os.listdir(PASTA_FATURAS):

    if arquivo.lower().endswith(".pdf"):

        caminho_pdf = os.path.join(PASTA_FATURAS, arquivo)

        print(f"Lendo arquivo: {arquivo}")

        texto_completo = ""

        try:
            with pdfplumber.open(caminho_pdf) as pdf:

                for pagina in pdf.pages:

                    texto = pagina.extract_text()

                    if texto:
                        texto_completo += texto + "\n"

            # Procura os dados no texto
            cnpj = re.search(regex_cnpj, texto_completo)
            total = re.search(
    regex_total,
    texto_completo,
    re.IGNORECASE
)

            faturas.append({
                "arquivo": arquivo,
                "cnpj": cnpj.group() if cnpj else "Não encontrado",
                "valor_total": total.group(1) if total else "Não encontrado"
            })

        except Exception as erro:
            print(f"Erro ao processar {arquivo}: {erro}")

# Cria DataFrame
df = pd.DataFrame(faturas)

# Exibe os resultados
print("\nDados Encontrados:")
print(df)

# Exporta para Excel
df.to_excel(
    "relatorio_faturas.xlsx",
    index=False
)

print("\nRelatório Excel criado com sucesso!")
print(f"Total de faturas processadas: {len(df)}")

print("\n--- TEXTO EXTRAÍDO ---")
print(texto_completo)
print("----------------------\n")

print(f"\n{'='*50}")
print(f"ARQUIVO: {arquivo}")
print(f"{'='*50}")
print(texto_completo)
print(f"{'='*50}\n")