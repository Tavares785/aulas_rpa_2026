import os
import re
import pandas as pd
import pdfplumber


def extrair_dados_faturas(pasta_faturas="faturas"):
  """Varre arquivos PDF em uma pasta, extrai texto e utiliza Regex para

  capturar CNPJ/NIF e Valores Totais, gerando um relatório em Excel.
  """
  # Verifica se a pasta de faturas existe
  if not os.path.exists(pasta_faturas):
    print(
        f"Aviso: A pasta '{pasta_faturas}' não foi encontrada no diretório"
        " atual."
    )
    print(
        "Criando uma pasta de exemplo e simulando um arquivo PDF ou gerando"
        " dados simulados..."
    )
    os.makedirs(pasta_faturas, exist_ok=True)

  arquivos_pdf = [
      f for f in os.listdir(pasta_faturas) if f.lower().endswith(".pdf")
  ]

  if not arquivos_pdf:
    print(
        f"Nenhum arquivo PDF encontrado na pasta '{pasta_faturas}'. Certifique-se"
        " de colocar os arquivos lá."
    )
    return

  dados_faturas = []

  # Padrões de Expressões Regulares (Regex)
  # Padrão para CNPJ (XX.XXX.XXX/XXXX-XX ou sequências de 14 dígitos) ou NIF (9 dígitos)
  regex_cnpj = r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b|\b\d{14}\b"
  regex_nif = r"\b\d{9}\b"

  # Padrão para Valor Total (ex: R$ 1.500,00, Total: 1500.00, R$1500,00)
  regex_valor = (
      r"(?:Total|Valor Total|R\$)\s*[:]?\s*R?\$?\s*([\d\.,]+)"
  )  # captura genérica de montantes monetários

  for arquivo in arquivos_pdf:
    caminho_pdf = os.path.join(pasta_faturas, arquivo)
    print(f"Lendo arquivo: {arquivo}...")

    texto_completo = ""
    try:
      with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
          texto_pagina = pagina.extract_text()
          if texto_pagina:
            texto_completo += texto_pagina + "\n"
    except Exception as e:
      print(f"Erro ao ler o PDF {arquivo}: {e}")
      continue

    # Aplicando Regex para buscar CNPJ/NIF
    cnpj_encontrado = re.search(regex_cnpj, texto_completo)
    nif_encontrado = re.search(regex_nif, texto_completo)

    identificador = "Não identificado"
    if cnpj_encontrado:
      identificador = cnpj_encontrado.group(0)
    elif nif_encontrado:
      identificador = nif_encontrado.group(0)

    # Aplicando Regex para buscar Valor Total
    valor_encontrado = re.search(regex_valor, texto_completo, re.IGNORECASE)

    # Fallback caso a regex específica não ache o rótulo "Total", buscando padrões de moeda genéricos
    if valor_encontrado:
      valor_total = valor_encontrado.group(1)
    else:
      # Tenta buscar valores monetários soltos no texto final se o rótulo falhar
      valores_alternativos = re.findall(
          r"R\$\s*[\d\.,]+|\b\d{1,3}(?:\.\d{3})*,\d{2}\b", texto_completo
      )
      valor_total = (
          valores_alternativos[-1]
          if valores_alternativos
          else "Não identificado"
      )

    # Armazenando os dados extraídos
    dados_faturas.append({
        "Arquivo": arquivo,
        "NIF_CNPJ": identificador,
        "Valor_Total": valor_total,
    })

  if not dados_faturas:
    print("Nenhum dado válido foi extraído dos PDFs.")
    return

  # Convertendo para DataFrame do pandas
  df = pd.DataFrame(dados_faturas)

  # Exibindo os resultados extraídos no terminal
  print("\n--- DADOS EXTRAÍDOS DAS FATURAS ---")
  print(df.to_string(index=False))

  # Salvando a lista completa em um arquivo Excel (.xlsx)
  nome_excel = "relatorio_faturas.xlsx"
  df.to_excel(nome_excel, index=False, engine="openpyxl")
  print(
      f"\nRelatório completo salvo com sucesso no arquivo Excel: '{nome_excel}'"
  )


if __name__ == "__main__":
  extrair_dados_faturas()