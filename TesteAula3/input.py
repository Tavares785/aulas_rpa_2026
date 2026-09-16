def menu(opcao):
    print("1. opcao1")
    print("2. opcao2")

op=input ("Escolha uma opção: ")

if op=="1":
    nome=input("Digite seu nome: ")
    idade=int(input("Digite sua idade: "))
    email=input("Digite seu email: ")
    print(f"Usuário {nome} cadastrado com sucesso!")