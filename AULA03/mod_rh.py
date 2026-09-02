"""
Módulo de Recursos Humanos - Cadastro de Colaboradores
"""


def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    """
    Cadastra um colaborador e retorna um dicionário estruturado.
    
    Args:
        nome (str): Nome do colaborador
        cargo (str): Cargo do colaborador
        salario (float): Salário do colaborador
    
    Returns:
        dict: Dicionário contendo os dados do colaborador
    """
    colaborador = {
        "nome": nome,
        "cargo": cargo,
        "salario": salario
    }
    return colaborador


def exibir_colaboradores(lista_colaboradores: list) -> None:
    """
    Exibe todos os colaboradores cadastrados de forma formatada.
    
    Args:
        lista_colaboradores (list): Lista de dicionários com dados dos colaboradores
    """
    if not lista_colaboradores:
        print("\n⚠️  Nenhum colaborador cadastrado.\n")
        return
    
    print("\n" + "=" * 60)
    print("📋 LISTA DE COLABORADORES")
    print("=" * 60)
    
    for idx, colaborador in enumerate(lista_colaboradores, 1):
        print(f"\n{idx}. Nome: {colaborador['nome']}")
        print(f"   Cargo: {colaborador['cargo']}")
        print(f"   Salário: R$ {colaborador['salario']:.2f}")
    
    print("\n" + "=" * 60 + "\n")
