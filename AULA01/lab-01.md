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
---

## 🚀 Entrega

1. No **seu fork**, crie uma branch a partir da `main` com o nome `lab01/SEU_RA` (ex: `lab01/123456`):
   ```bash
   git checkout main
   git pull origin main
   git checkout -b lab01/SEU_RA
   ```
2. Adicione e commite seus arquivos:
   ```bash
   git add .
   git commit -m "lab01: entrega RA SEU_RA"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin lab01/SEU_RA
   ```
4. No GitHub, abra um **Pull Request** do seu fork para o repositório do professor (`main`) com o título:
   ```
   [Lab01] Entrega - RA SEU_RA
   ```
5. Aguarde a validação do CI (GitHub Actions) e a revisão do professor.

---