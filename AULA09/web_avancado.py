
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


RA = "6326269"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def parte_1_selects(driver):
    logging.info("Iniciando Parte 1 - Selects")

    driver.get("https://the-internet.herokuapp.com/dropdown")
    wait = WebDriverWait(driver, 15)

    elemento = wait.until(
        EC.presence_of_element_located((By.ID, "dropdown"))
    )

    select = Select(elemento)

    for opcao in select.options:
        logging.info("Opção disponível: %s", opcao.text)

    select.select_by_index(2)

    assert select.first_selected_option.text == "Option 2"

    logging.info("Option 2 selecionada e validada!")


def parte_2_alerts(driver):
    logging.info("Iniciando Parte 2 - Alerts")

    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    wait = WebDriverWait(driver, 15)

    # JS Alert
    driver.find_element(
        By.XPATH, "//button[contains(., 'Click for JS Alert')]"
    ).click()

    alerta = wait.until(EC.alert_is_present())
    texto = alerta.text

    logging.info("Texto do JS Alert: %s", texto)
    alerta.accept()

    # JS Confirm
    driver.find_element(
        By.XPATH, "//button[contains(., 'Click for JS Confirm')]"
    ).click()

    alerta = wait.until(EC.alert_is_present())
    alerta.dismiss()

    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    )

    assert "You clicked: Cancel" in resultado.text

    logging.info("JS Confirm cancelado e validado!")

    # JS Prompt
    driver.find_element(
        By.XPATH, "//button[contains(., 'Click for JS Prompt')]"
    ).click()

    alerta = wait.until(EC.alert_is_present())
    alerta.send_keys(RA)
    alerta.accept()

    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    )

    assert RA in resultado.text

    logging.info("JS Prompt enviado e validado com o RA!")


def parte_3_iframes(driver):
    logging.info("Iniciando Parte 3 - Iframes")

    driver.get("https://the-internet.herokuapp.com/iframe")
    wait = WebDriverWait(driver, 15)

    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe")
        )
    )

    editor = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "body#tinymce")
        )
    )

    editor.clear()
    editor.send_keys(f"Automação RPA - RA: {RA}")

    logging.info("Mensagem escrita no editor!")

    driver.switch_to.default_content()

    cabecalho = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )

    assert "iFrame" in cabecalho.text

    logging.info("Retorno ao documento principal validado!")


def parte_4_janelas(driver):
    logging.info("Iniciando Parte 4 - Janelas")

    driver.get("https://the-internet.herokuapp.com/windows")
    wait = WebDriverWait(driver, 15)

    handle_original = driver.current_window_handle
    titulo_original = driver.title

    link = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[normalize-space()='Click Here']")
        )
    )

    link.click()

    wait.until(EC.number_of_windows_to_be(2))

    handles = driver.window_handles

    handle_novo = next(
        handle for handle in handles
        if handle != handle_original
    )

    driver.switch_to.window(handle_novo)

    cabecalho = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )

    assert cabecalho.text == "New Window"

    logging.info("Nova aba aberta e validada!")

    driver.close()

    driver.switch_to.window(handle_original)

    assert len(driver.window_handles) == 1
    assert driver.title == titulo_original

    logging.info("Retorno à aba original validado!")


def main():
    driver = webdriver.Chrome()

    try:
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_janelas(driver)

        logging.info("Todas as partes foram concluídas com sucesso!")

    except Exception:
        logging.exception("Ocorreu um erro durante a automação.")
        raise

    finally:
        driver.quit()
        logging.info("Navegador encerrado!")


if __name__ == "__main__":
    main()

