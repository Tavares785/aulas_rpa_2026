# Ficha de Avaliação de RPA

## Cenário: A — Conciliação Bancária Diária via CSV e ERP

---

## 1. Nome do Processo

**Conciliação Bancária Diária**
Download do extrato bancário em `.csv` e comparação com as baixas registradas no sistema ERP, utilizando regras fixas de CNPJ e valor.

---

## 2. É viável para RPA?

**Sim**

---

## 3. Justificativa baseada nos 4 critérios essenciais

| Critério | Avaliação | Justificativa |
|---|---|---|
| **Repetitividade** | ✅ Alta | O processo ocorre diariamente, seguindo sempre o mesmo fluxo: download do extrato → leitura do ERP → comparação → registro de divergências. |
| **Regras de Negócio** | ✅ Claras e fixas | A lógica de conciliação é determinística: uma linha do extrato bate com uma baixa do ERP se o CNPJ e o valor forem idênticos. Não há julgamento subjetivo. |
| **Tipo de Dados** | ✅ Estruturado | O extrato é um arquivo `.csv` com colunas bem definidas (data, CNPJ, valor, descrição) e o ERP expõe dados tabulares consultáveis via interface ou API. |
| **Volume** | ✅ Alto e justificável | Uma conciliação diária pode envolver centenas ou milhares de linhas, tornando a automação significativamente mais eficiente e menos sujeita a erros humanos do que o processo manual. |

**Conclusão:** O processo atende integralmente aos critérios de elegibilidade para RPA. A ausência de ambiguidade nas regras e o uso exclusivo de dados estruturados eliminam os principais riscos de falha em projetos de automação.

---

## 4. Mapeamento Passo a Passo das Ações do Robô

1. **Autenticar no portal bancário**
   - Acessar o portal do banco via navegador (ou API, se disponível).
   - Inserir credenciais armazenadas de forma segura (ex.: cofre de credenciais / variável de ambiente).

2. **Baixar o extrato do dia anterior**
   - Navegar até a seção de extratos.
   - Selecionar o período correspondente ao dia anterior.
   - Fazer o download do arquivo no formato `.csv`.
   - Salvar o arquivo em diretório local de trabalho.

3. **Acessar o sistema ERP**
   - Abrir o sistema ERP (via interface desktop ou web).
   - Autenticar com as credenciais do processo.

4. **Extrair as baixas registradas no ERP**
   - Navegar até o módulo de contas a pagar/receber.
   - Filtrar as baixas pelo mesmo período (dia anterior).
   - Exportar ou coletar os registros (CNPJ e valor) para comparação.

5. **Realizar a conciliação**
   - Para cada linha do extrato `.csv`:
     - Procurar no conjunto de baixas do ERP uma entrada com mesmo CNPJ **e** mesmo valor.
     - Se encontrado → marcar como **conciliado**.
     - Se não encontrado → registrar como **divergência**.

6. **Gerar relatório de resultado**
   - Criar um arquivo de saída (`.csv` ou `.xlsx`) contendo:
     - Itens conciliados com sucesso.
     - Itens com divergência, indicando o campo divergente (CNPJ ou valor ausente).

7. **Enviar notificação**
   - Enviar e-mail automático para o responsável financeiro com o relatório em anexo.
   - Destacar no corpo do e-mail a quantidade de itens conciliados e o total de divergências encontradas.

8. **Finalizar e registrar log de execução**
   - Salvar log com data/hora de execução, quantidade de registros processados e status final.
   - Encerrar as sessões abertas (portal bancário e ERP).
