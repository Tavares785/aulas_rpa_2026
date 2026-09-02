"""
Validador de Transações Financeiras
Analisa uma fila de transações e identifica valores suspeitos ou inválidos.
"""

# Lista de transações a processar
transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]

print("=" * 60)
print("🏦 VALIDADOR DE TRANSAÇÕES FINANCEIRAS")
print("=" * 60)

for transacao in transacoes:
    if transacao > 10000.00:
        print(f"[ALERTA] Transação suspeita de R$ {transacao:.2f}: Encaminhada para auditoria.")
        continue
    elif transacao <= 0:
        print(f"[ERRO CRÍTICO] Transação inválida encontrada (R$ {transacao:.2f}). Interrompendo bot...")
        break
    else:
        print(f"[SUCESSO] Transação de R$ {transacao:.2f} processada.")

print("=" * 60)
print("✅ Processamento finalizado.")
print("=" * 60)
