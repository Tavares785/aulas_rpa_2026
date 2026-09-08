z=[]
def soma(x, y):
    try:
        return x + y
    except (TypeError) as erro:
        print(f"Type Error: {erro}")  
    except (AttributeError, TypeError) as erro:
        print(f"Attribute Error: {erro}")  

print(soma("ola", 5))
resultado = soma(5,3)
z.append(resultado)
print(z)