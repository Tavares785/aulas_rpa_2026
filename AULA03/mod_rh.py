def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    """cria e retorna um dicionario de colaborador."""
    return {
        "nome": nome.strip(),
        "cargo": cargo.strip(),
        "salario": float(salario)
    }

def exibir_colaboradores(lista_colaboradores):
    for colaborador in lista_colaboradores:
        print("Nome:", colaborador["nome"])
        print("Cargo:", colaborador["cargo"])
        print("Salário:", colaborador["salario"])