import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


BASE_URL = "https://the-internet.herokuapp.com"
WAIT_SECONDS = 10
IFRAME_SELECTOR = "iframe[title='Rich Text Area']"
RA = "6326226"


def parte_1_selects(driver):
    driver.get(f"{BASE_URL}/dropdown")
    wait = WebDriverWait(driver, WAIT_SECONDS)
    dropdown = wait.until(
        EC.presence_of_element_located((By.ID, "dropdown"))
    )
    select = Select(dropdown)

    for option in select.options:
        logging.info("Opção disponível: %s", option.text)

    assert len(select.options) > 2
    select.select_by_index(2)
    selecionada = select.first_selected_option.text
    assert selecionada == "Option 2"
    logging.info("Opção selecionada pelo índice 2: %s", selecionada)


def parte_2_alerts(driver, ra):
    driver.get(f"{BASE_URL}/javascript_alerts")
    wait = WebDriverWait(driver, WAIT_SECONDS)

    botao_alert = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, ".//button[normalize-space(.)='Click for JS Alert']")
        )
    )
    botao_alert.click()
    alerta = wait.until(EC.alert_is_present())
    texto_alerta = alerta.text
    logging.info("Texto do JS Alert: %s", texto_alerta)
    alerta.accept()
    assert texto_alerta == "I am a JS Alert"
    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    )
    assert resultado.text == "You successfully clicked an alert"
    logging.info("JS Alert aceito e validado.")

    botao_confirm = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, ".//button[normalize-space(.)='Click for JS Confirm']")
        )
    )
    botao_confirm.click()
    wait.until(EC.alert_is_present()).dismiss()
    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    )
    assert "You clicked: Cancel" in resultado.text
    logging.info("JS Confirm cancelado e validado: %s", resultado.text)

    botao_prompt = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, ".//button[normalize-space(.)='Click for JS Prompt']")
        )
    )
    botao_prompt.click()
    alerta = wait.until(EC.alert_is_present())
    alerta.send_keys(ra)
    alerta.accept()
    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    )
    assert ra in resultado.text
    logging.info("JS Prompt aceito; resultado contém o RA informado.")


def parte_3_iframe(driver, ra):
    driver.get(f"{BASE_URL}/iframe")
    wait = WebDriverWait(driver, WAIT_SECONDS)
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, IFRAME_SELECTOR)
        )
    )
    editor = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "body#tinymce"))
    )
    editor.clear()
    mensagem = f"Automação da AULA09 - RA: {ra}"
    editor.click()
    editor.send_keys(mensagem)
    assert ra in editor.text
    logging.info("Conteúdo do editor atualizado com o RA informado.")

    driver.switch_to.default_content()
    cabecalho = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )
    assert cabecalho.text == (
        "An iFrame containing the TinyMCE WYSIWYG Editor"
    )
    logging.info("Contexto principal confirmado pelo cabeçalho: %s", cabecalho.text)


def parte_4_janelas(driver):
    driver.get(f"{BASE_URL}/windows")
    wait = WebDriverWait(driver, WAIT_SECONDS)
    titulo_original = driver.title
    handle_original = driver.current_window_handle
    link = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, ".//a[normalize-space(.)='Click Here']")
        )
    )
    link.click()
    wait.until(EC.number_of_windows_to_be(2))

    handle_novo = next(
        handle
        for handle in driver.window_handles
        if handle != handle_original
    )
    try:
        driver.switch_to.window(handle_novo)
        cabecalho = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h3"))
        )
        assert cabecalho.text == "New Window"
        logging.info("Nova aba validada: %s", cabecalho.text)
    finally:
        if handle_novo in driver.window_handles:
            driver.switch_to.window(handle_novo)
            driver.close()
        if handle_original in driver.window_handles:
            driver.switch_to.window(handle_original)

    wait.until(EC.number_of_windows_to_be(1))
    assert driver.current_window_handle == handle_original
    assert len(driver.window_handles) == 1
    assert driver.title == titulo_original
    logging.info("Aba original restaurada: %s", driver.title)


def main():
    driver = None
    try:
        driver = webdriver.Chrome()
        parte_1_selects(driver)
        parte_2_alerts(driver, RA)
        parte_3_iframe(driver, RA)
        parte_4_janelas(driver)
        logging.info("Todas as partes da AULA09 foram concluídas.")
    except Exception:
        logging.exception("A automação da AULA09 falhou.")
        raise
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    main()
