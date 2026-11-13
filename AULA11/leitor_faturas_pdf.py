import pdfplumber
import os
import re
import pandas as pd

def buscar_identificacao(texto_bruto):
    padrao_nif = r'\d{9}'
    padrao_cpf = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
    indentificacao = re.search(padrao_nif,texto_bruto)
    
    if indentificacao == None:
        indentificacao = re.search(padrao_cpf,texto_bruto)
    
    indentificacao = indentificacao.group() if indentificacao else "Nao encontrado"
    return indentificacao


def valor_total(texto_bruto):
    padrao_real = r'R\$\s*[\d\.]+,\d{2}'
    padrao_total = r'\d{3}\.\d{2}'
    valor = re.search(padrao_real, texto_bruto)
    if valor == None:
        valor = re.search(padrao_total,texto_bruto)
    valor = valor.group() if valor else "Nao encontrado"
    return valor

quantidade_pdf = os.listdir("/home/cadoni/Desktop/RPA/aulas_rpa_2026/AULA11/faturas")
faturas = []

for pdf_atual in range(len(quantidade_pdf)):
    pdf_atual += 1  
    with pdfplumber.open(f"faturas/fatura_00{pdf_atual}.pdf") as pdf:
        pagina = pdf.pages[0]
        texto_bruto = pagina.extract_text()
    
    indentificacao = buscar_identificacao(texto_bruto)
    valor = valor_total(texto_bruto)

    faturas.append({
        "arquivo": f"fatura_00{pdf_atual}.pdf",
        "cpf/nif": indentificacao,
        "valor total": valor
    })
    if indentificacao == "Nao encontrado":
        print(f'pdf:fatura:00{pdf_atual} cpf ou nif nao encontrado')
    if valor == 'Nao encontrado':
        print(f'pdf:fatura:00{pdf_atual} Valor nao encontrado')
    else:
        print(f'fatura:{pdf_atual} Arquivo adicionado com sucesso')    

df = pd.DataFrame(faturas)
df.to_excel("/home/cadoni/Desktop/RPA/aulas_rpa_2026/AULA11/relatorio_faturas.xlsx",index = False)
