# Lab 07: Projeto — Sistema de Lançamento de Notas

## 🎯 Objetivos de Aprendizagem
- Integrar lógica de dados em memória (listas de dicionários) com automação desktop.
- Construir formulários simulados de entrada e atalhos de navegação.
- Calcular e exibir estatísticas.

## 💼 Desafio de Mercado
Coordenadores pedagógicos gastam horas digitando manualmente notas de turmas em portais acadêmicos antigos que não oferecem suporte a upload de planilhas.

---

## Cenário: Fechamento de Semestre

Fim de semestre na faculdade. O professor possui uma planilha no Excel com as notas finais de 300 alunos. Ele precisa lançar essas notas em um Sistema Acadêmico Legado (Portal do Professor) que não permite importação de arquivos.

A dor manual: Olhar a linha no Excel, digitar a matrícula no sistema, esperar carregar, digitar a nota, clicar em salvar e repetir o processo centenas de vezes.


## FASE 1: MAPEANDO O PROCESSO

- Regra de Ouro: Se o humano não sabe o passo a passo, o robô também não saberá.

- Preparação do Ambiente: Garantir que o Sistema esteja criado (Formulario e link Planilha, GitHub do projeto)

- Lançamento e Validação: Preencher Nota Final, peso 8, TF peso 2,  verificar se o aluno foi aprovado/reprovado e salvar o registro.

- Busca pelo Aluno: Automação precisa trazer as informações pesquisando por RA ou Nome'.

## FASE 3: DADOS DE TESTE

O cliente, disponibilizara um arquivo com as notas dos alunos
Nome;RA;Nota01;TF01;Notao2;TF02


## FASE 4: O CORAÇÃO DO ROBÔ

Usaremos o for para iterar sobre cada aluno. O comando pyautogui é nossa melhor estratégia para a automação pedida

.63   REPROVADO
100078   7.66  APROVADO
100079   2.22  REPROVADO36 APROVADO
100081
100080   6.## FASE 5: Entrega

1. No **seu repo**, crie um repo Nome_projeto+ SEU_RA ou aula_07 + SEU_RA `(ex: projeto_lancamento_nota_123456)`:
2. Adicione e commite seus arquivos:   3.34  REPROVADO
100082   4.6   REPROVADO

   ```bash
   git add .
   git commit -m "lab07: Entrega Projeto Notas"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin seu repo
   ```
4. Preencha o form com as informações solicitadas:
   https://docs.google.com/forms/d/e/1FAIpQLScobs8AluooQSGYT-wIZSbDl2EseRKzaaTBpG7NjwDeQiENZw/viewform?usp=publish-editorREPROVA
5. Aguarde revisão do professor e Nota.

---
