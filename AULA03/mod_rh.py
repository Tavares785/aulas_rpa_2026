def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:

    colaborador = {
        "nome": nome,
        "cargo": cargo,
        "salario": salario
    }
    return colaborador
 
 
def exibir_colaboradores(lista_colaboradores: list) -> None:
 
    if not lista_colaboradores:
        print("\nNenhum colaborador cadastrado.\n")
        return
 
    print("\n" + "=" * 40)
    print("LISTA DE COLABORADORES")
    print("=" * 40)
    for indice, colaborador in enumerate(lista_colaboradores, start=1):
        print(f"{indice}. Nome: {colaborador['nome']}")
        print(f"   Cargo: {colaborador['cargo']}")
        print(f"   Salário: R$ {colaborador['salario']:.2f}")
        print("-" * 40)
    print()
 