# 1) Declaracao e inicializacao com tipos explicitos ------------------------
BOT_NAME: str = "RPA_BACKUP_NOTURNO"     # texto  -> str
MAX_RETRIES: int = 3                     # inteiro -> int
EXECUTION_TIMEOUT: float = 12.5          # decimal -> float
IS_PRODUCTION: bool = False              # verdadeiro/falso -> bool


def mostrar_configuracao() -> None:
    """Imprime cada variavel com seu valor e o tipo detectado em runtime."""
    print("=" * 50)
    print(f"Inicializando robo: {BOT_NAME}")
    print("=" * 50)
    for nome, valor in {
        "BOT_NAME": BOT_NAME,
        "MAX_RETRIES": MAX_RETRIES,
        "EXECUTION_TIMEOUT": EXECUTION_TIMEOUT,
        "IS_PRODUCTION": IS_PRODUCTION,
    }.items():
        # type() retorna a CLASSE do objeto -> otimo para mostrar tipagem
        print(f"{nome:<20} = {valor!r:<25} (tipo: {type(valor).__name__})")


if __name__ == "__main__":
    mostrar_configuracao()