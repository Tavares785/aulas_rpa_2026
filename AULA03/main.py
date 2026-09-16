from mod_rh import cadastrar_colaborador, exibir_colaboradores
 
 
def ler_salario() -> float:
   
    while True:
        entrada = input("Salário: ").replace(",", ".").strip()
        try:
            salario = float(entrada)
            if salario < 0:
                print("O salário não pode ser negativo. Tente novamente.")
                continue
            return salario
        except ValueError:
            print("Valor inválido. Digite um número (ex: 2500.00).")
 
 
def ler_texto(mensagem: str) -> str:
    
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Este campo não pode ficar vazio. Tente novamente.")
 
 
def exibir_menu() -> None:
    print("\n" + "=" * 40)
    print("MENU - CADASTRO DE COLABORADORES")
    print("=" * 40)
    print("1 - Cadastrar")
    print("2 - Listar")
    print("0 - Sair")
 
 
def main() -> None:
    colaboradores = []
 
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
 
        if opcao == "1":
            nome = ler_texto("Nome: ")
            cargo = ler_texto("Cargo: ")
            salario = ler_salario()
            colaborador = cadastrar_colaborador(nome, cargo, salario)
            colaboradores.append(colaborador)
            print(f"\nColaborador '{nome}' cadastrado com sucesso!\n")
 
        elif opcao == "2":
            exibir_colaboradores(colaboradores)
 
        elif opcao == "0":
            print("\nSaindo do sistema. Até logo!\n")
            break
 
        else:
            print("\nOpção inválida. Tente novamente.\n")
 
 
if __name__ == "__main__":
    main()