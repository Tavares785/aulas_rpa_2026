Cenário: A

1. Nome do Processo 
Conciliação bancária diária.

2. É viável para RPA? (Sim / Não)
Sim
3. Justificativa baseada nos 4 critérios essenciais (Repetitividade, Regras de Negócio, Tipo de Dados, Volume).
- Repetividade: O processo de repetividade é realizado diariamente, assim ele vai começar a exata mesma etapa para novos extratos bancários.

- Regras de Negócio: Para realizar a conciliação, será necessario entender as regras objetivas. Principalmente aquelas como comparação de CNPJ e do valor entre o extrato bancário e as baixas que são registradas no sistema ERP.

- Tipos de Dados: Os dados tem de ser estruturados, para assim ser usado, pelo fato de o extrato ser disponibilizado em formato ".csv" e As informações do sistema ERP também contém organização, como CNPJ, valor e data.

- Volume: A conciliação pode envolver uma grande quantidade de transações diariamente. A utilização de RPA pode acelerar a comparação dos registros e reduzir o trabalho manual.

4. Mapeamento Passo a Passo das Ações do Robô

. Iniciar o processo diariamente.
. Acessar o sistema ou ambiente onde está disponível o extrato bancário.
. Baixar o extrato bancário em formato `.csv`.
. Ler os dados do arquivo `.csv`.
. Acessar o sistema ERP.
. Consultar as baixas registradas no ERP.
. Comparar o CNPJ do extrato bancário com o CNPJ registrado no ERP.
. Comparar o valor da transação do extrato com o valor da baixa no ERP.
. Se o CNPJ e o valor forem iguais, marcar a transação como conciliada.
. Se não houver correspondência, marcar a transação como divergente.
. Separar as transações divergentes para análise manual.
. Gerar um relatório com as transações conciliadas e as divergências.
. Finalizar o processo.