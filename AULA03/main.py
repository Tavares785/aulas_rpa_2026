from rod_rh import cadastrar_colaborador, exibir_colaboradores


lista_colaboradores = []


while True:
    print("\n===== SISTEMA DE RH =====")
    print("1 - Cadastrar")
    print("2 - Listar")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        print("\n===== CADASTRAR COLABORADOR =====")

        nome = input("Digite o nome: ")
        cargo = input("Digite o cargo: ")

        while True:
            try:
                salario = float(input("Digite o salário: "))
                break
            except ValueError:
                print("Digite um salário válido.")

        colaborador = cadastrar_colaborador(nome, cargo, salario)

        lista_colaboradores.append(colaborador)

        print("\nColaborador cadastrado com sucesso!")

    elif opcao == "2":
        exibir_colaboradores(lista_colaboradores)

    elif opcao == "0":
        print("\nPrograma encerrado.")
        break

    else:
        print("\nOpção inválida!")