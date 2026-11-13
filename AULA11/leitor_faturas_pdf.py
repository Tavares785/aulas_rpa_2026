import pdfplumber
import os
import re
import pandas as pd


with pdfplumber.open("faturas/fatura_001.pdf") as pdf:
    pagina = pdf.pages[0]
    texto_bruto = pagina.extract_text()

faturas = []
os.listdir("/home/cadoni/Desktop/RPA/aulas_rpa_2026/AULA11/faturas")
padrao_nif = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
padrao_dinheiro = r'R\$\s*[\d\.]+,\d{2}'

resultado_nif = re.search(padrao_nif, texto_bruto)
resultado_valor = re.search(padrao_dinheiro, texto_bruto)

valor = resultado_valor.group() if resultado_valor else "Nao enc"
nif = resultado_nif.group() if resultado_nif else "Nao encontrado"


faturas.append({
    "arquivo": "fatura_001.pdf",
    "nif": nif,
    "valor total": valor
}) 

df = pd.DataFrame(faturas)
df.to_excel("/home/cadoni/Desktop/RPA/aulas_rpa_2026/AULA11/relatorio_faturas.xlsx",index = False)
  