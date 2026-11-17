# Desafio de Automação Web Avançada com Selenium WebDriver

Script desenvolvido para atender a todos os requisitos do desafio com validação rigorosa e boas práticas de automação.

## Arquivos
- [`web_avancado.py`] Script principal contendo as 4 partes e o bônus implementados e encapsulados em funções modulares.

---

## Regras Obrigatórias Atendidas
1. **Sincronização Exclusiva**: Uso estrito de `WebDriverWait` com `expected_conditions` (sem `time.sleep` para espera de carregamento).
2. **Encapsulamento Modular**: Cada parte em sua própria função (`parte_1_selects`, `parte_2_alerts`, `parte_3_iframes`, `parte_4_windows`, `parte_bonus_multiplas_janelas`).
3. **Validação com `assert` e Rastreamento com `logging`**: Todas as ações relevantes possuem asserções com mensagens explicativas e logs em tempo real.
4. **Tratamento de Exceções**: Bloco `try/except/finally` com `driver.quit()` garantido no `finally`.
5. **Seletores Específicos**:
   - Alertas JS localizados exclusivamente por **XPath relativo**.
   - Iframe localizado exclusivamente por **CSS Selector** (sem usar o ID fixo `mce_0_ifr`).
6. **Bônus**: Função genérica `fechar_abas_secundarias_e_retornar` capaz de lidar com 2 ou mais novas abas, capturando conteúdo e retornando com segurança à aba de origem.

---

## Como Executar

### 1. Execução padrão (Modo Headless, RA padrão `RA12345678`):
```bash
python web_avancado.py
```

### 2. Informando o seu próprio RA:
```bash
python web_avancado.py --ra 123456789
```

### 3. Execução com navegador visível (interface gráfica aberta):
```bash
python web_avancado.py --no-headless --ra 123456789
```

### 4. Ajustando o tempo limite do `WebDriverWait`:
```bash
python web_avancado.py --timeout 15
```

