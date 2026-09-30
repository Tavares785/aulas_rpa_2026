def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    colaborador = {
        'nome': nome,
        'cargo': cargo,
        'salario': salario
    }
    return colaborador


def exibir_colaboradores(lista_colaboradores: list) -> None:
    print("\nLista de colaboradores:")
    if not lista_colaboradores:
        print('Nenhum colaborador cadastrado.')
    else:
        for idx, colab in enumerate(lista_colaboradores, start=1):
            print(f"{idx}. Nome: {colab['nome']} | Cargo: {colab['cargo']} | Salário: R$ {colab['salario']:.2f}")