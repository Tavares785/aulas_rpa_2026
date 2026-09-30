from mod_rh import cadastrar_colaborador, exibir_colaboradores

# Lista principal de colaboradores
lista = []

# Cadastrando colaboradores
c1 = cadastrar_colaborador("Carlos", "Analista de Dados", 4500.0)
c2 = cadastrar_colaborador("Mariana", "Desenvolvedora", 6800.0)

lista.append(c1)
lista.append(c2)

# Exibindo no terminal
exibir_colaboradores(lista)
