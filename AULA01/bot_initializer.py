# bot_initializer.py
# Laboratório 01: Configuração do Ambiente de Desenvolvimento e Olá Mundo do Bot

BOT_NAME: str = "RPA_FINANCEIRO_01"
MAX_RETRIES: int = 3
EXECUTION_TIMEOUT: float = 60.0
IS_PRODUCTION: bool = False


def main():
    print("=" * 50)
    print("      INICIALIZADOR DO ROBÔ - CONFIGURAÇÕES     ")
    print("=" * 50)

    print(f"Nome do Bot        : {BOT_NAME} | Tipo: {type(BOT_NAME)}")
    print(f"Máx. de Tentativas : {MAX_RETRIES} | Tipo: {type(MAX_RETRIES)}")
    print(f"Timeout Execução   : {EXECUTION_TIMEOUT}s | Tipo: {type(EXECUTION_TIMEOUT)}")
    print(f"Ambiente Produção  : {IS_PRODUCTION} | Tipo: {type(IS_PRODUCTION)}")

    print("=" * 50)
    print("Status: Variáveis de ambiente inicializadas com sucesso.")


if __name__ == "__main__":
    main()











































print("Espacos")