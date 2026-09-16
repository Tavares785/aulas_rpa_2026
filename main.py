from mod_rh import cadastrar_colaborador, exibir_colaboradores

def executar_menu():
    banco_usuarios = []  # Armazena os colaboradores em memória

    while True:
        print("\n=== 🏢 Sistema de Cadastro de RH ===")
        print("1 - Cadastrar Colaborador")
        print("2 - Listar Colaboradores")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- Novo Cadastro ---")
            nome = input("Digite o nome: ").strip()
            cargo = input("Digite o cargo: ").strip()
            
            try:
                salario = float(input("Digite o salário: R$ "))
            except ValueError:
                print("❌ Erro: O salário deve ser um número válido. Tente novamente.")
                continue

            # Cria o dicionário chamando a função do módulo mod_rh
            novo_colaborador = cadastrar_colaborador(nome, cargo, salario)
            # Salva na lista
            banco_usuarios.append(novo_colaborador)
            print(f"✅ {nome} cadastrado com sucesso!")

        elif opcao == "2":
            exibir_colaboradores(banco_usuarios)

        elif opcao == "0":
            print("\n👋 Encerrando o sistema. Até logo!")
            break
        
        else:
            print("❌ Opção inválida! Escolha 1, 2 ou 0.")

if __name__ == "__main__":
    executar_menu()

