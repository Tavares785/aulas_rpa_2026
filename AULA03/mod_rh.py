# mod_rh.py

def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    
    colaborador = {
        "nome": nome,
        "cargo": cargo,
        "salario": salario
    }
    return colaborador

def exibir_colaboradores(lista_colaboradores: list) -> None:
    
    if not lista_colaboradores:
        print("\nNenhum colaborador cadastrado ainda.")
        return

    print("\n--- Lista de Colaboradores ---")
    for i, colab in enumerate(lista_colaboradores, start=1):
        print(f"{i}. Nome: {colab['nome']} | Cargo: {colab['cargo']} | Salário: R$ {colab['salario']:.2f}")
    print("------------------------------")    