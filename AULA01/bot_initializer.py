# 2. Declaração e inicialização das variáveis
BOT_NAME = "RPA_FINANCEIRO_01"
MAX_RETRIES = 3
EXECUTION_TIMEOUT = 45.5
IS_PRODUCTION = False

# 3. Impressão da mensagem formatada com os valores e os tipos de dados
print("=== INICIALIZAÇÃO DO ROBÔ ===")
print(f"Nome do Robô: {BOT_NAME} | Tipo: {type(BOT_NAME)}")
print(f"Máximo de Tentativas: {MAX_RETRIES} | Tipo: {type(MAX_RETRIES)}")
print(f"Tempo Limite (Timeout): {EXECUTION_TIMEOUT}s | Tipo: {type(EXECUTION_TIMEOUT)}")
print(f"Ambiente de Produção: {IS_PRODUCTION} | Tipo: {type(IS_PRODUCTION)}")
print("=============================")
BOT_NAME:str = "RPA_FINANCEIRO_01"
MAX_RETRIES:int = 3
EXECUTION_TIMEOUT:float = 30.0
IS_PRODUCTION:bool = False

print(f"Bot Name: {BOT_NAME} (Type: {type(BOT_NAME)})")
print(f"Max Retries: {MAX_RETRIES} (Type: {type(MAX_RETRIES)})")
print(f"Execution Timeout: {EXECUTION_TIMEOUT} (Type: {type(EXECUTION_TIMEOUT)})")
print(f"Is Production: {IS_PRODUCTION} (Type: {type(IS_PRODUCTION)})")