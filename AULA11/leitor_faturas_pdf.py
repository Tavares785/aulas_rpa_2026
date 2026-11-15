
import pdfplumber
import pandas as pd
import re
from pathlib import Path

# Caminho da pasta onde estão os PDFs
pasta = Path(__file__).parent / "faturas"

# Lista para armazenar as informações
lista_faturas = []

# Percorre todos os arquivos PDF da pasta
for arquivo in pasta.glob("*.pdf"):

    with pdfplumber.open(arquivo) as pdf:

        texto_completo = ""

        # Extrai o texto de cada página
        for pagina in pdf.pages:
            texto = pagina.extract_text()

            if texto:
                texto_completo += texto + "\n"

    # Procura NIF ou CNPJ
    padrao_documento = r"\b(?:\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})\b"

    documento = re.search(padrao_documento, texto_completo)

    if documento:
        nif_cnpj = documento.group()
    else:
        nif_cnpj = None

    # Procura o valor total da fatura
    padrao_total = (
        r"(?:total(?:\s+a\s+pagar)?|valor\s+total)"
        r"\s*:?\s*(?:R\$\s*)?"
        r"([\d.]+,\d{2}|\d+\.\d{2})"
    )

    total = re.search(
        padrao_total,
        texto_completo,
        re.IGNORECASE
    )

    if total:
        valor = total.group(1)

        # Converte o valor para número
        if "," in valor:
            valor = valor.replace(".", "").replace(",", ".")

        valor_total = float(valor)
    else:
        valor_total = None

    # Armazena os dados em um dicionário
    dados = {
        "Arquivo": arquivo.name,
        "NIF/CNPJ": nif_cnpj,
        "Valor Total": valor_total
    }

    lista_faturas.append(dados)

# Cria o DataFrame
df = pd.DataFrame(lista_faturas)

# Salva os dados em Excel
df.to_excel(
    Path(__file__).parent / "relatorio_faturas.xlsx",
    index=False
)

print("Relatório gerado com sucesso!")
print(df)
