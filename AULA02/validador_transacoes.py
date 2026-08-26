transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800,0, 0]

for valor in transacoes:
    if valor > 10000.00:
        print("[ALERTA] Transação suspeita de R$ <VALOR>: Encaminhada para auditoria.")
        continue
    elif valor <= 0:
        print("[ERRO CRÍTICO] Transação inválida encontrada (R$", valor, "). Interrompendo bot...")
        break
    else:
        print("[SUCESSO] Transação de R$ <VALOR> processada.")
        continue
