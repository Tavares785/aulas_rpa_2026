BOT_NAME = "RPA_FINANCEIRO_01"
MAX_RETRIES = 5
EXECUTION_TIMEOUT = 15.0
IS_PRODUCTION = True

print("Nome do robo: ", BOT_NAME, type(BOT_NAME), end="\n")
print("Máximo de tentativas: ", MAX_RETRIES, type(MAX_RETRIES), end="\n")
print("Tempo limite por tarefa em segundos: ", EXECUTION_TIMEOUT, type(EXECUTION_TIMEOUT), end="\n")
print("Flag indicando se o ambiente é produção: ", IS_PRODUCTION, type(IS_PRODUCTION), end="\n")