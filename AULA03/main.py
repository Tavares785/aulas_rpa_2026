from mod_rh import cadastrar_colaborador, exibir_colaboradores

def exibir_menu():
    print("\n┌──────────────────────────────┐")
    print("│      PAINEL DE RH - MENU     │")
    print("├──────────────────────────────┤")
    print("│ 1 - Cadastrar Colaborador    │")
    print("│ 2 - Listar Colaboradores     │")
    print("│ 0 - Sair                     │")
    print("└──────────────────────────────┘")

def main():
    colaboradores = []
    
    print(">> Sistema de Automação de RH Iniciado <<")
    
    while True:
        exibir_menu()
        opcao = input("Digite a opção desejada: ").strip()
        
        if opcao == "1":
            print("\n--- Novo Cadastro ---")
            nome = input("Informe o nome do colaborador: ")
            cargo = input("Informe o cargo: ")
            
            try:
                salario = float(input("Informe o salário (R$): ").replace(",", "."))
                novo_colab = cadastrar_colaborador(nome, cargo, salario)
                colaboradores.append(novo_colab)
                print(f"\n[✓] Sucesso: {novo_colab['nome']} foi cadastrado(a)!")
            except ValueError:
                print("\n[X] Erro: Digite um valor numérico válido para o salário.")
                
        elif opcao == "2":
            exibir_colaboradores(colaboradores)
            
        elif opcao == "0":
            print("\nEncerrando o sistema RH... Até logo!")
            break
            
        else:
            print("\n[!] Opção inválida. Por favor, escolha 1, 2 ou 0.")

if __name__ == "__main__":
    main()