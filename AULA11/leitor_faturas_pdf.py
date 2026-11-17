import re
from pathlib import Path
import pandas as pd
import pdfplumber


def formatar_padrao_brasileiro(valor_str):
    """Padroniza qualquer string numérica para o formato monetário brasileiro:

    ex: 1200.50 ou 1.500,00 -> 1.200,50 ou 1.500,00
    """
    if not valor_str:
        return None

    # Remove caracteres indesejados mantendo apenas dígitos, vírgulas e pontos
    limpo = re.sub(r'[^\d,\.]', '', valor_str)
    if not limpo:
        return None

    # Trata separadores de milhar e decimal
    if ',' in limpo and '.' in limpo:
        if limpo.rfind(',') > limpo.rfind('.'):
            num_str = limpo.replace('.', '').replace(',', '.')
        else:
            num_str = limpo.replace(',', '')
    elif ',' in limpo:
        num_str = limpo.replace('.', '').replace(',', '.')
    else:
        num_str = limpo

    try:
        numero = float(num_str)
        return f"{numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except ValueError:
        return valor_str


def extrair_dados_fatura(caminho_pdf):
    dados_fatura = {
        "Arquivo": Path(caminho_pdf).name,
        "NIF_CNPJ": None,
        "Valor_Total": None
    }
    
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
                
    # 1. Extração de NIF (9 dígitos) ou CNPJ (XX.XXX.XXX/XXXX-XX)
    padrao_cnpj = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
    padrao_nif = r'\b\d{9}\b'
    
    match_cnpj = re.search(padrao_cnpj, texto_completo)
    if match_cnpj:
        dados_fatura["NIF_CNPJ"] = match_cnpj.group(0)
    else:
        match_nif = re.search(padrao_nif, texto_completo)
        if match_nif:
            dados_fatura["NIF_CNPJ"] = match_nif.group(0)
            
    # 2. Extração de Valor Total
    # Procura por linhas contendo palavras-chave de totalização
    linhas = texto_completo.split('\n')
    valor_encontrado = None
    
    for linha in reversed(linhas):  # Geralmente o total fica no final da fatura
        if re.search(r'total|pagar|montante', linha, re.IGNORECASE):
            # Extrai valores monetários da linha
            valores_linha = re.findall(r'(?:R\$\s*)?([\d\.]+,\d{2}|\d+\.\d{2})', linha)
            if valores_linha:
                valor_encontrado = valores_linha[-1]
                break
                
    # Fallback caso não ache na linha com palavra-chave: pega o último valor válido do documento
    if not valor_encontrado:
        todos_valores = re.findall(r'(?:R\$\s*)?([\d\.]+,\d{2}|\d+\.\d{2})', texto_completo)
        if todos_valores:
            valor_encontrado = todos_valores[-1]
            
    if valor_encontrado:
        dados_fatura["Valor_Total"] = formatar_padrao_brasileiro(valor_encontrado)
        
    return dados_fatura


def main():
    diretorio_faturas = Path("faturas")
    if not diretorio_faturas.exists():
        diretorio_faturas = Path(".")

    faturas = list(diretorio_faturas.glob("*.pdf"))
    
    if not faturas:
        print("Aviso: Nenhum arquivo PDF encontrado na pasta de faturas.")
        return

    resultados = [extrair_dados_fatura(f) for f in faturas]
        
    df = pd.DataFrame(resultados)
    df.to_excel("relatorio_faturas.xlsx", index=False)
    print("Sucesso: Relatório gerado e padronizado em 'relatorio_faturas.xlsx'.")


if __name__ == "__main__":
    main()
