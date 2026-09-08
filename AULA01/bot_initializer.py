BOT_NAME = "RPA_FINANCEIRO_01"
MAX_RETRIES = 3
EXECUTION_TIMEOUT = 60.0  # in seconds
IS_PRODUCTION = True
tls = 47 #tamanho da linha de separaçcão
print("="*tls)
print(f"Iniciando bot {BOT_NAME}...")
print("-"*tls)
print(f"Bot: {BOT_NAME} - Tipo: {type(BOT_NAME)}")
print(f"Max retries: {MAX_RETRIES} - Tipo: {type(MAX_RETRIES)}")
print(f"Execution timeout: {EXECUTION_TIMEOUT} - Tipo: {type(EXECUTION_TIMEOUT)}")
print(f"Is production: {IS_PRODUCTION} - Tipo: {type(IS_PRODUCTION)}")
print("-"*tls)
print("Configuração carregada com sucesso!")
print("="*tls)