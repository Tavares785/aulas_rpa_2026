\# Ficha de Avaliação de RPA



\## Processo escolhido



\*\*Cenário A – Conciliação bancária diária\*\*



Processo de comparação do extrato bancário em formato `.csv` com as baixas realizadas no sistema ERP, utilizando regras fixas de CNPJ e valor.



\## 1. Objetivo do processo



Realizar a conciliação bancária diária de forma automática, identificando correspondências entre as movimentações do banco e os registros do ERP.



\## 2. Entradas



\- Extrato bancário em formato `.csv`;



\- Registros de baixas do sistema ERP;



\- CNPJ;



\- Valor da transação.



\## 3. Regras de negócio



\- Comparar o CNPJ da movimentação bancária com o CNPJ registrado no ERP;



\- Comparar o valor da movimentação com o valor registrado no ERP;



\- Considerar a transação conciliada quando CNPJ e valor forem correspondentes;



\- Separar as transações sem correspondência para análise manual.



\## 4. Avaliação de viabilidade para RPA



| Critério | Avaliação |



|---|---|



| Regras claras | Sim |



| Dados estruturados | Sim |



| Processo repetitivo | Sim |



| Processo estável | Sim |



| Necessidade de julgamento humano | Baixa |



| Possibilidade de automação | Alta |



\## 5. Exceções



As transações que não apresentarem correspondência de CNPJ e valor deverão ser encaminhadas para análise manual.



\## 6. Saídas esperadas



\- Transações conciliadas automaticamente;



\- Lista de transações não conciliadas;



\- Registro do resultado da conciliação.



\## 7. PDD simplificado



1\. Baixar o extrato bancário em formato `.csv`.



2\. Abrir e ler os dados do extrato.



3\. Acessar os registros de baixa do ERP.



4\. Comparar CNPJ e valor das transações.



5\. Marcar as transações correspondentes como conciliadas.



6\. Separar as transações sem correspondência.



7\. Gerar o resultado da conciliação.



\## 8. Conclusão



O processo apresenta características adequadas para automação por RPA, pois possui regras claras, dados estruturados, atividades repetitivas e pouca dependência de decisões subjetivas. As exceções podem ser direcionadas para análise humana.

