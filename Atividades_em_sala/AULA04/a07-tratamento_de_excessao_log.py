import pandas as pd
import logging

try:
    dados = pd.read_csv("./EXEMPLOS/arquivos/dados.csv", delimiter=";")  # Lê o arquivo CSV e cria um DataFrame
    print(dados.head())  # Mostra as primeiras linhas do DataFrame
    logging.info(w) # Exemplo para pegar a excessao
    logging.info(dados.head())
except FileNotFoundError: # Captura a exceção de arquivo não encontrado e imprime uma mensagem
    logging.error("Arquivo não encontrado.")
except Exception as e: # Captura qualquer outra exceção e imprime a mensagem de erro
    logging.error(f"Ocorreu um erro: {e}")

