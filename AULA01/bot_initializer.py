BOT_NAME:str = "RPA_FINANCEIRO_01"
MAX_RETRIES:int = 3
EXECUTION_TIMEOUT:float = 30.0
IS_PRODUCTION:bool = False

print(f"Bot Name: {BOT_NAME} (Type: {type(BOT_NAME)})")
print(f"Max Retries: {MAX_RETRIES} (Type: {type(MAX_RETRIES)})")
print(f"Execution Timeout: {EXECUTION_TIMEOUT} (Type: {type(EXECUTION_TIMEOUT)})")
print(f"Is Production: {IS_PRODUCTION} (Type: {type(IS_PRODUCTION)})")