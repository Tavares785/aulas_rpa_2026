transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]

for valor in transacoes:
    
    if valor > 10000.00:
        print(f"[ALERTA] Transação suspeita de R$ {valor}: Encaminhada para auditoria.")
        continue  # Usa o continue para ir direto para o próximo da fila
        
    if valor <= 0:
        print(f"[ERRO CRÍTICO] Transação inválida encontrada (R$ {valor}). Interrompendo bot...")
        break  # Usa o break para parar a execução da fila imediatamente
        
    print(f"[SUCESSO] Transação de R$ {valor} processada.")