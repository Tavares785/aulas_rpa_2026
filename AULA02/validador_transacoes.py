# Lista de transações fornecida no enunciado
transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]

# Percorre a lista de transações
for valor in transacoes:
    # 1. Verifica transações inválidas ou negativas (Erro Crítico)
    if valor <= 0:
        print(f"[ERRO CRÍTICO] Transação inválida encontrada (R$ {valor:.2f}). Interrompendo bot...")
        break
    # 2. Verifica transações suspeitas (Acima de R$ 10.000,00)
    elif valor > 10000.00:
        print(f"[ALERTA] Transação suspeita de R$ {valor:.2f}: Encaminhada para auditoria.")
        continue
    # 3. Transações normais e válidas
    else:
        print(f"[SUCESSO] Transação de R$ {valor:.2f} processada.")
