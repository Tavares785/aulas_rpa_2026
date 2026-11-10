transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]
for valor in transacoes:
  if valor <= 0:
    print(f"[ERRO CRÍTICO] Transação inválida encontrada (R$ {valor}).Interrompendo bot...")
    break
  elif valor > 10000.0:
    print(f"[ALERTA] Transação suspeita de R$ {valor}: Encaminhada para auditoria.)
    continue
    else:
    print("f[SUCESSO] transação de R$ {valor} processada.)
