import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)

w = "Olá, mundo!"
try:
    dados = pd.read_csv('./arquivos/dados.csv', delimiter=';')
    logging.info(w)
    logging.info(dados.head())
except FileNotFoundError:
    logging.error("Arquivo não encontrado.")
