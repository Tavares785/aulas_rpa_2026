from mod_rh import cadastrar_colaborador, exibir_colaboradores

colaboradores = []

while True:
    opcao = input("\n1 - Cadastrar\n2 - Listar\n0 - Sair\nOpção: ")

    if opcao == "1":
        nome = input("Nome: ")
        cargo = input("Cargo: ")
        salario = float(input("Salário: "))
        
        colab = cadastrar_colaborador(nome, cargo, salario)
        colaboradores.append(colab)
        print("Cadastrado!")

    elif opcao == "2":
        exibir_colaboradores(colaboradores)

    elif opcao == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida!")