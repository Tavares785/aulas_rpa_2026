"""
Script principal para gerenciar cadastro de colaboradores
"""

from mod_rh import cadastrar_colaborador, exibir_colaboradores


def main():
    """
    Menu principal para gerenciamento de colaboradores.
    """
    lista_colaboradores = []
    
    while True:
        print("\n" + "=" * 40)
        print("🏢 SISTEMA DE CADASTRO - RH")
        print("=" * 40)
        print("1 - Cadastrar")
        print("2 - Listar")
        print("0 - Sair")
        print("=" * 40)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n📝 CADASTRO DE COLABORADOR")
            nome = input("Nome: ").strip()
            cargo = input("Cargo: ").strip()
            
            try:
                salario = float(input("Salário: "))
                colaborador = cadastrar_colaborador(nome, cargo, salario)
                lista_colaboradores.append(colaborador)
                print(f"\n✅ Colaborador '{nome}' cadastrado com sucesso!")
            except ValueError:
                print("\n❌ Erro: Salário deve ser um número válido.")
        
        elif opcao == "2":
            exibir_colaboradores(lista_colaboradores)
        
        elif opcao == "0":
            print("\n👋 Encerrando o sistema. Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
