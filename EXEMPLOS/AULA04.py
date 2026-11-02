<<<<<<< HEAD
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
=======
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
>>>>>>> 3c50ef97a60e0cc5dca35bbb5ffd88c2e602b828
