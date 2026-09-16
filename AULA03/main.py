# main.py
from mod_rh import cadastrar_colaborador, exibir_colaboradores

# Lista em memória para armazenar os dicionários dos colaboradores
colaboradores_db = []

while True:
    print("\n--- MENU SISTEMA DE RH ---")
    print("1 - Cadastrar Colaborador")
    print("2 - Listar Colaboradores")
    print("0 - Sair")
    
    opcao = input("Escolha uma opção: ").strip()
    
    if opcao == "1":
        print("\n--- Novo Cadastro ---")
        nome = input("Digite o nome: ").strip()
        cargo = input("Digite o cargo: ").strip()
        
        # Tratamento simples para garantir que o salário seja digitado como número
        try:
            salario = float(input("Digite o salário (ex: 3500.50): "))
        except ValueError:
            print("[ERRO] Salário inválido! O cadastro não foi realizado.")
            continue
            
        # Chama a função do módulo e adiciona o dicionário retornado à lista
        novo_colaborador = cadastrar_colaborador(nome, cargo, salario)
        colaboradores_db.append(novo_colaborador)
        print(f"[SUCESSO] Colaborador '{nome}' guardado em memória!")
        
    elif opcao == "2":
        exibir_colaboradores(colaboradores_db)
        
    elif opcao == "0":
        print("\nEncerrando o sistema de RH. Até logo!")
        break
        
    else:
        print("\n[ERRO] Opção inválida! Tente novamente.")
