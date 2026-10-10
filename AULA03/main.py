from mod_rh import cadastrar_colaborador, exibir_colaboradores


def main() -> None:
    colaboradores = []

    while True:
        print("\n1 - Cadastrar")
        print("2 - Listar")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome: ").strip()
            cargo = input("Cargo: ").strip()

            if not nome or not cargo:
                print("Nome e cargo são obrigatórios.")
                continue

            try:
                salario = float(input("Salário: R$ ").strip().replace(",", "."))
            except ValueError:
                print("Informe um salário numérico válido.")
                continue

            if salario <= 0:
                print("O salário deve ser maior que zero.")
                continue

            colaboradores.append(cadastrar_colaborador(nome, cargo, salario))
            print("Colaborador cadastrado com sucesso.")
        elif opcao == "2":
            exibir_colaboradores(colaboradores)
        elif opcao == "0":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()