# Lab 09 - Dropdowns, Alerts, Iframes e Abas com Selenium

import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

RA = "6326092"


def parte_1_selects(driver):
    logging.info("Parte 1 - Selects")
    driver.get("https://the-internet.herokuapp.com/dropdown")
    wait = WebDriverWait(driver, 10)

    elemento = wait.until(EC.presence_of_element_located((By.ID, "dropdown")))
    select = Select(elemento)

    # lista todas as opcoes
    for opcao in select.options:
        print(opcao.text)
        logging.info(f"Opcao encontrada: {opcao.text}")

    # seleciona pelo indice (0 = Please select, 1 = Option 1, 2 = Option 2)
    select.select_by_index(2)
    assert select.first_selected_option.text == "Option 2"
    logging.info("Option 2 selecionada com sucesso")


def parte_2_alerts(driver):
    logging.info("Parte 2 - Alerts")
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    wait = WebDriverWait(driver, 10)

    # JS Alert
    driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
    alerta = wait.until(EC.alert_is_present())
    logging.info(f"Texto do alert: {alerta.text}")
    alerta.accept()
    resultado = driver.find_element(By.ID, "result").text
    assert resultado == "You successfully clicked an alert"
    logging.info("Alert aceito")

    # JS Confirm
    driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
    alerta = wait.until(EC.alert_is_present())
    logging.info(f"Texto do confirm: {alerta.text}")
    alerta.dismiss()
    resultado = driver.find_element(By.ID, "result").text
    assert resultado == "You clicked: Cancel"
    logging.info("Confirm cancelado")

    # JS Prompt
    driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
    alerta = wait.until(EC.alert_is_present())
    logging.info(f"Texto do prompt: {alerta.text}")
    alerta.send_keys(RA)
    alerta.accept()
    resultado = driver.find_element(By.ID, "result").text
    assert RA in resultado
    logging.info(f"Prompt respondido: {resultado}")


def parte_3_iframe(driver):
    logging.info("Parte 3 - Iframe")
    driver.get("https://the-internet.herokuapp.com/iframe")
    wait = WebDriverWait(driver, 10)

    # entra no iframe usando CSS Selector
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe")))
    logging.info("Entrou no iframe")

    editor = wait.until(EC.presence_of_element_located((By.ID, "tinymce")))
    mensagem = f"Mensagem do robo - RA {RA}"
    editor.clear()
    editor.send_keys(mensagem)
    # o editor do site esta bloqueando a digitacao, entao escrevo com javascript
    if editor.text == "":
        driver.execute_script("arguments[0].innerHTML = arguments[1]", editor, mensagem)
    assert RA in editor.text
    logging.info(f"Texto escrito no editor: {editor.text}")

    # volta para a pagina principal
    driver.switch_to.default_content()
    titulo = driver.find_element(By.TAG_NAME, "h3").text
    assert titulo == "An iFrame containing the TinyMCE WYSIWYG Editor"
    logging.info(f"Saiu do iframe, h3 da pagina: {titulo}")


def parte_4_janelas(driver):
    logging.info("Parte 4 - Abas")
    driver.get("https://the-internet.herokuapp.com/windows")
    wait = WebDriverWait(driver, 10)

    aba_original = driver.current_window_handle
    titulo_original = driver.title

    driver.find_element(By.LINK_TEXT, "Click Here").click()
    wait.until(EC.number_of_windows_to_be(2))
    logging.info("Nova aba aberta")

    # troca para a aba que nao e a original
    for aba in driver.window_handles:
        if aba != aba_original:
            driver.switch_to.window(aba)

    texto = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3"))).text
    assert texto == "New Window"
    logging.info(f"Texto da nova aba: {texto}")

    driver.close()
    driver.switch_to.window(aba_original)

    assert len(driver.window_handles) == 1
    assert driver.title == titulo_original
    logging.info("Voltou para a aba original")


driver = webdriver.Chrome()
try:
    parte_1_selects(driver)
    parte_2_alerts(driver)
    parte_3_iframe(driver)
    parte_4_janelas(driver)
    logging.info("Fim do lab!")
except Exception as erro:
    logging.error(f"Deu erro: {erro}")
finally:
    driver.quit()

