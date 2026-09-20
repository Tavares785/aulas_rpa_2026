# Lab 05: Matriz de Viabilidade e PDD (Process Definition Document)

## 🎯 Objetivos de Aprendizagem
- Analisar processos corporativos e determinar se são elegíveis a RPA.
- Estruturar um documento simplificado de especificação técnica (PDD).
- Aplicar critérios de seleção: regras claras, dados estruturados e repetibilidade.

## 💼 Desafio de Mercado
Muitos projetos de automação falham por tentarem automatizar processos instáveis ou dependentes do julgamento subjetivo humano. O analista/desenvolvedor de RPA deve saber filtrar o backlog de automação.

---

## 📝 Enunciado (Aluno)

Escolha **um** dos dois cenários abaixo e preencha a **Ficha de Avaliação de RPA** em Markdown no arquivo `AVALIACAO_PROCESSO.md`:

- **Cenário A:** Conciliação bancária diária feita a partir do download do extrato `.csv` e comparação das linhas com as baixas do sistema ERP via regras fixas de CNPJ e valor.
- **Cenário B:** Triagem de solicitações de reembolso de despesas médicas onde a decisão de autorizar é baseada na "análise de empatia e histórico emocional do paciente".

---


## 🚀 Entrega

1. No **seu fork**, crie uma branch a partir da `master` com o nome `lab05/SEU_RA` (ex: `lab05/123456`):
   ```bash
   git checkout master
   git pull origin master
   git checkout -b lab05/SEU_RA
   ```
2. Adicione e commite seus arquivos:
   ```bash
   git add .
   git commit -m "lab05: entrega RA SEU_RA"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin lab05/SEU_RA
   ```
4. No GitHub, abra um **Pull Request** do seu fork para o repositório do professor (`master`) com o título:
   ```
   [Lab05] Entrega - RA SEU_RA
   ```
5. Aguarde a validação do CI (GitHub Actions) e a revisão do professor.

---
