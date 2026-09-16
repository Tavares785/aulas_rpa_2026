## Cenário:
conciliação bancária diária feita a partir do download do extrato `.csv` e comparação das linhas com as baixas do sistema ERP via regras fixas de CNPJ e valor.

1. __Nome do Processo:__

    Conciliação Bancária Diária

2. __É viável para RPA?__

    Sim

3. __Justificativa baseada nos 4 critérios essenciais (Repetitividade, Regras de Negócio, Tipo de Dados, Volume).__

    O processo é executado diariamente sendo ideal para a execução do RPA, as regras de negócio são baseadas em critérios fixos (como o CNPJ) sem depender de julgamento humano, os dados de entrada são altamente estruturados no arquivo .csv e apresenta alto volume de transações diárias que demandam esforço manual repetitivo.


4. __Mapeamento Passo a Passo das Ações do Robô__
    1. Acesso ao Download.
    2. Abre ERP.
    3. Leitura e extração do .csv.
    4. Comparação de dados das linhas do ERP usando CNPJ e VALOR.
    5. Execução de baixas.
    6. Exceções e relátorios.
