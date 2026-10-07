cantina = {
    "faturamento": 10000,
    "despesas": 5000,
    "alimentos": ["arroz", "feijão", "macarrão","batata","frutas" ],
}
print(cantina)
print(cantina["faturamento"])
print(cantina["alimentos"])
print(cantina["alimentos"][1])
print(cantina["alimentos"][1][0])
print(cantina["alimentos"][1:]) 
print(cantina["alimentos"][1:3]) #range do item 2 ao 4
print(cantina["alimentos"][-1]) #ultimo item da lista
print(cantina["alimentos"][-2]) #penultimo item da lista
print(cantina["alimentos"][1][2][0]) #primeira letra do item 2 da lista