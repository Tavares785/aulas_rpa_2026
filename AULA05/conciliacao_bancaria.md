# Ficha de Avaliação de RPA

## Cenário
Cenário A – Conciliação bancária diária.

## 1. Nome do Processo
Conciliação Bancária Automatizada.

## 2. É viável para RPA?
Sim.

## 3. Justificativa baseada nos 4 critérios essenciais

### Repetitividade
A conciliação bancária é uma atividade realizada diariamente e que segue
praticamente os mesmos passos todos os dias. É necessário baixar o extrato,
verificar as transações e comparar essas informações com as baixas registradas
no ERP. Por ser um processo que se repete com frequência e segue uma sequência
bem definida, existe uma boa oportunidade para automatização.

### Regras de Negócio
As regras utilizadas para fazer a comparação são objetivas, já que são usados
dados como o CNPJ e o valor de cada transação. Dessa forma, o robô consegue
seguir critérios previamente definidos para verificar se uma movimentação
corresponde ou não a um registro existente no ERP, sem depender de uma
decisão subjetiva.

### Tipo de Dados
O extrato é disponibilizado em formato CSV, portanto os dados já possuem uma
estrutura que facilita sua leitura e processamento. Informações como CNPJ,
valor e outros dados da transação podem ser identificadas e comparadas com
os registros encontrados no ERP.

### Volume
Como esse processo acontece diariamente, ao longo do tempo existe uma
quantidade considerável de transações que precisam ser verificadas. Fazer
essas comparações manualmente pode consumir bastante tempo do responsável
pela atividade. Com a automação, o robô pode realizar a parte repetitiva da
conciliação e deixar para análise humana apenas os casos que apresentarem
alguma divergência.

## 4. Mapeamento Passo a Passo das Ações do Robô

1. Iniciar o processo de conciliação bancária.
2. Acessar o local onde o extrato bancário está disponível.
3. Fazer o download do extrato no formato CSV.
4. Ler os dados presentes no arquivo.
5. Consultar as baixas registradas no sistema ERP.
6. Percorrer as transações encontradas no extrato.
7. Identificar o CNPJ e o valor de cada transação.
8. Comparar essas informações com os registros existentes no ERP.
9. Caso os dados sejam correspondentes, marcar a transação como conciliada.
10. Caso exista alguma diferença, registrar a transação como uma divergência.
11. Gerar um relatório com as transações conciliadas e as divergências
encontradas.
12. Encerrar o processo.
