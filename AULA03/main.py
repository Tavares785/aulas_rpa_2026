"""
Script principal: menu interativo para gerenciar colaboradores.
"""

from mod_rh import cadastrar_colaborador, exibir_colaboradores

colaboradores = []

while True:
    print("\n=== Menu RH ===")
    print("1 - Cadastrar colaborador")
    print("2 - Listar colaboradores")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        nome = input("Nome: ").strip()
        cargo = input("Cargo: ").strip()
        salario = float(input("Salário: ").strip())
        colaborador = cadastrar_colaborador(nome, cargo, salario)
        colaboradores.append(colaborador)
        print(f"Colaborador '{nome}' cadastrado com sucesso!")

    elif opcao == "2":
        if not colaboradores:
            print("Nenhum colaborador cadastrado.")
        else:
            exibir_colaboradores(colaboradores)

    elif opcao == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida. Tente novamente.")
