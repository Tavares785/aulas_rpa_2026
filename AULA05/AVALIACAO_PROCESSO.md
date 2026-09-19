# Ficha de Avaliação de Viabilidade de RPA

**RA:** 6326020  
**Atividade:** TF 05  
**Cenário Escolhido:** Cenário A (Conciliação Bancária Diária)

---

## 1. Descrição do Processo
* **Nome do Processo:** Conciliação Bancária Diária
* **Objetivo:** Comparar os lançamentos do extrato bancário em formato `.csv` com os registros de baixas no sistema ERP, realizando a validação automática por meio de regras determinísticas.
* **Frequência:** Diária.

---

## 2. Análise de Viabilidade Técnica e Negócio

| Critério de Avaliação | Resultado | Observações / Justificativa |
| :--- | :--- | :--- |
| **Entradas Estruturadas** |  Sim | O extrato é exportado em formato tabular `.csv` padronizado. |
| **Regras Claras e Determinísticas** |  Sim | A validação baseia-se unicamente no confronto direto de CNPJ e Valor. |
| **Intervenção Humana / Subjetividade** | ❌ Não | Não há necessidade de julgamento subjetivo ou análise de sentimentos. |
| **Sistemas Estáveis** |  Sim | O portal bancário (download) e o sistema ERP possuem interfaces previsíveis. |
| **Potencial de Erro Humano** |  Alto | A validação manual de centenas de linhas é suscetível a falhas de atenção. |

---

## 3. Matriz de Recomendação de Automação

- [x] **Altamente Recomendado para RPA:** O processo possui alto volume, dados estruturados e regras 100% determinísticas.
- [ ] **Necessita de IA / IA Generativa (RPA + IPA):** O processo contém dados não estruturados ou decisões subjetivas.
- [ ] **Não Recomendado para Automação:** O processo é puramente baseado em decisões emocionais ou empáticas.

---

## 4. Passo a Passo do Robô (To-Be)
1. Acessar o sistema/portal bancário e efetuar o download do extrato do dia no formato `.csv`.
2. Ler a planilha `.csv` e extrair as colunas de CNPJ, Valor e Data.
3. Conectar ao sistema ERP e extrair a lista de baixas do dia.
4. Para cada linha do `.csv`, comparar com as baixas do ERP utilizando as regras fixas de cruzamento (`CNPJ_Extrato == CNPJ_ERP` **AND** `Valor_Extrato == Valor_ERP`).
5. Se houver correspondência exata: marcar o lançamento como **Conciliado** no ERP.
6. Se houver divergência: gerar um log de **Exceção** e notificar a equipe financeira via e-mail.