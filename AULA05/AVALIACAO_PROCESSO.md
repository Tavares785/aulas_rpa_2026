Cenário: A

1. Nome do Processo 
Conciliação Bancária Diária

2. É viável para RPA? (Sim / Não)
Sim

3. Justificativa baseada nos 4 critérios essenciais (Repetitividade, Regras de Negócio, Tipo de Dados, Volume).
repetitividade: Alto grau de repetitividade, pois é executado diariamente com a mesma lógica
regras de negocio: uma regra clara é a regra fixa de CNPJ e valor
tipo de dados:  .csv que é um dado estruturado
volume: volume alto de linhas, pois como mencionado anteriormente ele é repetitivo e diario

4. Mapeamento Passo a Passo das Ações do Robô
1. ele começa baixando o extrato bancário em .csv
2. ele abre o arquivo e compara CNPJ e valor de cada linha do extrato com os lançamentos do ERP 
3. se for "compatível" ele concilia ou confirma a baixa
4. se não ele registra um log de exceção/pendência para conferência manual
