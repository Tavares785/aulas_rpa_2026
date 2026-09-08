def cadastrar_colaborador(
        nome: str, 
        cargo: str, 
        salario: float) -> dict:
    return {"nome": nome, "cargo": cargo, "salario": salario}

def exibir_colaboradores(lista_colaboradores: list) -> None:
    if not lista_colaboradores:
        print("Nenhum colaborador cadastrado.")
        return

    for c in lista_colaboradores:
        print(f"Nome: {c['nome']} | Cargo: {c['cargo']} | Salário: R$ {c['salario']:.2f}")