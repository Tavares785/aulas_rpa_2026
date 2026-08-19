BOT_NAME = "BOB"
max_retires= 20
execution_timeout = 600.0
is_production = True
print("inicializando robo: ", BOT_NAME,"\n")
print("numero maximo de tentativas",max_retires,"\ntipagem:",type(max_retires),"\n")
print("tempo limite de tarefas(em segundos):",execution_timeout,"\ntipagem:",type(execution_timeout),"\n")
print("O ambiente esta em produçao",is_production,"\ntipagem ",type(is_production),"\n")