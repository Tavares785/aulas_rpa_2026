BOT_NAME: str = "RPA_Financeiro_01"
MAX_RETRIES: int = 3
EXECUTION_TIMEOUT: float = 3.0
IS_PRODUCTION: bool = True

print("=" * 50)
print("   INICIALIZAÇÃO DO ROBÔ - VARIÁVEIS DE AMBIENTE")
print("=" * 50)
print(f"  BOT_NAME          : {BOT_NAME}")
print(f"  Tipo              : {type(BOT_NAME)}")
print("-" * 50)
print(f"  MAX_RETRIES       : {MAX_RETRIES}")
print(f"  Tipo              : {type(MAX_RETRIES)}")
print("-" * 50)
print(f"  EXECUTION_TIMEOUT : {EXECUTION_TIMEOUT}")
print(f"  Tipo              : {type(EXECUTION_TIMEOUT)}")
print("-" * 50)
print(f"  IS_PRODUCTION     : {IS_PRODUCTION}")
print(f"  Tipo              : {type(IS_PRODUCTION)}")
print("=" * 50)
print("  Sistema inicializado com sucesso!")
print("=" * 50)
