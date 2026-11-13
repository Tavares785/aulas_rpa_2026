"""
Lab 09: Manipulação de Dropdowns, Pop-ups e Web Elements Complexos.

Automação web com Selenium tratando Selects, Alerts, Iframes e Janelas.
"""

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def parte_1_selects(driver):
    """Interação com elemento <select> via classe Select."""
    url = "https://the-internet.herokuapp.com/dropdown"
    logger.info("Acessando %s", url)
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    elemento_select = wait.until(
        EC.presence_of_element_located((By.ID, "dropdown"))
    )
    select = Select(elemento_select)

    opcoes = [opcao.text for opcao in select.options]
    logger.info("Opções encontradas: %s", opcoes)

    select.select_by_index(2)
    opcao_selecionada = select.first_selected_option.text
    logger.info("Opção selecionada: %s", opcao_selecionada)
    assert opcao_selecionada == "Option 2", "Opção 2 não foi selecionada!"


def parte_2_alerts(driver):
    """Manipulação de JavaScript Alerts (alert, confirm, prompt)."""
    url = "https://the-internet.herokuapp.com/javascript_alerts"
    logger.info("Acessando %s", url)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # 1. JS Alert
    btn_alert = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Click for JS Alert')]")
        )
    )
    btn_alert.click()
    alert = wait.until(EC.alert_is_present())
    logger.info("Texto do JS Alert: %s", alert.text)
    alert.accept()

    # 2. JS Confirm
    btn_confirm = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Click for JS Confirm')]")
        )
    )
    btn_confirm.click()
    confirm = wait.until(EC.alert_is_present())
    logger.info("Cancelando JS Confirm...")
    confirm.dismiss()
    resultado = driver.find_element(By.ID, "result").text
    assert "You clicked: Cancel" in resultado, "Cancel não registrado!"

    # 3. JS Prompt
    btn_prompt = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Click for JS Prompt')]")
        )
    )
    btn_prompt.click()
    prompt = wait.until(EC.alert_is_present())
    ra = "6326138"
    prompt.send_keys(ra)
    prompt.accept()
    resultado_prompt = driver.find_element(By.ID, "result").text
    assert ra in resultado_prompt, "RA não encontrado no resultado do prompt!"


def parte_3_iframe(driver):
    """Navegação e escrita em iframe rico."""
    url = "https://the-internet.herokuapp.com/iframe"
    logger.info("Acessando %s", url)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Localiza o iframe por CSS Selector
    iframe = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.tox-edit-area__iframe, iframe#mce_0_ifr"))
    )
    driver.switch_to.frame(iframe)

    corpo = wait.until(EC.presence_of_element_located((By.ID, "tinymce")))
    corpo.clear()
    corpo.send_keys("Robo RPA ativo - RA 6326138")

    driver.switch_to.default_content()
    h3_texto = driver.find_element(By.TAG_NAME, "h3").text
    assert "An iFrame containing the TinyMCE WYSIWYG Editor" in h3_texto, (
        "Não retornou ao documento principal!"
    )


def parte_4_janelas(driver):
    """Controle de múltiplas abas/janelas."""
    url = "https://the-internet.herokuapp.com/windows"
    logger.info("Acessando %s", url)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    aba_original = driver.current_window_handle
    link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
    )
    link.click()

    wait.until(EC.number_of_windows_to_be(2))
    todas_abas = driver.window_handles
    nova_aba = [h for h in todas_abas if h != aba_original][0]

    driver.switch_to.window(nova_aba)
    assert driver.find_element(By.TAG_NAME, "h3").text == "New Window"

    driver.close()
    driver.switch_to.window(aba_original)

    assert len(driver.window_handles) == 1
    assert "The Internet" in driver.title


def main():
    """Função principal executando os 4 módulos."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    try:
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframe(driver)
        parte_4_janelas(driver)
        logger.info("Todas as partes foram executadas com sucesso!")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
