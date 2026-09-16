def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    """Retorna um dicionário estruturado com os dados do colaborador."""
    return {
        "nome": nome,
        "cargo": cargo,
        "salario": salario
    }

def exibir_colaboradores(lista_colaboradores: list) -> None:
    """Percorre a lista e imprime os colaboradores formatados."""
    if not lista_colaboradores:
        print("\nNenhum colaborador cadastrado ainda.")
        return
    
    print("\n--- Lista de Colaboradores ---")
    for i, colab in enumerate(lista_colaboradores, 1):
        print(f"{i}. Nome: {colab['nome']} | Cargo: {colab['cargo']} | Salário: R$ {colab['salario']:.2f}")
    print("-" * 30)