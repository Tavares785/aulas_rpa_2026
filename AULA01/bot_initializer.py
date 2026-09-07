# 1. Declaração e inicialização das variáveis
BOT_NAME = "BOT_KAUA_01"
MAX_RETRIES = 5
EXECUTION_TIMEOUT = 120.5
IS_PRODUCTION = True

# 2. Impressão da mensagem formatada e tipagem usando type()
print("=== SETUP DO AMBIENTE DO ROBÔ ===")
print(f"Nome do Bot: {BOT_NAME} | Tipo: {type(BOT_NAME)}")
print(f"Tentativas Máximas: {MAX_RETRIES} | Tipo: {type(MAX_RETRIES)}")
print(f"Tempo Limite (seg): {EXECUTION_TIMEOUT} | Tipo: {type(EXECUTION_TIMEOUT)}")
print(f"Ambiente de Produção: {IS_PRODUCTION} | Tipo: {type(IS_PRODUCTION)}")
print("=================================")
