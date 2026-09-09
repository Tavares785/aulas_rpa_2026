#lab-03

def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:

    colaborador = {
        "nome": nome,
        "cargo": cargo,
        "salario": salario
    }
    return colaborador


def exibir_colaboradores(lista_colaboradores: list) -> None:

    if not lista_colaboradores:
        print("Nenhum colaborador.\n\n")
        return

    print("Lista de colaboradores:\n")
    for i, colab in enumerate(lista_colaboradores, start = 1):
        print(f"{i}. Nome: {colab['nome']} \n Cargo: {colab['cargo']} \n Salário: {colab['salario']:.2f}" )
        print("---\n")
