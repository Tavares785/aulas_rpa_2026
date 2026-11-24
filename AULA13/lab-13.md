# Lab 13: Arquitetura Orientada a Filas (Queue), Processamento Assíncrono e Resiliência

## 🎯 Objetivos de Aprendizagem
- Aplicar a arquitetura Produtor-Consumidor usando filas (`queue.Queue`).
- Entender o conceito de IO Assíncrono com a biblioteca `asyncio`.
- Configurar rotação avançada de logs corporativos usando `RotatingFileHandler`.
- Aplicar padrões de re-tentativa (*Retry Pattern*) com a biblioteca `tenacity` para auto-recuperação de erros de rede.

## 💼 Desafio de Mercado
Neste lab, você reaproveita o cenário do **Lab 07** (Lançamento de Notas): em vez de digitar nota a nota com `pyautogui`, o robô passa a trabalhar com uma fila de alunos e é resiliente a falhas. Processar milhares de registros (notas, faturas etc.) sequencialmente bloqueia o robô e desperdiça poder computacional. Caso haja instabilidade na internet, uma falha simples no meio da fila paralisa todo o pipeline sem rastreabilidade. A engenharia avançada de RPA resolve isso com arquitetura assíncrona, filas de tarefas independentes e logs rotativos de auditoria.

---

## 📝 Enunciado (Aluno)

Base de dados: `AULA07/notas_alunos.csv` (separador `;`, dados sujos: espaços extras, vírgula decimal, valores como `FALTOU`, `N/A` ou vazio).

1. Crie o arquivo `bot_faturamento_avancado.py` na pasta `AULA13`.
2. Configurar o `logging` para utilizar um `RotatingFileHandler` gravando no arquivo `app_rpa.log` com limite de 1MB por arquivo.
3. Implemente a arquitetura Produtor-Consumidor utilizando `queue.Queue`:
   - **Produtor**: Função que lê o CSV da AULA07 e adiciona na fila os 10 primeiros alunos.
   - **Consumidor**: Função worker que retira alunos da fila, limpa os dados e calcula a média de cada bimestre (nota peso 8 + TF peso 2). A média final é a média dos dois bimestres. Define **APROVADO** se média final >= 6, senão **REPROVADO**. Valores inválidos contam como 0.
4. Adicione um mecanismo de *Retry* usando `tenacity` na função que lança a nota no portal (simule o lançamento com falha aleatória de rede), com até 3 tentativas.

---



## 🚀 Entrega

1. No **seu fork**, crie uma branch a partir da `main` com o nome `lab13/SEU_RA` (ex: `lab13/123456`):
   ```bash
   git checkout main
   git pull origin main
   git checkout -b lab13/SEU_RA
   ```
2. Adicione e commite seus arquivos:
   ```bash
   git add .
   git commit -m "lab13: entrega RA SEU_RA"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin lab13/SEU_RA
   ```
4. No GitHub, abra um **Pull Request** do seu fork para o repositório do professor (`main`) com o título:
   ```
   [Lab13] Entrega - RA SEU_RA
   ```
5. Aguarde a validação do CI (GitHub Actions) e a revisão do professor.

---
