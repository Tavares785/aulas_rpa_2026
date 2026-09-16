def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    """Cria um dicionário com os dados de um colaborador."""
    return {
        "nome": nome,
        "cargo": cargo,
        "salario": float(salario),
    }


def exibir_colaboradores(lista_colaboradores: list) -> None:
    """Imprime os dados dos colaboradores em formato legível."""
    if not lista_colaboradores:
        print("Nenhum colaborador cadastrado.")
        return

    for colaborador in lista_colaboradores:
        print(
            f"Nome: {colaborador['nome']} | "
            f"Cargo: {colaborador['cargo']} | "
            f"Salário: R$ {colaborador['salario']:.2f}"
        )


if __name__ == "__main__":
    colaboradores = []

    while True:
        print("\n=== MENU RH ===")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cargo = input("Cargo: ")
            salario = float(input("Salário: "))
            colaboradores.append(cadastrar_colaborador(nome, cargo, salario))
            print("Colaborador cadastrado com sucesso!")

        elif opcao == "2":
            exibir_colaboradores(colaboradores)

        elif opcao == "0":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")
