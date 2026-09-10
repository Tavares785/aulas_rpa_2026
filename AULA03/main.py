from mod_rh import cadastrar_colaborador, exibir_colaboradores

lista_colaboradores = []

while True:
    print("Menu de RH:")
    print("1 - Cadastrar")
    print("2 - Listar")
    print("0 - Sair")
    opcao = input("Digite a opção: ")
    if opcao == "1":
        nome = input("Digite o nome: ")
        cargo = input("Digite o cargo: ")
        salario = float(input("Digite o salário: "))
        lista_colaboradores.append(cadastrar_colaborador(nome, cargo, salario))
    elif opcao == "2":
        exibir_colaboradores(lista_colaboradores)
    elif opcao == "0":
        break
