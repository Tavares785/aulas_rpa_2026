import os
import re
import pandas as pd
import pdfplumber

diretorio_faturas = "AULA11/faturas"
dados_faturas = []

if os.path.exists(diretorio_faturas):
    for arquivo in os.listdir(diretorio_faturas):
        if arquivo.endswith(".pdf"):
            caminho_pdf = os.path.join(diretorio_faturas, arquivo)
            
            with pdfplumber.open(caminho_pdf) as pdf:
                texto_completo = ""
                for pagina in pdf.pages:
                    texto_extraido = pagina.extract_text()
                    if texto_extraido:
                        texto_completo += texto_extraido + "\n"
            
            match_nif = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\b\d{9}\b', texto_completo)
            match_valor = re.search(r'(?:R\$\s*|Total[:\s]*)([\d\.,]+)', texto_completo, re.IGNORECASE)
            
            nif = match_nif.group(0) if match_nif else "Não encontrado"
            valor = match_valor.group(1) if match_valor else "Não encontrado"
            
            dados_faturas.append({
                "Arquivo": arquivo,
                "NIF_CNPJ": nif,
                "Valor_Total": valor
            })

df = pd.DataFrame(dados_faturas)
df.to_excel("relatorio_faturas.xlsx", index=False)
