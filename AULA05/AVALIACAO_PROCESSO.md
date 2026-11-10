# Avaliação de Processo para RPA e PDD Simplificado

**Aluno:** RA 6326260  
**Atividade:** Lab 05 - Matriz de Viabilidade e PDD  

---

## 1. Avaliação dos Cenários

Abaixo está a comparação entre os dois cenários para saber qual deles vale a pena automatizar com RPA:

| Ponto de Análise | Cenário A (Conciliação Bancária) | Cenário B (Reembolso por Empatia) |
| :--- | :--- | :--- |
| **Tem regras claras?** | **Sim** (compara CNPJ e valor exato) | **Não** (depende de sentimento e contexto) |
| **Os dados são organizados?** | **Sim** (arquivo `.csv` e dados no ERP) | **Não** (histórico emocional e conversas) |
| **Precisa de julgamento humano?** | **Não** (é puramente lógico) | **Sim** (precisa de empatia e análise humana) |
| **É uma tarefa repetitiva?** | **Sim** (feita todos os dias) | **Não** (cada caso é de um jeito) |
| **Da pra fazer com RPA?** | **VIÁVEL (SIM)** | **INVIÁVEL (NÃO)** |

### Por que escolhi o Cenário A?
O **Cenário A** é perfeito para automação porque o robô só precisa seguir regras fixas: ler uma planilha `.csv` e conferir se o CNPJ e o valor batem com o que está no ERP. 

Já o **Cenário B** não dá para fazer com RPA básico. Robôs não têm sentimentos e não conseguem medir "empatia". Tentar automatizar algo assim só geraria erros e exigiria que uma pessoa refizesse o trabalho depois.

---

## 2. PDD Simplificado (Cenário A)

### 2.1 Resumo
* **Processo:** Conciliação Bancária Diária
* **Quem usa:** Equipe Financeira
* **Quando roda:** Todo dia de manhã
* **Sistemas:** Site do Banco, Sistema ERP e arquivos `.csv`

### 2.2 O que precisa antes de começar
* Login e senha do banco e do ERP salvos com segurança.
* O arquivo `.csv` do extrato bancário disponível.

### 2.3 Como o robô vai trabalhar (Passo a Passo)
1. **Baixar o extrato:** O robô entra no site do banco e baixa o `.csv` com as movimentações do dia anterior.
2. **Ler os dados:** Ele abre o arquivo e pega a data, o CNPJ e o valor de cada linha.
3. **Buscar no ERP:** O robô pesquisa no ERP se existe algum lançamento pendente com o mesmo CNPJ e valor.
4. **Dar baixa:**
   * **Se encontrar:** Ele marca o lançamento no ERP como "Conciliado".
   * **Se não encontrar:** Ele anota essa linha em uma lista de pendências.
5. **Avisar a equipe:** No final, o robô manda um e-mail para o financeiro mostrando o que foi conciliado e o que sobrou para conferência manual.

### 2.4 O que fazer se der problema?
* **Se o site do banco estiver fora do ar:** O robô tenta 3 vezes. Se continuar fora, ele manda um e-mail avisando a equipe e encerra.
* **Se o arquivo `.csv` não estiver lá:** O robô avisa por e-mail que o arquivo está faltando.
* **Se o valor não bater com o CNPJ:** O robô joga o item para a lista de exceções e segue para a próxima linha sem travar o processo.