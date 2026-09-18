Cenário: A - Conciliação bancária diária

1. Nome do Processo

Conciliação bancária diária entre o extrato bancário em formato CSV e as baixas registradas no sistema ERP.

2. É viável para RPA? (Sim / Não)

Sim.

3. Justificativa baseada nos 4 critérios essenciais (Repetitividade, Regras de Negócio, Tipo de Dados, Volume).

* Repetitividade: o processo é realizado diariamente, seguindo uma sequência de atividades que se repete.
* Regras de Negócio: a comparação utiliza regras objetivas e fixas, como CNPJ e valor das transações, permitindo determinar se os registros correspondem.
* Tipo de Dados: o processo utiliza dados estruturados, pois o extrato bancário está disponível em formato CSV e as informações do ERP também podem ser tratadas de forma estruturada.
* Volume: a conciliação pode envolver muitas linhas de transações diariamente, tornando a automação útil para processar os registros de forma padronizada e reduzir o trabalho manual.

4. Mapeamento Passo a Passo das Ações do Robô

5. Acessar o local onde o extrato bancário está disponível.

6. Baixar o extrato bancário diário em formato CSV.

7. Ler os registros do arquivo CSV.

8. Acessar o sistema ERP.

9. Consultar as baixas registradas no ERP para o período correspondente.

10. Comparar os registros do extrato com as baixas do ERP utilizando CNPJ e valor como regras de comparação.

11. Identificar os registros conciliados.

12. Identificar os registros sem correspondência.

13. Registrar ou apresentar o resultado da conciliação para análise dos casos não correspondentes.

14. Encerrar a execução após processar todos os registros.
