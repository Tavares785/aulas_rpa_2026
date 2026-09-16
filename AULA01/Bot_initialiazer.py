BOT_NAME = "RPA_FINANCEIRO_01"

MAX_RETRIES = 3

EXECUTION_TIMEOUT = 45.5

IS_PRODUCTION = False

print("Iniciando o robo...")
print("")

print("Nome do robo:", BOT_NAME)
print("Tipo dessa variavel:", type(BOT_NAME))
print("")

print("Numero maximo de tentativas:", MAX_RETRIES)
print("Tipo dessa variavel:", type(MAX_RETRIES))
print("")

print("Tempo limite (timeout):", EXECUTION_TIMEOUT)
print("Tipo dessa variavel:", type(EXECUTION_TIMEOUT))
print("")

print("Esta em producao?", IS_PRODUCTION)
print("Tipo dessa variavel:", type(IS_PRODUCTION))
print("")

print("Robo pronto para rodar!")