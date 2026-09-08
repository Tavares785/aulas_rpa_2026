from mod_rh import cadastrar_colaborador, exibir_colaboradores


lista_colaboradores = []

while True:
    print("\n=== SISTEMA DE RH ===")
    print("1 - Cadastrar")
    print("2 - Listar")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome: ")
        cargo = input("Cargo: ")
        salario = float(input("Salário: "))

        colaborador = cadastrar_colaborador(nome, cargo, salario)
        lista_colaboradores.append(colaborador)

        print("Colaborador cadastrado com sucesso!")

    elif opcao == "2":
        if lista_colaboradores:
            exibir_colaboradores(lista_colaboradores)
        else:
            print("Nenhum colaborador cadastrado.")

    elif opcao == "0":
        print("Sistema encerrado.")
        break

    else:
        print("Opção inválida.")