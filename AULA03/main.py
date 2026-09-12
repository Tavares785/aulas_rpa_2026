from mod_rh import cadastrar_colaborador, exibir_colaboradores

listar_colaboradores = []
while True:
    opcao = input('Selecione uma opção: 1 - Cadastrar,  2 - Listar, 0 - Sair \n')
    if opcao == "1":
        nome = input('Nome colaborador: ')
        cargo = input('Cargo: ')
        salario = float(input('Salario: '))
        colaborador = cadastrar_colaborador(nome, cargo, salario)
        listar_colaboradores.append(colaborador)        
    elif opcao == "2":
        exibir_colaboradores(listar_colaboradores)
    elif opcao == "0":
        print('Encerrando o programa... até breve!')
        break
    else:
        print('Opção inválida! Tente novamente')
        


