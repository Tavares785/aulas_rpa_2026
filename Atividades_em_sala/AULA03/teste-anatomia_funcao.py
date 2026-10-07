def saudacao(nome, idade):
    print(f"Olá, {nome}! Bem-vindo(a) à aula de Análise e Desenvolvimento de Sistemas.")
    print(f"Você tem {idade} anos.")
    try:
        print("{idade}")
    except (AttributeError, TypeError) as erro:
        print(f"Erro: {erro}")  

saudacao("João",25)