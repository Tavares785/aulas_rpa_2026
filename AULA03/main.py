from mod_rh import cadastrar_colaborador, exibir_colaboradores

colaboradores = []

while True:
    print("1 - Cadastrar")
    print("2 - Listar")
    print("3 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome: ")
        cargo = input("Cargo: ")
        salario = float(input("Salário: "))
        colaborador = cadastrar_colaborador(nome, cargo, salario)
        colaboradores.append(colaborador)
        print("Colaborador cadastrado com sucesso.")
    elif opcao == "2":
        exibir_colaboradores(colaboradores)
    elif opcao == "3":
        print("Sistema encerrado.")
        break
    else:
        print("Opção inválida.")