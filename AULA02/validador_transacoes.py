transacoes = [150.00, 12000.00, 500.50, -50.00, 200.00]

for valor in transacoes:
    if valor > 10000.00:
        print(f"[ALERTA] Transação suspeita de R$ {valor:.2f}: Encaminhada para auditoria.")
        continue
    elif valor <= 0:
        print(f"[ERRO CRÍTICO] Transação inválida encontrada (R$ {valor:.2f}). Interrompendo bot...")
        break
    else:
        print(f"[SUCESSO] Transação de R$ {valor:.2f} processada.")
