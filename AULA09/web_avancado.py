import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def parte_1_selects(driver):

    logging.info("Iniciando Parte 1")

    driver.get("https://the-internet.herokuapp.com/dropdown")

    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dropdown"))
    )

    select = Select(dropdown)

    logging.info("Opções encontradas:")

    for opcao in select.options:
        logging.info(opcao.text)

    select.select_by_index(2)

    selecionada = select.first_selected_option.text

    assert selecionada == "Option 2"

    logging.info("Validação OK")



def parte_2_alerts(driver):

    RA = "6326193"

    logging.info("Iniciando Parte 2")

    driver.get(
        "https://the-internet.herokuapp.com/javascript_alerts"
    )

    # ALERT

    botao_alert = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(text(),'JS Alert')]"
            )
        )
    )

    botao_alert.click()

    alert = WebDriverWait(driver,10).until(
        EC.alert_is_present()
    )

    texto = alert.text

    logging.info(texto)

    alert.accept()

    # CONFIRM

    botao_confirm = driver.find_element(
        By.XPATH,
        "//button[contains(text(),'JS Confirm')]"
    )

    botao_confirm.click()

    alerta_confirm = WebDriverWait(driver,10).until(
        EC.alert_is_present()
    )

    alerta_confirm.dismiss()

    resultado = WebDriverWait(driver,10).until(
        EC.visibility_of_element_located(
            (By.ID,"result")
        )
    )

    assert resultado.text == "You clicked: Cancel"

    logging.info("Confirm validado")

    # PROMPT

    botao_prompt = driver.find_element(
        By.XPATH,
        "//button[contains(text(),'JS Prompt')]"
    )

    botao_prompt.click()

    prompt = WebDriverWait(driver,10).until(
        EC.alert_is_present()
    )

    prompt.send_keys(RA)

    prompt.accept()

    resultado_prompt = WebDriverWait(driver,10).until(
        EC.visibility_of_element_located(
            (By.ID, "result")
        )
    )

    assert RA in resultado_prompt.text

    logging.info("Prompt validado")



def parte_3_iframe(driver):

    RA = "123456"

    logging.info("Iniciando Parte 3")

    driver.get(
        "https://the-internet.herokuapp.com/iframe"
    )

    iframe = WebDriverWait(driver,10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "iframe"
            )
        )
    )

    driver.switch_to.frame(iframe)

    editor = WebDriverWait(driver,10).until(
        EC.presence_of_element_located(
            (By.ID, "tinymce")
        )
    )

    editor.clear()

    mensagem = f"Teste Selenium RA {RA}"

    editor.send_keys(mensagem)

    driver.switch_to.default_content()

    cabecalho = WebDriverWait(driver,10).until(
        EC.visibility_of_element_located(
            (By.TAG_NAME, "h3")
        )
    )

    assert "Editor" in cabecalho.text

    logging.info("Iframe validado")


def parte_4_janelas(driver):

    logging.info("Iniciando Parte 4")

    driver.get(
        "https://the-internet.herokuapp.com/windows"
    )

    handle_original = driver.current_window_handle

    link = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Click Here")
        )
    )

    link.click()

    WebDriverWait(driver,10).until(
        EC.number_of_windows_to_be(2)
    )

    for handle in driver.window_handles:

        if handle != handle_original:
            driver.switch_to.window(handle)
            break

    texto = WebDriverWait(driver,10).until(
        EC.visibility_of_element_located(
            (By.TAG_NAME, "h3")
        )
    )

    assert texto.text == "New Window"

    logging.info("Nova aba validada")

    driver.close()

    driver.switch_to.window(handle_original)

    assert len(driver.window_handles) == 1

    assert "The Internet" in driver.title

    logging.info("Retorno para aba original OK")



def main():

    driver = None

    try:

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            )
        )

        driver.maximize_window()

        parte_1_selects(driver)

        parte_2_alerts(driver)

        parte_3_iframe(driver)

        parte_4_janelas(driver)

        logging.info(
            "Laboratório concluído com sucesso"
        )

    except Exception as e:

        logging.error(f"Erro encontrado: {e}")

    finally:

        if driver:
            driver.quit()
            logging.info("Driver encerrado")

if __name__ == "__main__":
    main()