transacoes = [1500.00, 23000.00, 450.75, -200.00, 8900.00, 15000.01, 0.00, 300.00]

for transacao in transacoes:
    if transacao > 10000.00:
        print(f"[ALERTA] Transação suspeita de R$ {transacao:.2f}: Encaminhada para auditoria.")
        continue

    if transacao <= 0:
        print(f"[ERRO CRÍTICO] Transação inválida encontrada (R$ {transacao:.2f}). Interrompendo bot...")
        break

    print(f"[SUCESSO] Transação de R$ {transacao:.2f} processada.")
