# Ficha de Avaliação de RPA

**Aluno:** João Pedro Brão · **RA:** 6326200

**Cenário:** A - Conciliação bancária diária a partir do extrato `.csv`, comparando as linhas com as baixas do ERP por regras fixas de CNPJ e valor.

## 1. Nome do Processo

Conciliação Bancária Diária (Extrato x ERP).

## 2. É viável para RPA? (Sim / Não)

**Sim.** O processo é um ótimo candidato para automação.

## 3. Justificativa baseada nos 4 critérios essenciais

| Critério | Atende? | Por quê |
|---|---|---|
| **Repetitividade** | Sim | É feito todo dia útil, sempre do mesmo jeito: baixar o extrato, abrir o ERP e comparar. |
| **Regras de Negócio** | Sim | A regra é fixa e objetiva: mesmo CNPJ e mesmo valor = conciliado. Não tem decisão "no feeling". |
| **Tipo de Dados** | Sim | Os dados são estruturados: o extrato vem em `.csv` e o ERP exporta um relatório em colunas. |
| **Volume** | Sim | São dezenas ou centenas de lançamentos por dia; fazer na mão toma tempo e gera erro. |

Como os quatro critérios são atendidos, o robô consegue fazer o trabalho sem precisar de julgamento humano, e o ganho (tempo + menos erro) é alto.

Já o **Cenário B** (reembolso médico decidido por "empatia e histórico emocional do paciente") **não seria viável**: a decisão é subjetiva, sem regra fixa que um robô consiga seguir.

## 4. Mapeamento Passo a Passo das Ações do Robô

1. Iniciar no horário agendado (ex.: 7h, todo dia útil) e registrar o início no log.
2. Acessar o internet banking (ou a pasta compartilhada) e baixar o extrato `.csv` do dia.
3. Acessar o ERP e exportar o relatório de baixas da mesma data.
4. Ler os dois arquivos e padronizar os campos (CNPJ só com números, valor com 2 casas decimais).
5. Para cada linha do extrato, procurar no relatório do ERP uma baixa com o **mesmo CNPJ e o mesmo valor**.
6. Se encontrar: marcar as duas linhas como **conciliadas**.
7. Se não encontrar: enviar a linha para a lista de **pendências**.
8. Se encontrar mais de uma baixa possível para a mesma linha: não decidir sozinho, mandar para pendências para conferência humana.
9. Gerar a planilha `conciliacao_AAAA-MM-DD.xlsx` com as abas "Conciliados" e "Pendências".
10. Enviar e-mail de resumo ao financeiro com a planilha anexada.
11. Registrar o fim no log, com a quantidade de linhas conciliadas e pendentes.

**Exceções previstas**

| Situação | Ação do robô |
|---|---|
| Extrato do dia ainda não disponível | Tentar de novo a cada 30 min até as 12h; depois avisar o financeiro. |
| Layout do `.csv` diferente do esperado | Parar e avisar a equipe de RPA (o banco mudou o arquivo). |
| Falha de login no banco ou no ERP | Tentar mais 2 vezes, registrar no log e avisar por e-mail. |
