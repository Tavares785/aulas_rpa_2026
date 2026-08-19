"\n\n\n"

resposta = input("Olá, tudo bem? \nResponda apenas com sim ou não 🤓:\n----------------------\n\n").strip().lower()

if resposta == "sim":
	print("Que bom!")
elif resposta == "não":
	print("Espero que você fique bem!")
else:
	print("Não entendi sua resposta.")
