import pandas as pd

try:
    dados = pd.read_csv("./EXEMPLOS/arquivos/dados.csv", delimiter=";")  # Lê o arquivo CSV e cria um DataFrame
    print(dados.head())  # Mostra as primeiras linhas do DataFrame
    print(w) # Exemplo para pegar a excessao
except FileNotFoundError: # Captura a exceção de arquivo não encontrado e imprime uma mensagem
    print("Arquivo não encontrado.")
except Exception as e: # Captura qualquer outra exceção e imprime a mensagem de erro
    print(f"Ocorreu um erro: {e}")
raise w != "Olá mundo!" # Exemplo para pegar a excessao
print("Fim do programa.")
