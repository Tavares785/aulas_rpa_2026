#1. Crie um script chamado `bot_initializer.py`.
#2. Declare e inicialize as seguintes variáveis:
#   - `BOT_NAME` (String): Nome do robô (ex: "RPA_FINANCEIRO_01").
#   - `MAX_RETRIES` (Integer): Número máximo de tentativas de execução em caso de falha.
#   - `EXECUTION_TIMEOUT` (Float): Tempo limite por tarefa em segundos.
#   - `IS_PRODUCTION` (Boolean): Flag indicando se o ambiente é de produção.
#3. Imprima no terminal uma mensagem de inicialização formatada, exibindo todos os valores #configurados e a tipagem de cada variável utilizando a função `type()`.
#4. Commit o código no seu repositório Git e suba PR para o GitHub (`aulas_rpa_2026`).

BOT_NAME: str = "RPA_FINANCEIRO_01"
MAX_RETRIES: int = 3
EXECUTION_TIMEOUT: float = 1.5
IS_PRODUCTION: bool = True

print("BOT INICIANDO. . .")
print(f"Nome do Robô: {BOT_NAME} (Tipo: {type(BOT_NAME)})")
print(f"Número máximo de tentativas: {MAX_RETRIES} (Tipo: {type(MAX_RETRIES)})")
print(f"Tempo limite por tarefa: {EXECUTION_TIMEOUT} segundos (Tipo: {type(EXECUTION_TIMEOUT)})")
print(f"Ambiente de produção: {IS_PRODUCTION} (Tipo: {type(IS_PRODUCTION)})")