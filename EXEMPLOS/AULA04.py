import pandas as pd
import logging
w = "Olá, mundo!"
try:
    dados = pd.read_csv('arquivos/dados.csv', delimiter=';')
    logging.info(w)
    logging.info(dados.head())
except FileNotFoundError:
    logging.error("Arquivo não encontrado.")
except Exception as e:
    logging.error(f"Ocorreu um erro: {e}")


logging.info("OK O PROCESSO DEU CERTO")