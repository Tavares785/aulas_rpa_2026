transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]

for valor in transacoes:
    print()
    if valor > 10000:
        print(f'\033[33m[ALERTA] Transação suspeita de R${valor:.2f}: Encaminhada para auditoria.\033[0m')
        continue
    elif valor <= 0:
        if valor == 0:
            print(f'\033[31m[ERRO CRÍTICO] Transação inválida de R${valor:.2f}: Valor zero não permitido.\033[0m')
            break
        else:
            print(f'\033[31m[ERRO CRÍTICO] Transação inválida de R${valor:.2f}: Valor negativo não permitido.\033[0m')
    else:
        print(f'\033[32m[SUCESSO] Transação de R${valor:.2f} processada com sucesso.\033[0m')
