import mod_rh as rh


colaboradores = []
while True:

    print("Escolha uma opção:")
    print("1 - Cadastrar")
    print("2 - Listar")
    print("0 - Sair")

    try:
        opcao = int(input("Escolha uma opção: "))
    except ValueError:
        print("Digite apenas as opção do menu !")
        print("-" * 60)
        continue

    print("-"*60)
    if opcao == 0:
        break
    elif opcao == 1:
        nome = input("Digite o nome do colaborador: ")
        cargo = input("Digite o nome do cargo: ")
        while True:
            try:
                salario = float(input("Digite o salário: "))
                break
            except ValueError:
                print("Digite um valor numérico válido !")
                print("-"*60)

        colaboradores.append(rh.cadastrar_colaborador(nome, cargo, salario))
        print("-"*60)
    elif opcao == 2:
        rh.exibir_colaboradores(colaboradores)
        print("-"*60)
    else:
        print("Opção Inválida !")
