#lab-03

from mod_rh import cadastrar_colaborador, exibir_colaboradores

def main():

    base_colaboradores = []

    while True:
        print("\nMENU: ")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\nCadastro")
            nome = input("Nome: ")
            cargo = input("Cargo: ")
            salario = float(input("Salário: "))

            novo_colaborador = cadastrar_colaborador(nome, cargo, salario)

            base_colaboradores.append(novo_colaborador)
            print("\nCadastrado com sucesso.\n")

        elif opcao == "2":
            print("\n")
            exibir_colaboradores(base_colaboradores)

        elif opcao == "0":
            print("\n\nSaindo...\n\n")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()