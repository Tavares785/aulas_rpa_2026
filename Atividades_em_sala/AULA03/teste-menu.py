def menu():
    print("Menu:")
    print("1. Cadastrar Usuário")
    print("2. Opção 2")
    print("3. Opção 3")
    op = input("Escolha uma opção: ")
    print(f"Você escolheu a opção {op}.")
    if op == "1":
        nome = input("Digite o nome do usuário: ")
        idade = input("Digite a idade do usuário: ")
        email = input("Digite o email do usuário: ")
        print(f"Usuário cadastrado: Nome: {nome}, Idade: {idade}, Email: {email}")
menu()