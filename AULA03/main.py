from mod_rh import cadastrar_colaborador, exibir_colaboradores


lista_colaboradores = []


while True:
    print("\n=== SISTEMA DE RH ===")
    print("1 - Cadastrar")
    print("2 - Listar")
    print("0 - Sair")

    opcao = input("Digite uma opção: ")

    if opcao == "1":
        nome = input("Nome do colaborador: ")
        cargo = input("Cargo: ")
        salario = float(input("Salário: "))

        colaborador = cadastrar_colaborador(nome, cargo, salario)
        lista_colaboradores.append(colaborador)

        print("\n[SUCESSO] Colaborador cadastrado!")

    elif opcao == "2":
        exibir_colaboradores(lista_colaboradores)

    elif opcao == "0":
        print("\nEncerrando o sistema...")
        break

    else:
        print("\n[ERRO] Opção inválida.")