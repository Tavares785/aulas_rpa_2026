Cenário: **A - Conciliação Bancária Diária**

## 1. Nome do Processo
Conciliação Bancária Diária (Extrato CSV x Baixas ERP)

## 2. É viável para RPA?
**Sim.**

## 3. Justificativa baseada nos 4 critérios essenciais

- **Repetitividade:** O processo é executado diariamente, sempre com a mesma sequência de passos (baixar extrato, ler linhas, comparar, apontar divergências). Alta repetitividade favorece a automação.
- **Regras de Negócio:** A comparação é feita por regras fixas e determinísticas (CNPJ e valor), sem necessidade de julgamento subjetivo ou interpretação humana. Regras claras e objetivas são o principal requisito de elegibilidade.
- **Tipo de Dados:** O processo trabalha com dados estruturados — um arquivo `.csv` (extrato bancário) e registros do sistema ERP, ambos em formato tabular/campo-a-campo, facilmente lidos e processados por um robô.
- **Volume:** Processos diários de conciliação tendem a ter volume considerável de linhas/transações, o que gera ganho real de eficiência e redução de erro humano ao automatizar, justificando o investimento em RPA.

## 4. Mapeamento Passo a Passo das Ações do Robô

1. Acessar o portal/sistema do banco (ou pasta de rede/e-mail) e baixar o extrato bancário do dia em formato `.csv`.
2. Abrir e ler o arquivo `.csv`, extraindo as colunas relevantes (data, CNPJ, valor, descrição da transação).
3. Acessar o sistema ERP e extrair (via consulta, relatório ou API) a lista de baixas/lançamentos pendentes do mesmo período.
4. Para cada linha do extrato bancário, buscar no ERP um lançamento correspondente com **mesmo CNPJ e mesmo valor**.
5. Quando encontrar correspondência exata, marcar a transação como **conciliada** (baixar automaticamente no ERP, se aplicável).
6. Quando não encontrar correspondência, marcar a transação como **divergência/pendência**.
7. Gerar um relatório (ex.: planilha ou log) com o resumo do dia: total de linhas processadas, total conciliado e total de pendências.
8. Enviar o relatório por e-mail (ou salvar em pasta compartilhada) para o time financeiro revisar as divergências apontadas.
9. Registrar log de execução do robô (sucesso, erros, horário de início/fim) para fins de auditoria.