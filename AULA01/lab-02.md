# Lab 01: Setup do Ambiente Dev e Hello World do Bot

## 🎯 Objetivos de Aprendizagem
- Configurar o ambiente de desenvolvimento Python para RPA.
- Versionar scripts e gerenciar credenciais via GitHub.
- Compreender a tipagem de dados aplicada à automação.

## 💼 Desafio de Mercado
Um analista de operações gasta cerca de 30 minutos todos os dias verificando manualmente se as variáveis de ambiente e as credenciais do sistema de faturamento estão devidamente tipadas antes de rodar os scripts de fechamento. Você foi contratado para criar um script de verificação/inicialização de variáveis de ambiente do robô.

---

## 📝 Enunciado (Aluno)

1. Crie um script chamado `bot_initializer.py`.
2. Declare e inicialize as seguintes variáveis:
   - `BOT_NAME` (String): Nome do robô (ex: "RPA_FINANCEIRO_01").
   - `MAX_RETRIES` (Integer): Número máximo de tentativas de execução em caso de falha.
   - `EXECUTION_TIMEOUT` (Float): Tempo limite por tarefa em segundos.
   - `IS_PRODUCTION` (Boolean): Flag indicando se o ambiente é de produção.
3. Imprima no terminal uma mensagem de inicialização formatada, exibindo todos os valores configurados e a tipagem de cada variável utilizando a função `type()`.
4. Commit o código no seu repositório Git e suba PR para o GitHub (`aulas_rpa_2026`).

---