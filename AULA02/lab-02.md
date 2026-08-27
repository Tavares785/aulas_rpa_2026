# Lab 02: Motor de Tomada de Decisão e Resiliência de Repetição

## 🎯 Objetivos de Aprendizagem
- Aplicar estruturas condicionais (`if`, `elif`, `else`) para regras de negócio.
- Utilizar estruturas de repetição (`for`, `while`) para processamento em lote.
- Implementar controle de fluxo avançado com `break` e `continue`.

## 💼 Desafio de Mercado
Em um processo bancário, o bot deve analisar uma fila de transações financeiras pendentes. Caso encontre um valor suspeito (acima de R$ 10.000,00), ele deve sinalizar para auditoria humana e continuar; caso encontre uma transação com valor negativo ou inválido (status "ERRO"), a execução da fila deve ser interrompida imediatamente para manutenção.

---

## 📝 Enunciado (Aluno)

Dado a seguinte lista de transações:
`transacoes = [150.0, 3200.5, 12500.0, 450.0, -50.0, 800.0, 0]`

Crie um script `validador_transacoes.py` que:
1. Percorra a lista de transações usando um laço `for`.
2. Se a transação for maior que `10000.00`, exiba a mensagem: `"[ALERTA] Transação suspeita de R$ <VALOR>: Encaminhada para auditoria."` e utilize `continue`.
3. Se a transação for menor ou igual a `0`, exiba a mensagem: `"[ERRO CRÍTICO] Transação inválida encontrada (R$ <VALOR>). Interrompendo bot..."` e encerre o loop com `break`.
4. Para transações normais, exiba: `"[SUCESSO] Transação de R$ <VALOR> processada."`

---


## 🚀 Entrega

1. No **seu fork**, crie uma branch a partir da `main` com o nome `lab02/SEU_RA` (ex: `lab02/123456`):
   ```bash
   git checkout main
   git pull origin main
   git checkout -b lab02/SEU_RA
   ```
2. Adicione e commite seus arquivos:
   ```bash
   git add .
   git commit -m "lab02: entrega RA SEU_RA"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin lab02/SEU_RA
   ```
4. No GitHub, abra um **Pull Request** do seu fork para o repositório do professor (`main`) com o título:
   ```
   [Lab02] Entrega - RA SEU_RA
   ```
5. Aguarde a validação do CI (GitHub Actions) e a revisão do professor.

---
