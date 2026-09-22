Lab 05

1. Processo escolhido

Cenário A — Conciliação bancária diária

O processo consiste em comparar o extrato bancário em .csv com as baixas do ERP, usando CNPJ e valor.

2. Avaliação
Critério	               Resposta	                           Motivo
Regras claras                 sim                a comparação é feita por CNPJ e valor.
Dados estruturados	          Sim	             Os dados estão no .csv e no ERP.
Processo repetitivo	          Sim	             A conciliação é feita diariamente.
Julgamento humano	          Baixo 	         A maior parte da comparação segue regras fixas.
Viabilidade para RPA	      Sim	             O processo é padronizado e repetitivo.

3. PDD Simplificado

Objetivo

1 - Automatizar a conciliação entre o extrato bancário e o ERP.

2 - Entrada

3 - Extrato bancário em .csv

4 - Dados de baixas do ERP

5 - Processo

6 - Ler o arquivo .csv.

7 - Acessar o ERP.

8 - Buscar as baixas do período.

9 - Comparar CNPJ e valor.

10 - Identificar os registros que possuem correspondência.

11 - Separar os registros com divergências.

12 - Gerar um relatório final.

13 - Regras

14 - Se CNPJ e valor forem iguais, o lançamento é conciliado.

15 - Se o CNPJ ou valor for diferente, o lançamento é divergente.

16 - Casos que não puderem ser identificados automaticamente serão enviados para análise manual.

17 - Saída

18 - Um relatório contendo:

19 - Registros conciliados;

20 - Registros divergentes;

21 - Motivo da divergência.

4. Conclusão

O processo é viável para RPA, pois possui regras claras, dados estruturados e é realizado de forma repetitiva. A automação pode fazer a comparação automaticamente e deixar apenas as exceções para análise humana.