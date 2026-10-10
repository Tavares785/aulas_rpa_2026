import pandas as pd

dados = pd.read_csv("./EXEMPLOS/arquivos/dados.csv", delimiter=";")  # Lê o arquivo CSV e cria um DataFrame
print(dados.head())  # Mostra as primeiras linhas do DataFrame