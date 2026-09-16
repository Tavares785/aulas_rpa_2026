# Lista de transações enviada no enunciado
transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]

# Validação das transações uma a uma
for valor in transacoes:
    
    # Transação acima de R$ 10.000 é suspeita
    if valor > 10000.0:
        print(f"[ALERTA] Transação suspeita de R$ {valor}: Encaminhada para auditoria.")
        continue  # Pula para a próxima transação
    
    # Transação zero ou negativa indica erro e para a execução
    if valor <= 0:
        print(f"[ERRO CRÍTICO] Transação inválida encontrada (R$ {valor}). Interrompendo bot...")
        break  # Interrompe o processo imediatamente
    
    # Processamento padrão para transações normais
    print(f"[SUCESSO] Transação de R$ {valor} processada.")