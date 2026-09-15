def cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict:
    colaborador = {
		"nome": nome,
		"cargo": cargo,
		"salario": salario,
	}
    return colaborador


def exibir_colaboradores(lista_colaboradores: list) -> None:
	for colaborador in lista_colaboradores:
		print(
			f"Nome: {colaborador['nome']} | "
			f"Cargo: {colaborador['cargo']} | "
			f"Salário: R$ {colaborador['salario']:.2f}"
		)