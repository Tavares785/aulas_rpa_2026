
from mod_rh import cadastrar_colaborador, exibir_colaboradores


colaboradores = []

while True:
    print("\n=== MENU RH ===")
    print("1 - Cadastrar")
    print("2 - Listar")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome: ")
        cargo = input("Cargo: ")
        salario = float(input("Salário: R$ "))

        colaborador = cadastrar_colaborador(nome, cargo, salario)
        colaboradores.append(colaborador)

        print("Colaborador cadastrado com sucesso!")

    elif opcao == "2":
        if colaboradores:
            exibir_colaboradores(colaboradores)
        else:
            print("Nenhum colaborador cadastrado.")

    elif opcao == "0":
        print("Programa encerrado.")
        break

    else:
        print("Opção inválida. Tente novamente.")
        


