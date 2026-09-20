Bot_Name = "RPA_Financeiro_01"
Max_Retries = 3
Execution_Timeout = 45.5
Is_Production = False

print("--- Inicialização do Robô ---")
print(f"Nome do Robô: {Bot_Name} | Tipo: {type(Bot_Name)}")
print(f"Máximo de Tentativas: {Max_Retries} | Tipo: {type(Max_Retries)}")
print(f"Tempo Limite: {Execution_Timeout}s | Tipo: {type(Execution_Timeout)}")
print(f"Ambiente de Produção: {Is_Production} | Tipo: {type(Is_Production)}")
print("------------------------------")
