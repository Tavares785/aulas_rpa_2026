# Ficha de Avaliação de RPA

## Cenário A

### 1. Nome do Processo

Conciliação Bancária Diária.

### 2. É viável para RPA?

**Sim.**

### 3. Justificativa baseada nos 4 critérios essenciais

- **Repetitividade:** O processo é realizado diariamente e segue as mesmas etapas de leitura e comparação das transações.

- **Regras de Negócio:** As regras são claras e objetivas, pois a conciliação é realizada por meio da comparação do CNPJ e do valor das transações.

- **Tipo de Dados:** Os dados são estruturados. O extrato bancário é disponibilizado em formato CSV e os registros do ERP possuem campos definidos para comparação.

- **Volume:** O processo pode envolver um grande número de transações, tornando a execução manual repetitiva e demorada. A automação permite processar essas informações de forma mais eficiente.

### 4. Mapeamento Passo a Passo das Ações do Robô

1. Iniciar a execução do robô.
2. Realizar o download do extrato bancário em formato CSV.
3. Abrir e ler os dados do arquivo CSV.
4. Acessar o sistema ERP.
5. Consultar as baixas registradas no ERP.
6. Comparar o CNPJ de cada transação do extrato com o CNPJ registrado no ERP.
7. Comparar o valor de cada transação com o valor registrado no ERP.
8. Identificar as transações que atendem às regras de conciliação.
9. Registrar as transações conciliadas e as divergências encontradas.
10. Gerar o resultado da conciliação.
11. Finalizar a execução do robô.