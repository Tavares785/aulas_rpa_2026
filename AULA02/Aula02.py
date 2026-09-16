idade = int(input("Digite sua idade: "))

if idade<=17:
    print("Você é uma criança")
elif idade<60:
    print("Você é um adulto")
else:
    print("Você é um idoso")

#Soma dos números pares de 1 a 50

soma: int = 0

for numero in range(2, 51, 2):
    soma += numero

print(f"\nA soma dos números pares de 1 a 50 é: {soma}")

#Tabuada de um número

num = int(input("\nDigite um número para gerar a tabuada: "))

for tab in range(1, 11):
    resultado = tab * num
    print(f"{tab} x {num} = {resultado}")