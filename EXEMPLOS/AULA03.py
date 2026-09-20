lista = [1, 2, 3, 4, 5]
lista.append(6)

tupla = (1, 2, 3, 4, 5)
tupla[0] = 6  # ERRO: tuplas sao imutaveis

dicionario = {"nome": "Joao", "idade": 30}
dicionario["idade"] = 31  # OK: dicionarios sao mutaveis
print(dicionario["idade"])  # imprime 31]



def saudacoes(nome):
    """Retorna uma saudacao personalizada."""
    return f"Olá, {nome}!"

sd = saudacoes("Maria")  # retorna "Olá, Maria!"
print(sd)  # imprime "Olá, Maria!"


def funcao_dinamica(*args, **kwargs):
    """Exemplo de funcao que aceita argumentos dinamicos."""
    print("Posicionais:", args)
    print("Nomeados:", kwargs)
    print("Primeiro posicional:", args[0] if args else None)
    print("Valor de 'chave1':", kwargs.get("chave1"))

funcao_dinamica(1, 2, 3, chave1="valor1", chave2="valor2")


def funcao_input():
    """Exemplo de funcao que recebe input do usuario."""
    nome = input("Digite seu nome: ")
    idade = int(input("Digite sua idade: "))
    print(f"Nome: {nome}, Idade: {idade}")

funcao_input()



import pandas as pd
df = pd.read_csv("dados.csv")  # Lendo um arquivo CSV
print(df.head())  # Mostrando as primeiras linhas do DataFrame


cliente = {}
def menu():
    """Exemplo de menu interativo."""
    while True:
        print("Menu:")
        print("1. Cadastrar usuario")
        print("2. Atualizar usuario")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            cliente["nome"] = input("Digite o nome do usuario: ")
            cliente["idade"] = int(input("Digite a idade do usuario: "))
            print("Usuario cadastrado com sucesso!")
        elif escolha == "2":
            if cliente:
                cliente["nome"] = input("Digite o novo nome do usuario: ")
                cliente["idade"] = int(input("Digite a nova idade do usuario: "))
                print("Usuario atualizado com sucesso!")
            else:
                print("Nenhum usuario cadastrado.")
        elif escolha == "3":
            print("Saindo do menu.")
            break
        else:
            print("Opção inválida. Tente novamente.")