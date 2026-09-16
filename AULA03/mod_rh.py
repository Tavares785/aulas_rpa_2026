def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    """Cria um registro padronizado de colaborador."""
    return {
        "nome": nome,
        "cargo": cargo,
        "salario": salario,
    }


def exibir_colaboradores(lista_colaboradores: list) -> None:
    """Exibe os colaboradores cadastrados."""
    if not lista_colaboradores:
        print("Nenhum colaborador cadastrado.")
        return

    for colaborador in lista_colaboradores:
        print(
            f"Nome: {colaborador['nome']} | "
            f"Cargo: {colaborador['cargo']} | "
            f"Salário: R$ {colaborador['salario']:.2f}"
        )
