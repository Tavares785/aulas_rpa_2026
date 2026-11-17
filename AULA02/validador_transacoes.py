
transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]

print("=" * 60)
print("🔍 INICIANDO PROCESSAMENTO DA FILA DE TRANSAÇÕES 🔍")
print("=" * 60)

# Percorre a lista de transações usando um laço for
for valor in transacoes:
    
    # Se a transação for maior que 10000.00 (Suspeita)
    if valor > 10000.00:
        print(f"[ALERTA] Transação suspeita de R$ {valor:.2f}: Encaminhada para auditoria.")
        continue  # Pula para a próxima iteração do laço
        
    # Se a transação for menor ou igual a 0 (Inválida)
    if valor <= 0:
        print(f"[ERRO CRÍTICO] Transação inválida encontrada (R$ {valor:.2f}). Interrompendo bot...")
        break 
        
    # Para transações normais
    print(f"[SUCESSO] Transação de R$ {valor:.2f} processada.")

print("=" * 60)
print("🏁 FIM DA EXECUÇÃO DO SCRIPT 🏁")
print("=" * 60)
