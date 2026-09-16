import logging
import pandas as pd
w = "%(asctime)s - %(levelname)s - %(message)s"
try:
    dados = pd.read_csv('AULA04/Dados.csv', delimiter=';')
    logging.info(w)
    logging.info(dados.head())
except FileNotFoundError:
    logging.error("Arquivo não encontrado.")
except Exception as e:
    logging.error(f"Ocorreu um erro: {e}")
finally:
    logging.info("OK O PROCESSO DEU CERTO")