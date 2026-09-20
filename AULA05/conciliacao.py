import csv

erp = [
    {"cnpj": "12.345.678/0001-90", "valor": 1500.00},
    {"cnpj": "98.765.432/0001-10", "valor": 2500.00},
    {"cnpj": "11.222.333/0001-44", "valor": 800.00}
]

with open("extrato.csv", "r", encoding="utf-8") as arquivo:
    extrato = csv.DictReader(arquivo)

    for transacao in extrato:
        cnpj = transacao["cnpj"]
        valor = float(transacao["valor"])

        encontrado = any(
            item["cnpj"] == cnpj and item["valor"] == valor
            for item in erp
        )

        if encontrado:
            print(f"OK - Transação encontrada: {cnpj} - R$ {valor:.2f}")
        else:
            print(f"DIVERGÊNCIA: {cnpj} - R$ {valor:.2f}")