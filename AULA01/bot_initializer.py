BOT_NAME = "RPA_FINANCEIRO_01"
MAX_RETRIES = 3
EXECUTION_TIMEOUT = 60.0
IS_PRODUCTION = False

def main():
    """Exibe as configurações usadas na inicialização do robô."""
    print("=" * 50)
    print("INICIALIZAÇÃO DO ROBÔ")
    print("=" * 50)
    print(f"BOT_NAME: {BOT_NAME!r} | Tipo: {type(BOT_NAME)}")
    print(f"MAX_RETRIES: {MAX_RETRIES} | Tipo: {type(MAX_RETRIES)}")
    print(f"EXECUTION_TIMEOUT: {EXECUTION_TIMEOUT} | Tipo: {type(EXECUTION_TIMEOUT)}")
    print(f"IS_PRODUCTION: {IS_PRODUCTION} | Tipo: {type(IS_PRODUCTION)}")
    print("=" * 50)

if __name__ == "__main__":
    main()

