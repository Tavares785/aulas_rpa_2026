# Lab 03: Arquitetura Modular de Dados de Processamento

## 🎯 Objetivos de Aprendizagem
- Modelar entidades de negócio utilizando Dicionários e Listas.
- Modularizar o código do robô através de Funções com parâmetros e retornos explicitados.
- Construir um menu interativo e manipulador de dados dinâmico.

## 💼 Desafio de Mercado
Um sistema de RH necessita de uma automação que cadastre colaboradores em memória antes de enviá-los ao sistema legado. É necessário um módulo isolado que valide as entradas e estruture os dados do colaborador em dicionários padronizados.

---

## 📝 Enunciado (Aluno)

1. Crie um arquivo chamado `mod_rh.py` e nele desenvolva as seguintes funções:
   - `cadastrar_colaborador(nome: str, cargo: str, salario: float) -> dict`: Retorna um dicionário estruturado com as chaves `"nome"`, `"cargo"`, `"salario"`.
   - `exibir_colaboradores(lista_colaboradores: list) -> None`: Percorre a lista e imprime os colaboradores formatados.
2. Crie um script principal `main.py` contendo um loop `while True` para gerenciar um menu interativo com as opções: `1 - Cadastrar`, `2 - Listar`, `0 - Sair`.

---


## 🚀 Entrega

1. No **seu fork**, crie uma branch a partir da `master` com o nome `lab03/SEU_RA` (ex: `lab03/123456`):
   ```bash
   git checkout master
   git pull origin master
   git checkout -b lab03/SEU_RA
   ```
2. Adicione e commite seus arquivos:
   ```bash
   git add .
   git commit -m "lab03: entrega RA SEU_RA"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin lab03/SEU_RA
   ```
4. No GitHub, abra um **Pull Request** do seu fork para o repositório do professor (`master`) com o título:
   ```
   [Lab03] Entrega - RA SEU_RA
   ```
5. Aguarde a validação do CI (GitHub Actions) e a revisão do professor.

---
