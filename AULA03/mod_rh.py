def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    return {
        "nome": nome,
        "cargo": cargo,
        "salario": salario
    }

def exibir_colaboradores(lista_colaboradores: list) -> None:
    if not lista_colaboradores:
        print("\nNenhum colaborador cadastrado")
        return

    print("\nColaboradores cadastrados")
    for i, colaborador in enumerate(lista_colaboradores, start=1):
        print(f"{i}. Nome: {colaborador['nome']}")
        print(f"   Cargo: {colaborador['cargo']}")
        print(f"   Salário: {colaborador['salario']:.2f}")