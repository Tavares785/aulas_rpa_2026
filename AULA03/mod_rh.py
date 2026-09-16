# mod_rh.py

def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    """
    Retorna um dicionário estruturado com as chaves 'nome', 'cargo' e 'salario'.
    """
    return {
        "nome": nome,
        "cargo": cargo,
        "salario": salario
    }

def exibir_colaboradores(lista_colaboradores: list) -> None:
    """
    Percorre a lista e imprime os colaboradores de forma formatada.
    """
    if not lista_colaboradores:
        print("\n[AVISO] Nenhum colaborador cadastrado ainda.")
        return

    print("\n" + "=" * 45)
    print(f"{'NOME':<15} | {'CARGO':<15} | {'SALÁRIO':<10}")
    print("=" * 45)
    
    for colab in lista_colaboradores:
        print(f"{colab['nome']:<15} | {colab['cargo']:<15} | R$ {colab['salario']:<.2f}")
        
    print("=" * 45) 