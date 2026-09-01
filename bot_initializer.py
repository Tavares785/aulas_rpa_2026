BOT_NAME: str = "RPA_FINANCEIRO_01"
MAX_RETRIES: int = 3
EXECUTION_TIMEOUT: float = 45.5
IS_PRODUCTION: bool = False

def main():
    print("=" * 60)
    print(f"🤖 INICIALIZANDO O BOT: {BOT_NAME}")
    print("=" * 60)
    print("📋 Verificação de Variáveis de Ambiente e Tipagem:")
    print("-" * 60)
    
    print(f"Variável: BOT_NAME          | Valor: '{BOT_NAME}' | Tipo: {type(BOT_NAME)}")
    print(f"Variável: MAX_RETRIES       | Valor: {MAX_RETRIES}                  | Tipo: {type(MAX_RETRIES)}")
    print(f"Variável: EXECUTION_TIMEOUT | Valor: {EXECUTION_TIMEOUT}               | Tipo: {type(EXECUTION_TIMEOUT)}")
    print(f"Variável: IS_PRODUCTION     | Valor: {IS_PRODUCTION}              | Tipo: {type(IS_PRODUCTION)}")
    
    print("-" * 60)
    print("✅ Ambiente verificado e pronto para execução!")
    print("=" * 60)

if __name__ == "__main__":
    main()
