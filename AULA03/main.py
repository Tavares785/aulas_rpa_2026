import mod_rh
colaboradores = []
while True:
    print('--'*20)
    print('\n\033[34mESCOLHA UMA OPÇÃO[1 a 3]:\033[0m')
    opcao = input('1-Cadastrar Colaborador.\n2-Listar Colaboradores.\n3-Sair.\n')
    
    if opcao == '1':
        nome = input('Digite o nome do colaborador: ')
        cargo = input('Digite o cargo do colaborador: ')
        salario = float(input('Digite o salário do colaborador: '))
        colaboradores.append(mod_rh.cadastrar_colaborador(nome, cargo, salario))

    elif opcao == '2':
        mod_rh.exibir_colaboradores(colaboradores)  

    elif opcao == "3":
        print('\033[32mSaindo do programa...\033[0m')
        break
    else:
        print('\033[31mOPÇÃO INVÁLIDA. TENTE NOVAMENTE.\033[0m')
