# bot_initializer.py
# Script de inicialização e configuração do robô RPA

# Nome do robô (String)
BOT_NAME: str = "RPA_FINANCEIRO_01"

# Número máximo de tentativas em caso de falha (Integer)
MAX_RETRIES: int = 3

# Tempo limite por tarefa em segundos (Float)
EXECUTION_TIMEOUT: float = 30.0

# Flag indicando se o ambiente é de produção (Boolean)
IS_PRODUCTION: bool = True


def display_config() -> None:
    """Exibe as configurações iniciais do robô."""
    print("=== Configurações do Robô ===")
    print(f"Nome:              {BOT_NAME}")
    print(f"Máx. Tentativas:   {MAX_RETRIES}")
    print(f"Timeout (s):       {EXECUTION_TIMEOUT}")
    print(f"Produção:          {IS_PRODUCTION}")


if __name__ == "__main__":
    display_config()
