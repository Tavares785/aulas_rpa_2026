def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    """Estrutura os dados do colaborador em um dicionário padronizado."""
    return {
        "nome": nome.strip().title(),
        "cargo": cargo.strip().title(),
        "salario": round(salario, 2)
    }

def exibir_colaboradores(lista_colaboradores: list) -> None:
    """Exibe a lista de colaboradores de forma organizada no terminal."""
    if not lista_colaboradores:
        print("\n[!] Nenhum colaborador cadastrado até o momento.")
        return
    
    print("\n" + "=" * 45)
    print("        COLABORADORES CADASTRADOS")
    print("=" * 45)
    
    for indice, colab in enumerate(lista_colaboradores, start=1):
        print(f"#{indice:02d} | Nome: {colab['nome']}")
        print(f"     Cargo: {colab['cargo']}")
        print(f"     Salário: R$ {colab['salario']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        print("-" * 45)