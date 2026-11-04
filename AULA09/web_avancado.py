import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

RA = "6326146"
BASE = "https://the-internet.herokuapp.com"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("web_avancado")


def parte_1_selects(driver):
    log.info("Parte 1: dropdown")
    driver.get(BASE + "/dropdown")
    espera = WebDriverWait(driver, 10)

    dropdown = espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dropdown")))
    select = Select(dropdown)

    for opcao in select.options:
        log.info("Opção disponível: %s", opcao.text)

    select.select_by_index(2)  # índice 2 = "Option 2"
    assert select.first_selected_option.text == "Option 2", "Option 2 não ficou selecionada"
    log.info("Selecionada: %s", select.first_selected_option.text)


def parte_2_alerts(driver):
    log.info("Parte 2: alerts JS")
    driver.get(BASE + "/javascript_alerts")
    espera = WebDriverWait(driver, 10)
    resultado = (By.CSS_SELECTOR, "#result")

    # JS Alert
    espera.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']"))).click()
    alerta = espera.until(EC.alert_is_present())
    log.info("Texto do alert: %s", alerta.text)
    alerta.accept()
    espera.until(EC.text_to_be_present_in_element(resultado, "You successfully clicked an alert"))

    # JS Confirm (cancelar)
    espera.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Confirm']"))).click()
    alerta = espera.until(EC.alert_is_present())
    alerta.dismiss()
    espera.until(EC.text_to_be_present_in_element(resultado, "You clicked: Cancel"))
    texto = driver.find_element(*resultado).text
    assert "You clicked: Cancel" in texto, "Confirm não foi cancelado"
    log.info("Confirm: %s", texto)

    # JS Prompt (enviar o RA)
    espera.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Prompt']"))).click()
    alerta = espera.until(EC.alert_is_present())
    alerta.send_keys(RA)
    alerta.accept()
    espera.until(EC.text_to_be_present_in_element(resultado, RA))
    texto = driver.find_element(*resultado).text
    assert RA in texto, "RA não apareceu no resultado"
    log.info("Prompt: %s", texto)


def parte_3_iframes(driver):
    log.info("Parte 3: iframe")
    driver.get(BASE + "/iframe")
    espera = WebDriverWait(driver, 10)

    # entra no iframe localizando por CSS Selector (sem usar o id fixo)
    espera.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "div.tox-edit-area iframe")))
    corpo = espera.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body#tinymce")))

    # clica, seleciona tudo, apaga e escreve
    corpo.click()
    corpo.send_keys(Keys.CONTROL, "a")
    corpo.send_keys(Keys.DELETE)
    corpo.send_keys("Entrega do Lab 09 - RA " + RA)

    # espera o texto aparecer antes de validar
    espera.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body#tinymce"), RA))
    texto = driver.find_element(By.CSS_SELECTOR, "body#tinymce").text
    assert RA in texto, "RA não foi escrito no editor"
    log.info("Texto no editor: %s", texto)

    # volta pro documento principal e confere o <h3>
    driver.switch_to.default_content()
    titulo = espera.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert "iFrame" in titulo, "não saiu do iframe"
    log.info("Cabeçalho da página: %s", titulo)


def parte_4_janelas(driver):
    log.info("Parte 4: troca de abas")
    driver.get(BASE + "/windows")
    espera = WebDriverWait(driver, 10)

    handle_original = driver.current_window_handle
    titulo_original = driver.title

    espera.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
    espera.until(EC.number_of_windows_to_be(2))

    for handle in driver.window_handles:
        if handle != handle_original:
            driver.switch_to.window(handle)

    espera.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h3"), "New Window"))
    texto = driver.find_element(By.TAG_NAME, "h3").text
    assert texto == "New Window", "não está na nova aba"
    log.info("Nova aba: %s", texto)

    driver.close()
    driver.switch_to.window(handle_original)

    assert len(driver.window_handles) == 1, "sobrou aba aberta"
    assert driver.title == titulo_original, "título da página original mudou"
    log.info("Voltou pra aba original: %s", driver.title)


def ler_e_fechar_novas_abas(driver, handle_original):
    """Bônus: percorre todas as abas novas, lê o <h3>, fecha e volta pra original."""
    textos = []
    espera = WebDriverWait(driver, 10)
    try:
        for handle in list(driver.window_handles):
            if handle != handle_original:
                driver.switch_to.window(handle)
                h3 = espera.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
                textos.append(h3.text)
                driver.close()
    finally:
        driver.switch_to.window(handle_original)
    return textos


def parte_5_bonus(driver):
    log.info("Parte 5 (bônus): várias abas")
    driver.get(BASE + "/windows")
    espera = WebDriverWait(driver, 10)
    handle_original = driver.current_window_handle

    for _ in range(2):
        espera.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
    espera.until(EC.number_of_windows_to_be(3))

    textos = ler_e_fechar_novas_abas(driver, handle_original)
    assert len(textos) == 2, "esperava ler 2 abas novas"
    assert len(driver.window_handles) == 1, "sobrou aba aberta"
    log.info("Textos lidos: %s", textos)


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_janelas(driver)
        parte_5_bonus(driver)
        log.info("Todas as partes passaram")
    except Exception:
        log.exception("Falha na execução")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    main()