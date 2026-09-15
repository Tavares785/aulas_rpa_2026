from mod_rh import cadastrar_colaborador, exibir_colaboradores

def main():
    colaboradores = []
    
    while True:
        print("\n=== MENU RH ===")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            nome = input("Digite o nome do colaborador: ")
            cargo = input("Digite o cargo: ")
            try:
                salario = float(input("Digite o salário: R$ "))
                novo_colab = cadastrar_colaborador(nome, cargo, salario)
                colaboradores.append(novo_colab)
                print(f"[SUCESSO] Colaborador {nome} cadastrado com sucesso!")
            except ValueError:
                print("[ERRO] Salário inválido. Por favor, digite um número.")
                
        elif opcao == "2":
            exibir_colaboradores(colaboradores)
            
        elif opcao == "0":
            print("Encerrando o sistema de RH. Até logo!")
            break
        else:
            print("[ERRO] Opção inválida. Escolha 1, 2 ou 0.")

if __name__ == "__main__":
    main()