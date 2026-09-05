from tabulate import tabulate
def cadastrar_colaborador(nome, cargo, salario):
    cadastros = {
        "nome" : nome,
        "cargo" : cargo,
        "salario" : salario
    }
    return cadastros

def exibir_colaboradores(lista_colaboradores):
        print(tabulate(lista_colaboradores, headers='keys'))


