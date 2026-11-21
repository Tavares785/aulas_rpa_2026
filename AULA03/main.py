from mod_rh import cadastrar_colaborador, exibir_colaboradores


def menu() -> None:
    colaboradores = []
    while True:
        print("\n[1] Cadastrar  [2] Listar  [0] Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            nome = input("Nome: ").strip()
            cargo = input("Cargo: ").strip()
            try:
                salario = float(input("Salário: R$ ").replace(",", "."))
            except ValueError:
                print("Salário inválido. Informe um número.")
                continue
            colaboradores.append(cadastrar_colaborador(nome, cargo, salario))
            print("Colaborador cadastrado.")
        elif opcao == "2":
            exibir_colaboradores(colaboradores)
        elif opcao == "0":
            print("Encerrando.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
