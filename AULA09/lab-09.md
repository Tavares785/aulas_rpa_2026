# Lab 09: Manipulação de Dropdowns, Pop-ups e Web Elements Complexos

## 🎯 Objetivos de Aprendizagem
- Mapear elementos dinâmicos usando `XPath` e `CSS Selectors` avançados[cite: 9].
- Lidar com caixas de seleção suspensas através da classe `Select`[cite: 9].
- Trocar contexto de execução para operar dentro de `Iframes`[cite: 9].
- Capturar, aceitar ou rejeitar caixas de diálogo nativas do navegador (`Alerts`)[cite: 9].
- Controlar **múltiplas abas/janelas** com `window_handles` e `switch_to.window`.
- Sincronizar o robô com `WebDriverWait` + `expected_conditions` (Esperas Explícitas).

## 💼 Desafio de Mercado
A maioria das aplicações corporativas web possui seletores dinâmicos, janelas modais de confirmação, estruturas aninhadas em `iframes`, formulários com dropdowns e fluxos que **abrem novas abas/janelas** (relatórios, comprovantes, portais externos)[cite: 9]. Dominar essas interações — e sincronizá-las corretamente com esperas explícitas — é crucial para criar automações web resilientes em sistemas legados.

---

## 📝 Enunciado (Aluno)

> ⚠️ **Regras obrigatórias (valem para todas as partes):**
> - **Proibido usar `time.sleep()` como forma de sincronização.** Use exclusivamente `WebDriverWait` com `expected_conditions`. O `sleep` só é tolerado para efeito visual didático, nunca para "esperar carregar".
> - Encapsule cada parte em **sua própria função** (`parte_1_selects(driver)`, `parte_2_alerts(driver)`, etc.).
> - Toda ação relevante deve ser **validada por `assert`** (ex: conferir que a opção realmente ficou selecionada) e registrada via `logging` (não apenas `print`).
> - Use `try/except/finally` garantindo o `driver.quit()` no `finally`.

1. Crie o script `web_avancado.py`[cite: 9].

2. **Parte 1 (Selects — com validação):** Acesse `https://the-internet.herokuapp.com/dropdown`[cite: 9]. Utilizando a classe `Select`:
   - Liste no terminal **todas** as opções disponíveis do dropdown (`select.options`).
   - Selecione a **"Option 2"** pelo *índice* (não pelo texto).
   - Valide com `assert` que `select.first_selected_option.text == "Option 2"`.

3. **Parte 2 (Alerts JS — os três tipos):** Acesse `https://the-internet.herokuapp.com/javascript_alerts`[cite: 9]. Localize os botões **apenas por XPath relativo** (sem usar IDs prontos). Execute, nesta ordem:
   - **JS Alert:** dispare, capture o texto, confirme com `accept()`.
   - **JS Confirm:** dispare e **cancele** com `dismiss()`. Em seguida, leia o `#result` da página e valide com `assert` que o texto indica *"You clicked: Cancel"*.
   - **JS Prompt:** dispare, **envie seu RA** como texto (`alert.send_keys(...)`), confirme com `accept()` e valide com `assert` que o `#result` contém o RA digitado.

4. **Parte 3 (Iframes — editor rico):** Acesse `https://the-internet.herokuapp.com/iframe`[cite: 9]. Troque o foco para o iframe do editor (localize-o **por CSS Selector**, não pelo ID fixo `mce_0_ifr`), limpe o conteúdo, escreva uma mensagem contendo seu RA, **retorne ao documento principal** (`default_content()`) e, de volta no DOM raiz, leia o cabeçalho `<h3>` da página para confirmar que você saiu do iframe (`assert` no texto do `<h3>`).

5. **Parte 4 (Troca de Abas / Janelas — NOVO):** Acesse `https://the-internet.herokuapp.com/windows`[cite: 9]. Esta é a parte central do desafio:
   - Guarde o *handle* da aba original (`driver.current_window_handle`).
   - Clique no link **"Click Here"**, que abre uma **nova aba**.
   - Usando `WebDriverWait`, espere até existirem **2 handles** (`EC.number_of_windows_to_be(2)`).
   - Faça o robô **trocar o foco** para a nova aba (o handle diferente do original) e valide com `assert` que o texto exibido é **"New Window"**.
   - **Feche** a nova aba (`driver.close()`) e **retorne o foco** para a aba original (`switch_to.window(handle_original)`).
   - Valide com `assert` que, ao final, só existe **1 handle** e que o título da página voltou a ser o da página de janelas.

6. **(Bônus — opcional, +pontos):** Transforme a Parte 4 para o cenário em que o clique abre **duas ou mais** janelas. Escreva uma função genérica que receba a lista de handles, percorra **todas** as abas novas, leia o conteúdo de cada uma e feche-as, retornando sempre à aba original de forma segura.


## 🚀 Entrega

1. No **seu fork**, crie uma branch a partir da `main` com o nome `lab09/SEU_RA` (ex: `lab09/123456`):
   ```bash
   git checkout main
   git pull origin main
   git checkout -b lab09/SEU_RA
   ```
2. Adicione e commite seus arquivos:
   ```bash
   git add .
   git commit -m "lab09: entrega RA SEU_RA"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin lab09/SEU_RA
   ```
4. No GitHub, abra um **Pull Request** do seu fork para o repositório do professor (`main`) com o título:
   ```
   [Lab09] Entrega - RA SEU_RA
   ```
5. Aguarde a validação do CI (GitHub Actions) e a revisão do professor.

---
