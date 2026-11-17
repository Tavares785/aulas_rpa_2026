transacao = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]
for valor in transacao:
    if valor < 10000.00:
        print(f"[ALERTA] Transação suspeita de R$ {valor}: Encaminhada para auditoria.")
    elif valor < 0:
        print(f"[ERRO] Transação inválida de R$ {valor}: Valor negativo.")
        break
    else:
        print(f"[INFO] Transação de R$ {valor} aprovada.")