import pdfplumber as pl
import re
import pandas as pd

caminho = "lab-professor/AULA11/espelhos/nota-fiscal-notebook-dell.pdf"
with pl.open(caminho) as pdf:
    x = "\n".join((pagina.extract_text() or "") for pagina in pdf.pages)


padrao = re.compile(r'www\.[\w.-]+\.[a-z]{2,4}/[\w./-]+')
telefone = re.compile(r'\d{4,5}-?\d{4}')

site = re.search(padrao, x)
telefone = re.search(telefone, x)

colunas = ["site", "telefone"]
dado_nota = ((site.group(0), telefone.group(0)), ("www.google.com", "1193221121"))

df = pd.DataFrame(dado_nota, columns=colunas)

df.to_
print(df)