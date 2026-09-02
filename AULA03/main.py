from mod_rh import cadastrar_colaborador, exibir_colaboradores

def main():
    lista_colaboradores = []

    while True:
        print("\n=== MENU DE GERENCIAMENTO DE RH ===")
        print("1 - Cadastrar Colaborador")
        print("2 - Listar Colaboradores")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- Novo Cadastro ---")
            nome = input("Digite o nome: ").strip()
            cargo = input("Digite o cargo: ").strip()
            
            try:
                salario = float(input("Digite o salário: "))
                novo_colaborador = cadastrar_colaborador(nome, cargo, salario)
                lista_colaboradores.append(novo_colaborador)
                print("🎉 Colaborador cadastrado com sucesso!")
            except ValueError:
                print("❌ Erro: O salário deve ser um número válido (use ponto para decimais, ex: 2500.50).")

        elif opcao == "2":
            exibir_colaboradores(lista_colaboradores)

        elif opcao == "0":
            print("\nEncerrando o sistema. Até logo!")
            break
            
        else:
            print("⚠️ Opção inválida! Escolha entre 1, 2 ou 0.")

if __name__ == "__main__":
    main()