def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    """Retorna um dicionário estruturado com as chaves nome, cargo e salario."""
    colaborador = {
        "nome": nome,
        "cargo": cargo,
        "salario": salario
    }
    return colaborador


def exibir_colaboradores(lista_colaboradores: list) -> None:
    """Percorre a lista e imprime os colaboradores formatados."""
    if not lista_colaboradores:
        print("\n⚠️ Nenhum colaborador cadastrado ainda.")
        return

    print("\n--- 📋 Lista de Colaboradores ---")
    for idx, colab in enumerate(lista_colaboradores, start=1):
        print(f"{idx}. Nome: {colab['nome']} | Cargo: {colab['cargo']} | Salário: R$ {colab['salario']:.2f}")
    print("---------------------------------")
