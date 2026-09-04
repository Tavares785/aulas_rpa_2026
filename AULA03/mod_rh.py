"""
Módulo de RH: funções para cadastro e exibição de colaboradores.
"""


def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    """Retorna um dicionário estruturado com os dados do colaborador."""
    return {
        "nome": nome,
        "cargo": cargo,
        "salario": salario,
    }


def exibir_colaboradores(lista_colaboradores: list) -> None:
    """Percorre a lista e imprime os colaboradores formatados."""
    for colaborador in lista_colaboradores:
        print(
            f"Nome: {colaborador['nome']} | "
            f"Cargo: {colaborador['cargo']} | "
            f"Salário: R$ {colaborador['salario']:.2f}"
        )
