Cenário A — Conciliação bancária diária
1. Nome do Processo

Conciliação bancária diária

2. É viável para RPA?

Sim.

3. Justificativa baseada nos 4 critérios essenciais
Repetitividade: O processo é realizado diariamente e segue as mesmas etapas de comparação das transações.
Regras de Negócio: Existem regras claras e fixas para realizar a comparação, utilizando principalmente o CNPJ e o valor da transação.
Tipo de Dados: Os dados são estruturados, pois o extrato bancário está disponível em formato .csv e as informações das baixas estão registradas no sistema ERP.
Volume: O processo pode envolver uma grande quantidade de transações, tornando a automação útil para reduzir o trabalho manual e o tempo necessário para a conciliação.

Conclusão: O processo é viável para RPA porque possui alta repetitividade, regras objetivas, dados estruturados e pode envolver um volume significativo de operações.

4. Mapeamento Passo a Passo das Ações do Robô
Iniciar a execução do robô.
Localizar e abrir o arquivo de extrato bancário .csv.
Ler os dados das transações do extrato.
Acessar o sistema ERP.
Consultar as baixas registradas no sistema.
Comparar as transações do banco com as baixas do ERP utilizando o CNPJ e o valor.
Identificar as transações que possuem correspondência.
Identificar as transações que apresentam divergências.
Registrar os resultados da conciliação.
Gerar um relatório com as transações conciliadas e as divergências encontradas.
Encerrar a execução do robô.