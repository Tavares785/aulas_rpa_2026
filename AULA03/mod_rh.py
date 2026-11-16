def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    return {
        "nome": nome,
        "cargo": cargo,
        "salario": salario
    }


def exibir_colaboradores(lista_colaboradores: list) -> None:
    for colaborador in lista_colaboradores:
        print(f"Nome: {colaborador['nome']}")
        print(f"Cargo: {colaborador['cargo']}")
        print(f"Salário: R$ {colaborador['salario']:.2f}")
        print("-" * 30)
        
    





