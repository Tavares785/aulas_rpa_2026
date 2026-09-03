numero = int(input("Digite um número para gerar a tabuada: "))

for multiplicador in range(1, 11):
	resultado = numero * multiplicador
	print(f"{numero} x {multiplicador} = {resultado}")
