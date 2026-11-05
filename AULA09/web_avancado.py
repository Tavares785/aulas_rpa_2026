"""
Lab 09 - Manipulação de Dropdowns, Pop-ups e Web Elements Complexos
Aluno: Icaro Ferrari de Senço - RA 1926102

Regras atendidas:
- Nenhum time.sleep(): toda sincronização usa WebDriverWait + expected_conditions.
- Cada parte em sua própria função.
- Ações validadas com assert e registradas com logging.
- try/except/finally garantindo driver.quit().
"""

import logging
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

RA = "1926102"
BASE_URL = "https://the-internet.herokuapp.com"
TIMEOUT = 10  # segundos máximos de espera explícita

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("lab09")


# ---------------------------------------------------------------------------
# Configuração do navegador
# ---------------------------------------------------------------------------
def criar_driver() -> webdriver.Chrome:
    """Cria o Chrome. Em ambiente de CI (GitHub Actions) roda em modo headless."""
    opcoes = webdriver.ChromeOptions()
    if os.getenv("CI") or os.getenv("HEADLESS"):
        opcoes.add_argument("--headless=new")
        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1366,768")
    return webdriver.Chrome(options=opcoes)


# ---------------------------------------------------------------------------
# Parte 1 - Selects
# ---------------------------------------------------------------------------
def parte_1_selects(driver):
    log.info("=== Parte 1: Selects ===")
    driver.get(f"{BASE_URL}/dropdown")
    wait = WebDriverWait(driver, TIMEOUT)

    elemento = wait.until(EC.presence_of_element_located((By.ID, "dropdown")))
    select = Select(elemento)

    # Lista todas as opções (inclui o placeholder "Please select an option")
    for i, opcao in enumerate(select.options):
        log.info("Opção [%d]: %s", i, opcao.text)

    # Índice 0 = placeholder, 1 = Option 1, 2 = Option 2
    select.select_by_index(2)

    selecionada = select.first_selected_option.text
    assert selecionada == "Option 2", f"Esperado 'Option 2', obtido '{selecionada}'"
    log.info("OK - opção selecionada: %s", selecionada)


# ---------------------------------------------------------------------------
# Parte 2 - Alerts JS (Alert, Confirm, Prompt)
# ---------------------------------------------------------------------------
def _ler_resultado(driver, wait, texto_esperado):
    """Espera o #result conter o texto esperado e devolve o texto lido."""
    wait.until(EC.text_to_be_present_in_element((By.ID, "result"), texto_esperado))
    return driver.find_element(By.ID, "result").text


def parte_2_alerts(driver):
    log.info("=== Parte 2: Alerts JS ===")
    driver.get(f"{BASE_URL}/javascript_alerts")
    wait = WebDriverWait(driver, TIMEOUT)

    # --- JS Alert: botões localizados apenas por XPath relativo ---
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Click for JS Alert']"))).click()
    alerta = wait.until(EC.alert_is_present())
    log.info("Texto do JS Alert: %s", alerta.text)
    assert alerta.text == "I am a JS Alert"
    alerta.accept()
    resultado = _ler_resultado(driver, wait, "You successfully clicked an alert")
    log.info("OK - %s", resultado)

    # --- JS Confirm: cancelar com dismiss() ---
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Click for JS Confirm']"))).click()
    confirmacao = wait.until(EC.alert_is_present())
    log.info("Texto do JS Confirm: %s", confirmacao.text)
    confirmacao.dismiss()
    resultado = _ler_resultado(driver, wait, "You clicked: Cancel")
    assert resultado == "You clicked: Cancel", f"Resultado inesperado: {resultado}"
    log.info("OK - %s", resultado)

    # --- JS Prompt: enviar o RA ---
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Click for JS Prompt']"))).click()
    prompt = wait.until(EC.alert_is_present())
    log.info("Texto do JS Prompt: %s", prompt.text)
    prompt.send_keys(RA)
    prompt.accept()
    resultado = _ler_resultado(driver, wait, RA)
    assert RA in resultado, f"RA não encontrado no resultado: {resultado}"
    log.info("OK - %s", resultado)


