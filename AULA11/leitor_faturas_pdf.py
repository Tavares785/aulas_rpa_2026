import os
import re
import glob
import pdfplumber
import pandas as pd

def criar_pdf_exemplo_se_vazio(pasta):
    """Cria um PDF de fatura simulado caso não haja nenhum PDF na pasta."""
    arquivos_existentes = glob.glob(os.path.join(pasta, "*.pdf"))
    if not arquivos_existentes:
        caminho_pdf = os.path.join(pasta, "fatura_exemplo_01.pdf")
        # Estrutura mínima válida de um arquivo PDF com texto extraível
        conteudo_texto = b"FATURA DE SERVICOS - Fornecedor Tech LTDA - CNPJ: 12.345.678/0001-99 - Data: 12/11/2026 - Valor Total: R$ 1.500,00"
        stream = b"BT /F1 12 Tf 50 750 Td (" + conteudo_texto + b") Tj ET"
        
        objs = [
            b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
            b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
            b"3 0 obj << /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >> endobj\n",
            b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
            f"5 0 obj << /Length {len(stream)} >> stream\n".encode() + stream + b"\nendstream endobj\n"
        ]
        
        pdf_bytes = b"%PDF-1.4\n"
        offsets = []
        for obj in objs:
            offsets.append(len(pdf_bytes))
            pdf_bytes += obj
            
        xref_pos = len(pdf_bytes)
        pdf_bytes += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode()
        for off in offsets:
            pdf_bytes += f"{off:010d} 00000 n \n".encode()
        pdf_bytes += f"trailer << /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode()
        
        with open(caminho_pdf, "wb") as f:
            f.write(pdf_bytes)
        print(f"Nenhum PDF encontrado. Arquivo de teste criado: {caminho_pdf}")

# 1. Define a pasta onde o script está (AULA11)
pasta_script = os.path.dirname(os.path.abspath(__file__))

# Garante que exista pelo menos 1 PDF na pasta para testar
criar_pdf_exemplo_se_vazio(pasta_script)

# 2. Localiza todos os arquivos .pdf na pasta
arquivos_pdf = glob.glob(os.path.join(pasta_script, "*.pdf"))

# Expressões Regulares (Regex)
# CNPJ (XX.XXX.XXX/XXXX-XX) ou NIF (9 dígitos seguidos)
padrao_nif_cnpj = r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\b\d{9}\b)"

# Valor monetário: captura formatos como "R$ 1.500,00" ou "Total: 1500.00"
padrao_valor = r"(?:R\$\s*|Total:\s*)(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})"

dados_faturas = []

# 3. Lê cada PDF e extrai os padrões
for caminho_pdf in arquivos_pdf:
    nome_arquivo = os.path.basename(caminho_pdf)
    texto_completo = ""
    
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
                
    # Aplica os filtros Regex no texto extraído
    match_doc = re.search(padrao_nif_cnpj, texto_completo)
    match_valor = re.search(padrao_valor, texto_completo, re.IGNORECASE)
    
    nif_cnpj = match_doc.group(1) if match_doc else "Não encontrado"
    valor_total = match_valor.group(1) if match_valor else "Não encontrado"
    
    dados_faturas.append({
        "arquivo": nome_arquivo,
        "nif_cnpj": nif_cnpj,
        "valor_total": valor_total
    })

# 4. Converte para DataFrame do pandas e exporta para Excel
df = pd.DataFrame(dados_faturas)

print("\n--- DADOS EXTRAÍDOS DAS FATURAS ---")
print(df)

caminho_excel = os.path.join(pasta_script, "relatorio_faturas.xlsx")
df.to_excel(caminho_excel, index=False)

print(f"\nSucesso! Relatório salvo em '{caminho_excel}'.")