
# Declaração e inicialização das variáveis com seus respectivos tipos
BOT_NAME = "RPA_FINANCEIRO_01"      # String (Texto)
MAX_RETRIES = 3                     # Integer (Inteiro)
EXECUTION_TIMEOUT = 120.5           # Float (Número Decimal)
IS_PRODUCTION = False               # Boolean (Verdadeiro ou Falso)

# Impressão da mensagem de inicialização e tipagem das variáveis
print("=" * 60)
print("🤖 INICIALIZADOR DO ROBÔ - VERIFICAÇÃO DE AMBIENTE 🤖")
print("=" * 60)

print(f"Variável: BOT_NAME")
print(f"  - Valor: {BOT_NAME}")
print(f"  - Tipo:  {type(BOT_NAME)}")
print("-" * 40)

print(f"Variável: MAX_RETRIES")
print(f"  - Valor: {MAX_RETRIES}")
print(f"  - Tipo:  {type(MAX_RETRIES)}")
print("-" * 40)

print(f"Variável: EXECUTION_TIMEOUT")
print(f"  - Valor: {EXECUTION_TIMEOUT}")
print(f"  - Tipo:  {type(EXECUTION_TIMEOUT)}")
print("-" * 40)

print(f"Variável: IS_PRODUCTION")
print(f"  - Valor: {IS_PRODUCTION}")
print(f"  - Tipo:  {type(IS_PRODUCTION)}")

print("=" * 60)
print("✅ Verificação de tipos concluída com sucesso!")
print("=" * 60)
