# Lab 04: Resiliência do Bot — Persistência, Exceções e Trilha de Auditoria

## 🎯 Objetivos de Aprendizagem
- Manipular arquivos de texto (`.csv` / `.txt`) usando o gerenciador de contexto `with`.
- Tratar e isolar exceções comuns com blocos `try/except/finally`.
- Implementar logs estruturados com múltiplos níveis de severidade (`logging`).

## 💼 Desafio de Mercado
Em produção, os robôs rodam de forma não supervisionada (Unattended). Se ocorrer uma exceção não tratada, o processo morre sem deixar rastros. Você deve criar uma rotina resiliente de leitura de arquivo CSV com auditoria por logs.


## 📝 Enunciado (Aluno)

1. Crie o arquivo `processador_csv.py`.
2. Configure o módulo `logging` para gravar logs no arquivo `execucao_bot.log` e exibi-los no console, com formato contendo data, horário, nível do log e mensagem.
3. Desenvolva uma função `processar_arquivo(caminho: str)` que:
   - Abra o arquivo de caminho fornecido.
   - Utilize `try/except` para tratar a exceção `FileNotFoundError` (gravar log nivel `ERROR`).
   - Leia as linhas do arquivo e grave logs de nível `INFO` para cada linha lida.
   - Utilize o bloco `finally` para registrar o término da tentativa de processamento.


## 🚀 Entrega

1. No **seu fork**, crie uma branch a partir da `master` com o nome `lab04/SEU_RA` (ex: `lab04/123456`):
   ```bash
   git checkout master
   git remote add upstream HTTPS_OU_SSH_DO_REPOSITORIO_ORIGINAL
   git fetch upstream - ou se preferir "git pull upstream master"
   git checkout -b lab04/SEU_RA
   ```
2. Adicione e commite seus arquivos:
   ```bash
   git add .
   git commit -m "lab04: entrega RA SEU_RA"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin lab04/SEU_RA
   ```
4. No GitHub, abra um **Pull Request** do seu fork para o repositório do professor (`master`) com o título:
   ```
   [Lab04] Entrega - RA SEU_RA
   ```
5. Aguarde a validação do CI (GitHub Actions) e a revisão do professor.

---
