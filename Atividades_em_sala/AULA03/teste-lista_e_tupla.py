lista = [1 ,2 ,3, 4, 5]
print(lista)
lista.append(6)
print(lista)

tupla = (1, 2, 3, 4, 5)
print(tupla)

try:
    tupla.append(6)
    print(tupla)

except AttributeError as erro:
    print(f"Erro: {erro}")

print(tupla)