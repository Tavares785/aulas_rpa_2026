from mod_rh import cadastrar_colaborador, exibir_colaboradores

def main():
    lista_colaboradores = []
    
    while True:
        print("\n--- MENU ---")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            print("\n-- Cadastro de Colaborador --")
            nome = input("Digite o nome: ")
            cargo = input("Digite o cargo: ")
            
            try:
                salario = float(input("Digite o salário: R$ "))
            except ValueError:
                print("Valor de salário inválido! Cadastre novamente.")
                continue
                
            novo_colaborador = cadastrar_colaborador(nome, cargo, salario)
            lista_colaboradores.append(novo_colaborador)
            print("Colaborador cadastrado com sucesso!")
            
        elif opcao == "2":
            print("\n-- Lista de Colaboradores --")
            if not lista_colaboradores:
                print("Nenhum colaborador cadastrado ainda.")
            else:
                exibir_colaboradores(lista_colaboradores)
                
        elif opcao == "0":  # Espaço corrigido aqui
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida! Escolha 1, 2 ou 0.")

if __name__ == "__main__":
    main()