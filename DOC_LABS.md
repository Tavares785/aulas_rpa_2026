# Labs - Automação Robótica de Processos (RPA) com Python

Repositório de laboratórios práticos da disciplina de **RPA (2º ano)**.

Cada aula (01 a 14) tem sua própria pasta com o enunciado do lab e, quando
aplicável, **correção automática (CI/CD)** via GitHub Actions que roda em
toda Pull Request usando `flake8` (lint/PEP8) e `pytest`.

## Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/) instalado na sua máquina
- [Git](https://git-scm.com/) para clonar o repositório e enviar suas alterações
- Uma conta no GitHub
- Editor recomendado: [VS Code](https://code.visualstudio.com/)

## Labs disponíveis

| Pasta | Aula | Enunciado | Gabarito | O que é avaliado |
|---|---|---|---|---|
| `AULA01/` | Setup do Ambiente e Hello World do Bot | `lab-01.md` | `lab-01_resp.md` | Variáveis, tipagem e inicialização (`bot_initializer.py`) |
| `AULA02/` | Motor de Decisão e Resiliência de Repetição | `lab-02.md` | `lab-02_resp.md` | Condicionais e laços (`validador_transacoes.py`) |
| `AULA03/` | Arquitetura Modular de Dados | `lab-03.md` | `lab-03_resp.md` | Funções, dicionários e menu (`mod_rh.py` + `main.py`) |
| `AULA04/` | Persistência, Exceções e Auditoria | `lab-04.md` | `lab-04_resp.md` | Arquivos, `try/except` e `logging` (`processador_csv.py`) |
| `AULA05/` | Matriz de Viabilidade e PDD | `lab-05.md` | `lab-05_resp.md` | Ficha de avaliação de RPA (`AVALIACAO_PROCESSO.md`) |
| `AULA06/` | Controle de Periféricos e Fail-Safe | `lab-06.md` | `lab-06_resp.md` | Automação desktop com PyAutoGUI (`notepad_bot.py`) |
| `AULA07/` | Projeto Guiado: Lançamento de Notas | `lab-07.md` | `lab-07_resp.md` | Automação de formulário com teclado (`lancador_notas.py`) |
| `AULA08/` | Web Scraping com Selenium | `lab-08.md` | `lab-08_resp.md` | Login web automatizado (`bot_web_login.py`) |
| `AULA09/` | Dropdowns, Pop-ups e Iframes | `lab-09.md` | `lab-09_resp.md` | Selects, alerts e iframes (`web_avancado.py`) |
| `AULA10/` | Extração de PDFs, Regex e Excel | `lab-10.md` | `lab-10_resp.md` | Regex + Pandas + Excel (`leitor_faturas_pdf.py`) |
| `AULA11/` | Web Scraping com BeautifulSoup | `lab-11.md` | `lab-11_resp.md` | Requests + BeautifulSoup + CSV (`scraper_noticias.py`) |
| `AULA12/` | APIs REST e Notificações por E-mail | `lab-12.md` | `lab-12_resp.md` | Consumo de API + SMTP (`bot_cotacao_alerta.py`) |
| `AULA13/` | Filas, Assíncrono e Resiliência | `lab-13.md` | `lab-13_resp.md` | Produtor-Consumidor + Retry (`bot_faturamento_avancado.py`) |
| `AULA14/` | Arquitetura, Gitignore e Repositório | `lab-14.md` | `lab-14_resp.md` | Estrutura do projeto final (`rpa-projeto-final/`) |

> Os arquivos `lab-XX_resp.md` são **gabaritos/materiais do professor**. Os
> alunos devem trabalhar a partir do enunciado em `lab-XX.md`.

## Estrutura do repositório

```
Aulas_RPA/
├── AULA01/ ... AULA14/     <- Uma pasta por aula
│   ├── lab-XX.md           <- Enunciado da atividade (aluno)
│   └── lab-XX_resp.md      <- Gabarito comentado (professor)
├── tests/                  <- Correção automática (NÃO EDITAR)
├── .github/workflows/      <- Pipelines de CI por aula
├── requirements.txt        <- Dependências Python
├── pytest.ini              <- Configuração do pytest
└── DOC_LABS.md             <- Este arquivo
```

## Como fazer um lab (passo a passo)

### 1. Fork e Clone

```bash
# Faça o Fork pelo GitHub (botão "Fork" no canto superior direito).
# Depois clone o SEU fork:
git clone https://github.com/SEU-USUARIO/Aulas_RPA.git
cd Aulas_RPA
```

### 2. Prepare o ambiente Python

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3. Crie uma branch para o lab

Use o padrão `labXX/SEU_RA` (ex: `lab02/123456`):

```bash
git checkout master
git pull origin master
git checkout -b lab02/SEU_RA
```

### 4. Edite o código

Abra o enunciado em `AULAXX/lab-XX.md` e implemente o que é pedido. Crie o(s)
arquivo(s) `.py` indicados no enunciado.

### 5. Teste localmente

```bash
# Rode o lint (mesmo do CI):
flake8 AULA02/ --max-complexity=10 --max-line-length=127

# Rode os testes da aula correspondente:
pytest tests/test_aula02.py -v

# Ou rode toda a suíte:
pytest -v
```

### 6. Envie e abra uma PR

```bash
git add .
git commit -m "lab02: entrega RA SEU_RA"
git push origin lab02/SEU_RA
```

Abra uma **Pull Request** do seu fork para o repositório do professor
(branch `master`), com o título no padrão:

```
[Lab02] Entrega - RA SEU_RA
```

O GitHub Actions roda a correção automaticamente na PR.

### 7. Registre a entrega no formulário

Além da PR, preencha o **Google Forms** de entrega informando:

- Seu **RA**
- O **link da sua Pull Request** no GitHub

### 8. Aguarde o resultado

- ✅ = Todos os checks passaram — parabéns!
- ❌ = Algo falhou — clique em "Details" para ver o que quebrou (lint ou testes)

Se algo falhar, corrija o código, faça `commit` + `push` de novo na mesma
branch, e o CI roda novamente automaticamente.

## Como a correção automática funciona

1. Ao abrir (ou atualizar) uma PR para a `master`, o GitHub Actions detecta
   quais pastas de aula foram alteradas (via `paths`).
2. O workflow correspondente configura o Python (3.10 e 3.11), instala as
   dependências de `requirements.txt` e roda:
   - **`flake8`** para validar sintaxe e PEP8.
   - **`pytest`** com os testes da aula em `tests/`.
3. O resultado é publicado como um "check" na PR.

## Para o professor: exigir que o CI passe antes do merge

No GitHub, vá em **Settings → Branches → Branch protection rules** para a
branch `master` e ative:

- "Require status checks to pass before merging"
- Selecione os checks de lint/testes de cada workflow de aula

Isso impede que uma PR seja mesclada enquanto os testes não passarem.
