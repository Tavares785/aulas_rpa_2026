"""Lab 09: dropdown, alertas, iframe e troca de abas com Selenium."""
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

RA = "SEU_RA"
URL = "https://the-internet.herokuapp.com"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def parte_1_selects(driver):
    driver.get(f"{URL}/dropdown")
    espera = WebDriverWait(driver, 10)

    dropdown = espera.until(EC.presence_of_element_located((By.TAG_NAME, "select")))
    opcoes = Select(dropdown)

    for opcao in opcoes.options:
        logging.info("Opção disponível: %s", opcao.text)

    # O índice 0 é o placeholder; Option 2 fica no índice 2.
    opcoes.select_by_index(2)
    assert opcoes.first_selected_option.text == "Option 2"
    logging.info("Option 2 selecionada pelo índice.")


def parte_2_alerts(driver):
    driver.get(f"{URL}/javascript_alerts")
    espera = WebDriverWait(driver, 10)

    botao = espera.until(EC.element_to_be_clickable(
        (By.XPATH, ".//button[normalize-space()='Click for JS Alert']")
    ))
    botao.click()
    alerta = espera.until(EC.alert_is_present())
    texto_alerta = alerta.text
    assert texto_alerta
    logging.info("Texto do alerta: %s", texto_alerta)
    alerta.accept()

    botao = espera.until(EC.element_to_be_clickable(
        (By.XPATH, ".//button[normalize-space()='Click for JS Confirm']")
    ))
    botao.click()
    espera.until(EC.alert_is_present()).dismiss()
    resultado = espera.until(EC.visibility_of_element_located((By.ID, "result"))).text
    assert "You clicked: Cancel" in resultado
    logging.info("Confirmação cancelada: %s", resultado)

    botao = espera.until(EC.element_to_be_clickable(
        (By.XPATH, ".//button[normalize-space()='Click for JS Prompt']")
    ))
    botao.click()
    alerta = espera.until(EC.alert_is_present())
    alerta.send_keys(RA)
    alerta.accept()
    resultado = espera.until(EC.visibility_of_element_located((By.ID, "result"))).text
    assert RA in resultado
    logging.info("RA enviado no prompt: %s", resultado)


def parte_3_iframe(driver):
    driver.get(f"{URL}/iframe")
    espera = WebDriverWait(driver, 10)

    iframe = espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
    driver.switch_to.frame(iframe)

    editor = espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce")))
    editor.clear()
    mensagem = f"Atividade de RPA - RA {RA}"
    editor.send_keys(mensagem)
    assert editor.text == mensagem
    logging.info("Mensagem escrita no editor: %s", editor.text)

    driver.switch_to.default_content()
    titulo = espera.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert "TinyMCE" in titulo
    logging.info("Voltamos à página principal: %s", titulo)


def parte_4_abas(driver):
    driver.get(f"{URL}/windows")
    espera = WebDriverWait(driver, 10)
    titulo_original = driver.title
    aba_original = driver.current_window_handle

    link = espera.until(EC.element_to_be_clickable(
        (By.XPATH, ".//a[normalize-space()='Click Here']")
    ))
    link.click()
    espera.until(EC.number_of_windows_to_be(2))

    aba_nova = [aba for aba in driver.window_handles if aba != aba_original][0]
    driver.switch_to.window(aba_nova)
    texto = espera.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert texto == "New Window"
    logging.info("Nova aba aberta: %s", texto)

    driver.close()
    driver.switch_to.window(aba_original)
    assert len(driver.window_handles) == 1
    assert driver.title == titulo_original
    logging.info("Voltamos à aba original: %s", driver.title)


def main():
    driver = None
    try:
        driver = webdriver.Chrome()
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframe(driver)
        parte_4_abas(driver)
        logging.info("Lab 09 concluído.")
    except Exception:
        logging.exception("Ocorreu um erro durante a execução.")
        raise
    finally:
        if driver is not None:
            driver.quit()
            logging.info("Navegador fechado.")


if __name__ == "__main__":
    main()
