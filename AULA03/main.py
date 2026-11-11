from mod_rh import cadastrar_colaborador, exibir_colaboradores

def main():
    colaboradores = []
    while True:
        print("\n=== Menu RH ===")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            nome = input("Nome do colaborador: ")
            cargo = input("Cargo: ")
            try:
                salario = float(input("Salário: "))
                novo_colab = cadastrar_colaborador(nome, cargo, salario)
                colaboradores.append(novo_colab)
                print("[SUCESSO] Colaborador cadastrado!")
            except ValueError:
                print("[ERRO] Por favor, digite um valor numérico válido.")
        elif opcao == '2':
            exibir_colaboradores(colaboradores)
        elif opcao == '0':
            print("Encerrando o sistema...")
            break
        else:
            print("[ERRO] Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()