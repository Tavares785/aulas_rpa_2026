"""
web_avancado.py

Instalação:
    pip install selenium
"""

import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# >>> TROQUE PELO SEU RA <<<
RA = "6326205"

BASE = "https://the-internet.herokuapp.com"
TIMEOUT = 10

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


def esperar(driver, condicao, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(condicao)


# ---------------------------------------------------------------- Parte 1
def parte_1_selects(driver):
    log.info("=== PARTE 1: Selects ===")
    driver.get(f"{BASE}/dropdown")

    elemento = esperar(driver, EC.element_to_be_clickable((By.ID, "dropdown")))
    select = Select(elemento)

    log.info("Opções disponíveis:")
    for opcao in select.options:
        log.info(" - %s", opcao.text)
        print(opcao.text)

    select.select_by_index(2)
    selecionada = select.first_selected_option.text
    log.info("Opção selecionada: %s", selecionada)
    assert selecionada == "Option 2", f"Esperava 'Option 2', veio '{selecionada}'"
    log.info("Parte 1 validada com sucesso")


# ---------------------------------------------------------------- Parte 2
def _ler_result(driver):
    return esperar(driver, EC.visibility_of_element_located((By.ID, "result"))).text


def parte_2_alerts(driver):
    log.info("=== PARTE 2: Alerts JS ===")
    driver.get(f"{BASE}/javascript_alerts")

    # --- JS Alert
    esperar(
        driver,
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'JS Alert')]")),
    ).click()
    alerta = esperar(driver, EC.alert_is_present())
    log.info("Texto do alert: %s", alerta.text)
    assert alerta.text == "I am a JS Alert", f"Texto inesperado: {alerta.text}"
    alerta.accept()
    resultado = _ler_result(driver)
    assert "You successfully clicked an alert" in resultado, resultado
    log.info("JS Alert validado: %s", resultado)

    # --- JS Confirm (cancelar)
    esperar(
        driver,
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'JS Confirm')]")),
    ).click()
    alerta = esperar(driver, EC.alert_is_present())
    log.info("Texto do confirm: %s", alerta.text)
    alerta.dismiss()
    resultado = _ler_result(driver)
    assert "You clicked: Cancel" in resultado, resultado
    log.info("JS Confirm validado: %s", resultado)

    # --- JS Prompt (enviar RA)
    esperar(
        driver,
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'JS Prompt')]")),
    ).click()
    alerta = esperar(driver, EC.alert_is_present())
    log.info("Texto do prompt: %s", alerta.text)
    alerta.send_keys(RA)
    alerta.accept()
    resultado = _ler_result(driver)
    assert RA in resultado, f"RA '{RA}' não encontrado em: {resultado}"
    log.info("JS Prompt validado: %s", resultado)


# ---------------------------------------------------------------- Parte 3
def parte_3_iframes(driver):
    log.info("=== PARTE 3: Iframes ===")
    driver.get(f"{BASE}/iframe")

    # Troca o foco para o iframe localizado por CSS Selector (sem ID fixo)
    esperar(
        driver,
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe.tox-edit-area__iframe")
        ),
    )
    log.info("Foco trocado para o iframe do editor")

    corpo = esperar(driver, EC.element_to_be_clickable((By.ID, "tinymce")))
    corpo.click()  # garante o foco dentro do editor
    corpo.send_keys(Keys.CONTROL, "a")
    corpo.send_keys(Keys.DELETE)
    mensagem = f"Mensagem automatizada - RA: {RA}"
    corpo.send_keys(mensagem)

    try:
        esperar(driver, lambda d: RA in corpo.text, timeout=3)
    except TimeoutException:
        log.warning("Digitação não surtiu efeito; usando JavaScript como fallback")
        driver.execute_script(
            "arguments[0].innerHTML = arguments[1];", corpo, f"<p>{mensagem}</p>"
        )

    texto_editor = corpo.text
    log.info("Texto no editor: %s", texto_editor)
    assert RA in texto_editor, f"RA não encontrado no editor: {texto_editor}"

    # Volta ao documento principal
    driver.switch_to.default_content()
    log.info("Foco devolvido ao documento principal")

    titulo = esperar(driver, EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    log.info("Cabeçalho <h3>: %s", titulo)
    assert "iFrame" in titulo, f"<h3> inesperado: {titulo}"
    log.info("Parte 3 validada com sucesso")


# ---------------------------------------------------------------- Parte 4
def parte_4_janelas(driver):
    log.info("=== PARTE 4: Troca de abas ===")
    driver.get(f"{BASE}/windows")

    handle_original = driver.current_window_handle
    titulo_original = driver.title
    log.info("Handle original: %s | título: %s", handle_original, titulo_original)

    esperar(driver, EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
    esperar(driver, EC.number_of_windows_to_be(2))

    novo_handle = next(h for h in driver.window_handles if h != handle_original)
    driver.switch_to.window(novo_handle)
    log.info("Foco na nova aba: %s", novo_handle)

    texto = esperar(driver, EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert texto == "New Window", f"Texto inesperado na nova aba: {texto}"
    log.info("Texto da nova aba validado: %s", texto)

    driver.close()
    driver.switch_to.window(handle_original)
    log.info("Aba nova fechada e foco devolvido à original")

    assert len(driver.window_handles) == 1, "Deveria restar apenas 1 handle"
    assert driver.title == titulo_original, (
        f"Título esperado '{titulo_original}', veio '{driver.title}'"
    )
    log.info("Parte 4 validada com sucesso")


# ---------------------------------------------------------------- Bônus
def tratar_novas_abas(driver, handle_original):
    """Percorre todas as abas novas, lê o conteúdo, fecha cada uma e
    volta sempre à aba original."""
    conteudos = []
    novos = [h for h in driver.window_handles if h != handle_original]
    log.info("Abas novas para tratar: %d", len(novos))

    try:
        for handle in novos:
            driver.switch_to.window(handle)
            texto = esperar(
                driver, EC.visibility_of_element_located((By.TAG_NAME, "h3"))
            ).text
            log.info("Aba %s -> %s", handle, texto)
            conteudos.append(texto)
            driver.close()
    finally:
        driver.switch_to.window(handle_original)

    assert len(driver.window_handles) == 1, "Deveria restar apenas 1 handle"
    return conteudos


def parte_bonus_varias_janelas(driver):
    log.info("=== BÔNUS: várias janelas ===")
    driver.get(f"{BASE}/windows")

    handle_original = driver.current_window_handle
    titulo_original = driver.title

    # Dois cliques = duas novas janelas
    for _ in range(2):
        esperar(driver, EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
    esperar(driver, EC.number_of_windows_to_be(3))

    conteudos = tratar_novas_abas(driver, handle_original)
    assert len(conteudos) == 2, f"Esperava 2 abas, tratou {len(conteudos)}"
    assert all(c == "New Window" for c in conteudos), conteudos
    assert driver.current_window_handle == handle_original
    assert driver.title == titulo_original
    log.info("Bônus validado: %s", conteudos)


# ---------------------------------------------------------------- Main
def main():
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_janelas(driver)
        parte_bonus_varias_janelas(driver)
        log.info("TODAS AS PARTES CONCLUÍDAS COM SUCESSO")
    except AssertionError as erro:
        log.error("Falha de validação: %s", erro)
        raise
    except Exception as erro:
        log.exception("Erro inesperado: %s", erro)
        raise
    finally:
        driver.quit()
        log.info("Driver encerrado")


if __name__ == "__main__":
    main()
