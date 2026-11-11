def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    return {"nome": nome, "cargo": cargo, "salario": salario}

def exibir_colaboradores(lista_colaboradores: list) -> None:
    if not lista_colaboradores:
        print("\n[AVISO] Nenhum colaborador cadastrado ainda.")
        return
    print("\n--- Lista de Colaboradores ---")
    for colab in lista_colaboradores:
        print(f"Nome: {colab['nome']} | Cargo: {colab['cargo']} | Salário: R$ {colab['salario']:.2f}")
    print("------------------------------\n")