import pdfplumber as pl
import pandas as pd
import re

padrao_cnpjNIF = re.compile(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\b\d{9}\b)')
padrao_valorTotal = re.compile(r'total\s*:\s*(R\$\s*[\d\.]+,\d{2})', re.IGNORECASE)

faturas = {
'fatura01' : 'AULA10/faturas/fatura_001.pdf',
'fatura02' : 'AULA10/faturas/fatura_002.pdf',
'fatura03' : 'AULA10/faturas/fatura_003.pdf',
'fatura04' : 'AULA10/faturas/fatura_004.pdf',
'fatura05' : 'AULA10/faturas/fatura_005.pdf',
}

dados_extraidos = list()

def extrair_texto(caminho):
    texto_completo = ''
    with pl.open(caminho) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + '\n'
    return texto_completo

for nome_fatura, caminho_pdf in faturas.items():
    try:
        texto_pdf = extrair_texto(caminho_pdf)

        #Busca no texto extraido
        resultadoCPF_NIF = re.search(padrao_cnpjNIF,texto_pdf)
        valor_total = re.search(padrao_valorTotal,texto_pdf)

        #Se encontrar pega o grupo 1, se não, salva como não encontrado
        finalCPF_NIF = resultadoCPF_NIF.group(1) if resultadoCPF_NIF else 'não encontrado'
        valor_final = valor_total.group(1) if valor_total else 'não encontrado'

        #Cria um dicionario para essa fatura especifica e adiciona na lista
        dados_extraidos.append({
            'arquivo': nome_fatura,
            'Documento (CPF/NIF)': finalCPF_NIF,
            'Valor Total': valor_final
        })

        print(f'\033[32mSucesso bb! {nome_fatura} encontrado\033[0m')

    except FileNotFoundError:
        print(f'\033[31mErro: o arquivo {nome_fatura} não foi encontrado no caminho {caminho_pdf}\033[0m')

#só executa se a lista não estiver vazia
if dados_extraidos:
    #1 transforma a lista de dicionáris em um DF 
    df_relatorio = pd.DataFrame(dados_extraidos)

    #2 converte a tabela virtual para um arquivo excel real
    df_relatorio.to_excel('AULA10/faturas/fatura_001.xlsx', index = False)
    print('\n Relátorio criado com sucesso')
    print(df_relatorio)
else:
    print('\nNenhum dado foi extrado, excel não foi gerado')

