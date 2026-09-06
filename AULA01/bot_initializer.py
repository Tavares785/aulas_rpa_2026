BOT_NAME = "RPA_FINANCEIRO_01"
MAX_RETRIES = 3
EXECUTION_TIMEOUT = 120.5
IS_PRODUCTION = True

print("=== Inicialização do Robô ===")
print(f"Nome do Bot: {BOT_NAME} | Tipo: {type(BOT_NAME)}")
print(f"Máx. Tentativas: {MAX_RETRIES} | Tipo: {type(MAX_RETRIES)}")
print(f"Timeout de Execução: {EXECUTION_TIMEOUT} | Tipo: {type(EXECUTION_TIMEOUT)}")
print(f"Ambiente Produção: {IS_PRODUCTION} | Tipo: {type(IS_PRODUCTION)}")
