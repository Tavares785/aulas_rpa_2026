 Ficha de Avaliação de RPA

Cenário: A — Conciliação bancária diária

 1. Nome do Processo

Conciliação bancária diária entre o extrato bancário e as baixas do sistema ERP.

 2. É viável para RPA?

Sim.

 3. Justificativa baseada nos 4 critérios essenciais

Repetitividade: O processo é realizado diariamente, seguindo as mesmas etapas para baixar o extrato e comparar os registros.
Regras de Negócio: A comparação pode ser realizada por regras fixas e objetivas, utilizando principalmente o **CNPJ e o valor** da transação.
Tipo de Dados: Os dados são estruturados, pois o extrato é disponibilizado em arquivo `.csv` e as informações do ERP também podem ser utilizadas para comparação.
Volume: A automação pode processar diversas linhas do extrato e realizar as comparações de forma automática, reduzindo o trabalho manual.

 4. Mapeamento Passo a Passo das Ações do Robô

1. Acessar o sistema ou local onde o extrato bancário está disponível.
2. Baixar o extrato bancário diário no formato `.csv`.
3. Abrir e ler os dados do arquivo.
4. Acessar o sistema ERP.
5. Consultar as baixas registradas no ERP.
6. Comparar os registros do extrato com as baixas do ERP utilizando as regras definidas de **CNPJ e valor**.
7. Identificar os registros que possuem correspondência.
8. Identificar os registros que não possuem correspondência.
9. Registrar ou separar as divergências para análise manual.
10. Finalizar o processo de conciliação e gerar o resultado da operação.
