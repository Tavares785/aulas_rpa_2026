transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]

for valor in transacoes:
    if valor >10000:
        print(f"[ALERTA] Transação suspeita de R$ {valor}: Encaminhada para auditoria.")
    if valor <= 0:
        print(f"[ERRO CRÍTICO] Transação inválida encontrada (R$ {valor}). Interrompendo bot...")
    else:
        print(f"[SUCESSO] Transação de R$ {valor} processada.")
    