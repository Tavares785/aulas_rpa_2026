import glob
import os
import re

import pandas as pd
import pdfplumber

# Pasta onde este script esta (assim funciona de qualquer lugar)
pasta_script = os.path.dirname(os.path.abspath(__file__))
pasta_faturas = os.path.join(pasta_script, "faturas")

# Lista com todos os PDFs da pasta faturas, em ordem
arquivos = sorted(glob.glob(os.path.join(pasta_faturas, "*.pdf")))

dados = []

for caminho in arquivos:
    nome_arquivo = os.path.basename(caminho)

    # 1. Le o texto de todas as paginas do PDF
    pdf = pdfplumber.open(caminho)
    texto = ""
    for pagina in pdf.pages:
        texto_pagina = pagina.extract_text()
        if texto_pagina is not None:
            texto = texto + texto_pagina + "\n"
    pdf.close()

    # 2. Procura o CNPJ no formato XX.XXX.XXX/XXXX-XX
    documento = "NAO ENCONTRADO"
    achou = re.search(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", texto)
    if achou is not None:
        documento = achou.group()
    else:
        # Se nao tem CNPJ, procura o NIF (9 digitos seguidos)
        achou = re.search(r"\b\d{9}\b", texto)
        if achou is not None:
            documento = achou.group()

    # 3. Procura o valor que vem depois da palavra "total"
    valor_total = None
    padrao_total = r"total.*?(\d[\d.]*,\d{2}|\d+\.\d{2})"
    achou = re.search(padrao_total, texto, re.IGNORECASE)
    if achou is not None:
        texto_valor = achou.group(1)
        # Formato brasileiro (1.500,00) vira numero (1500.00)
        if "," in texto_valor:
            texto_valor = texto_valor.replace(".", "")
            texto_valor = texto_valor.replace(",", ".")
        valor_total = float(texto_valor)

    # 4. Guarda os dados desta fatura
    dados.append({
        "arquivo": nome_arquivo,
        "nif_cnpj": documento,
        "valor_total": valor_total,
    })
    print(nome_arquivo, "|", documento, "|", valor_total)

# 5. Converte para tabela e salva em Excel
tabela = pd.DataFrame(dados)
caminho_excel = os.path.join(pasta_script, "relatorio_faturas.xlsx")
tabela.to_excel(caminho_excel, index=False)
print("Excel salvo em:", caminho_excel)
