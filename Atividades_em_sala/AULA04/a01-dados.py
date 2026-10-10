#ler e mostra no csv
'''
Checkout
-b = cria uma branch nova

'''
with open("./EXEMPLOS/arquivos/dados.csv", "r") as arquivo:
    for linha in arquivo:
        print(linha.strip())  # strip() remove espaços em branco e quebras de linha