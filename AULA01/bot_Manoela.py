
BOT_NAME = "RPA_FINANCEIRO_01"
MAX_RETRIES = 3
EXECUTION_TIMEOUT = 120.5
IS_PRODUCTION = True


print("=" * 50)
print("   INICIALIZANDO CONFIGURAÇÕES DO ROBÔ DE RPA   ")
print("=" * 50)

print(f"Nome do Robô (BOT_NAME): {BOT_NAME} | Tipo: {type(BOT_NAME)}")
print(f"Máximo de Tentativas (MAX_RETRIES): {MAX_RETRIES} | Tipo: {type(MAX_RETRIES)}")
print(f"Timeout de Execução (EXECUTION_TIMEOUT): {EXECUTION_TIMEOUT}s | Tipo: {type(EXECUTION_TIMEOUT)}")
print(f"Ambiente de Produção (IS_PRODUCTION): {IS_PRODUCTION} | Tipo: {type(IS_PRODUCTION)}")

print("=" * 50)
print("Status: Variáveis de ambiente validadas com sucesso!")
print("=" * 50)