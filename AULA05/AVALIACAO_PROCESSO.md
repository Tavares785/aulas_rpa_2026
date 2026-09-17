Ficha de Avaliação de RPA

Cenário: A — Conciliação bancária diária

1. Nome do Processo

Conciliação bancária diária.

2. É viável para RPA? 

Sim

3. Justificativa baseada nos 4 critérios essenciais (Repetitividade, Regras de Negócio, Tipo de Dados, Volume).

Repetitividade: O processo é realizado diariamente e segue as mesmas etapas de comparação dos dados.
Regras de Negócio: As regras são fixas e objetivas, utilizando o CNPJ e o valor das transações para comparar o extrato bancário com as baixas do sistema ERP.
Tipo de Dados: Os dados são estruturados, pois o extrato bancário está em formato .csv e as informações do ERP também são estruturadas.
Volume: O processo pode envolver muitas transações diariamente, tornando a automação útil para realizar as comparações de forma rápida e padronizada.

4. Mapeamento Passo a Passo das Ações do Robô

1 - Inicia o processo.
2 - Acessa o local onde está o extrato bancário.
3 - Faz o download do extrato em formato .csv.
4 - Lê os dados do arquivo.
5 - Acessa o sistema ERP.
6 - Consultar as baixas financeiras do período.
7 - Comparar os dados do extrato com as baixas do ERP.
8 - Verificar o CNPJ de cada transação.
9 - Verificar o valor de cada transação.
10 - Identificar os registros que possuem correspondência.
11 - Identificar os registros sem correspondência.
12 - Registrar o resultado da conciliação.
13 - Finalizar o processo.