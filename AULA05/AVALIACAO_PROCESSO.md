# Ficha de Avaliação de RPA

## Cenário escolhido

**Cenário A:** conciliação bancária diária a partir do extrato CSV e das baixas registradas no ERP.

## 1. Nome do processo

Conciliação bancária diária por CNPJ e valor.

## 2. É viável para RPA?

**Sim**, desde que o extrato e os dados do ERP sigam formatos estáveis e que divergências sejam encaminhadas para análise humana, sem o robô decidir exceções fora das regras definidas.

## 3. Justificativa pelos critérios essenciais

| Critério | Avaliação |
| --- | --- |
| Repetitividade | Alta. A atividade é executada diariamente e repete as mesmas etapas para cada lançamento. |
| Regras de negócio | Claras. A conciliação compara CNPJ e valor conforme regras fixas. Registros sem correspondência, duplicados ou divergentes devem ser separados para revisão humana. |
| Tipo de dados | Estruturados. O extrato CSV e os registros do ERP possuem campos que podem ser lidos e comparados, como CNPJ e valor. |
| Volume | Adequado. O processamento em lote de muitos lançamentos reduz o trabalho manual e mantém o mesmo critério para todos os registros. |

## 4. Mapeamento passo a passo das ações do robô

1. Iniciar a execução e registrar data, horário e identificador do processamento no log.
2. Localizar e baixar o extrato bancário CSV do período definido.
3. Validar a existência do arquivo, o formato esperado e a presença dos campos necessários; interromper com registro de erro se houver falha.
4. Acessar o ERP e obter as baixas do mesmo período.
5. Normalizar os valores de CNPJ e valor para comparação, sem alterar os arquivos de origem.
6. Comparar cada lançamento do extrato com as baixas do ERP usando as regras fixas de CNPJ e valor.
7. Registrar como conciliados os pares que atendem às regras; separar lançamentos sem correspondência, duplicados ou divergentes para análise humana.
8. Salvar um relatório com os totais processados, conciliados e pendentes, mantendo referência aos registros de origem.
9. Registrar o resultado final no log e encerrar a execução, sinalizando falhas para acompanhamento.

## Premissas e controles

- O arquivo CSV e os campos do ERP mantêm um formato conhecido e estável.
- O acesso ao banco e ao ERP é autorizado e protegido conforme as políticas da empresa.
- O robô não cria baixas nem altera valores: apenas compara e registra resultados.
- Exceções e divergências permanecem pendentes até a validação de uma pessoa responsável.