# ---------------------------------------------------------------------------
# Parte 3 - Iframes (editor TinyMCE)
# ---------------------------------------------------------------------------
def parte_3_iframe(driver):
    log.info("=== Parte 3: Iframe ===")
    driver.get(f"{BASE_URL}/iframe")
    wait = WebDriverWait(driver, TIMEOUT)

    # CSS Selector por atributo: qualquer iframe cujo id TERMINA com "_ifr"
    # (padrão do TinyMCE) -> não depende do ID fixo "mce_0_ifr".
    wait.until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[id$='_ifr']")))
    log.info("Foco trocado para o iframe do editor")

    corpo = wait.until(EC.presence_of_element_located((By.ID, "tinymce")))
    mensagem = f"Lab 09 - automação RPA - RA {RA}"

    # 1ª tentativa: digitar normalmente (clear + send_keys)
    try:
        corpo.clear()
        corpo.send_keys(mensagem)
    except Exception as erro:
        log.warning("send_keys não funcionou no editor: %s", erro)

    # A versão atual do site coloca o TinyMCE em modo somente leitura DEPOIS de
    # carregar, então o send_keys "passa" mas o texto não fica gravado.
    # Se isso acontecer, escrevemos direto no DOM do iframe via JavaScript.
    if RA not in (corpo.get_attribute("textContent") or ""):
        log.warning("Editor em modo somente leitura - escrevendo via JavaScript")
        driver.execute_script(
            "arguments[0].innerHTML = '';"
            "var p = document.createElement('p');"
            "p.textContent = arguments[1];"
            "arguments[0].appendChild(p);",
            corpo, mensagem,
        )

    # Espera explícita até o texto realmente estar no editor
    wait.until(lambda d: RA in (corpo.get_attribute("textContent") or ""))
    texto_editor = corpo.get_attribute("textContent")
    assert RA in texto_editor, f"Mensagem não gravada no editor: {texto_editor}"
    log.info("OK - texto no editor: %s", texto_editor)

    # Volta ao documento principal
    driver.switch_to.default_content()
    titulo = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert titulo == "An iFrame containing the TinyMCE WYSIWYG Editor", \
        f"h3 inesperado (ainda dentro do iframe?): {titulo}"
    log.info("OK - de volta ao DOM raiz, h3: %s", titulo)


# ---------------------------------------------------------------------------
# Parte 4 - Troca de abas / janelas
# ---------------------------------------------------------------------------
def parte_4_janelas(driver):
    log.info("=== Parte 4: Abas/Janelas ===")
    driver.get(f"{BASE_URL}/windows")
    wait = WebDriverWait(driver, TIMEOUT)

    handle_original = driver.current_window_handle
    titulo_original = driver.title
    log.info("Handle original: %s | título: %s", handle_original, titulo_original)

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
    wait.until(EC.number_of_windows_to_be(2))

    nova_aba = next(h for h in driver.window_handles if h != handle_original)
    driver.switch_to.window(nova_aba)
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h3"), "New Window"))
    texto = driver.find_element(By.TAG_NAME, "h3").text
    assert texto == "New Window", f"Texto inesperado na nova aba: {texto}"
    log.info("OK - nova aba exibe: %s", texto)

    driver.close()
    driver.switch_to.window(handle_original)

    assert len(driver.window_handles) == 1, "Ainda existem abas abertas"
    assert driver.title == titulo_original, f"Título inesperado: {driver.title}"
    h3 = driver.find_element(By.TAG_NAME, "h3").text
    assert h3 == "Opening a new window"
    log.info("OK - de volta à aba original (%s), 1 handle aberto", driver.title)


# ---------------------------------------------------------------------------
# Bônus - várias janelas abertas
# ---------------------------------------------------------------------------
def processar_novas_abas(driver, handle_original, handles):
    """
    Percorre todas as abas diferentes da original, lê o conteúdo de cada uma,
    fecha e sempre retorna à aba original. Devolve a lista de textos lidos.
    """
    wait = WebDriverWait(driver, TIMEOUT)
    conteudos = []
    for handle in handles:
        if handle == handle_original:
            continue
        driver.switch_to.window(handle)
        h3 = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
        log.info("Aba %s -> título '%s' | conteúdo '%s'", handle, driver.title, h3)
        conteudos.append(h3)
        driver.close()
    driver.switch_to.window(handle_original)
    return conteudos


def bonus_varias_janelas(driver, quantidade=3):
    log.info("=== Bônus: %d janelas ===", quantidade)
    driver.get(f"{BASE_URL}/windows")
    wait = WebDriverWait(driver, TIMEOUT)
    handle_original = driver.current_window_handle

    for i in range(quantidade):
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
        wait.until(EC.number_of_windows_to_be(i + 2))

    conteudos = processar_novas_abas(driver, handle_original, list(driver.window_handles))

    assert len(conteudos) == quantidade, f"Esperadas {quantidade} abas, lidas {len(conteudos)}"
    assert all(c == "New Window" for c in conteudos)
    assert driver.window_handles == [handle_original]
    log.info("OK - %d abas lidas e fechadas, foco na original", quantidade)


# ---------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------
def main() -> int:
    driver = None
    try:
        driver = criar_driver()
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframe(driver)
        parte_4_janelas(driver)
        bonus_varias_janelas(driver)
        log.info("Todas as partes concluídas com sucesso!")
        return 0
    except AssertionError as erro:
        log.error("Validação falhou: %s", erro)
        return 1
    except Exception as erro:
        log.exception("Erro inesperado: %s", erro)
        return 1
    finally:
        if driver:
            driver.quit()
            log.info("Navegador encerrado")


if __name__ == "__main__":
    sys.exit(main())
