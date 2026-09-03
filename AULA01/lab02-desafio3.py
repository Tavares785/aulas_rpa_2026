BOT_NAME: str = "RPA_FINANCEIRO_01"
MAX_RETRIES: int = 3
EXECUTION_TIMEOUT: float = 1.5
IS_PRODUCTION: bool = True

print("BOT INICIANDO...")
print(f"Nome do Robô: {BOT_NAME} (Tipo: {type(BOT_NAME)})")
print(f"Número máximo de tentativas: {MAX_RETRIES} (Tipo: {type(MAX_RETRIES)})")
print(f"Tempo limite por tarefa: {EXECUTION_TIMEOUT} segundos (Tipo: {type(EXECUTION_TIMEOUT)})")

if IS_PRODUCTION:
	print("Ambiente: Produção")
else:
	print("Ambiente: Desenvolvimento")
