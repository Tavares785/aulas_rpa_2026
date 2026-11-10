"""
Lab 09 - Dropdowns, Pop-ups, Iframes e Abas com Selenium
RA: 6326012

Partes:
1 - Select (dropdown)
2 - Alerts JS (alert, confirm e prompt)
3 - Iframe (editor TinyMCE)
4 - Troca de abas/janelas
Bonus - funcao generica para varias abas novas
"""
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

RA = "6326012"
URL_BASE = "https://the-internet.herokuapp.com"
TEMPO_ESPERA = 10

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("web_avancado.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def parte_1_selects(driver):
    driver.get(URL_BASE + "/dropdown")
    espera = WebDriverWait(driver, TEMPO_ESPERA)
    elemento = espera.until(EC.presence_of_element_located((By.ID, "dropdown")))
    select = Select(elemento)

    logging.info("Parte 1 - opcoes do dropdown:")
    for i, opcao in enumerate(select.options):
        logging.info("  [%d] %s", i, opcao.text)

    # indice 0 e o "Please select an option", entao a Option 2 fica no 2
    select.select_by_index(2)
    selecionada = select.first_selected_option.text
    assert selecionada == "Option 2", f"Esperado Option 2, veio {selecionada}"
    logging.info("Parte 1 - opcao selecionada: %s", selecionada)


def ler_resultado(driver):
    espera = WebDriverWait(driver, TEMPO_ESPERA)
    return espera.until(EC.visibility_of_element_located((By.ID, "result"))).text


def disparar_alert(driver, texto_botao):
    # botoes localizados so por XPath relativo, pelo texto
    espera = WebDriverWait(driver, TEMPO_ESPERA)
    botao = espera.until(EC.element_to_be_clickable((By.XPATH, f"//button[text()='{texto_botao}']")))
    botao.click()
    return espera.until(EC.alert_is_present())


def parte_2_alerts(driver):
    driver.get(URL_BASE + "/javascript_alerts")

    # JS Alert
    alerta = disparar_alert(driver, "Click for JS Alert")
    logging.info("Parte 2 - texto do alert: %s", alerta.text)
    alerta.accept()
    assert "You successfully clicked an alert" in ler_resultado(driver)

    # JS Confirm -> cancelar
    alerta = disparar_alert(driver, "Click for JS Confirm")
    logging.info("Parte 2 - texto do confirm: %s", alerta.text)
    alerta.dismiss()
    resultado = ler_resultado(driver)
    assert resultado == "You clicked: Cancel", f"Resultado inesperado: {resultado}"
    logging.info("Parte 2 - confirm cancelado: %s", resultado)

    # JS Prompt -> envia o RA
    alerta = disparar_alert(driver, "Click for JS Prompt")
    logging.info("Parte 2 - texto do prompt: %s", alerta.text)
    alerta.send_keys(RA)
    alerta.accept()
    resultado = ler_resultado(driver)
    assert RA in resultado, f"RA nao apareceu no resultado: {resultado}"
    logging.info("Parte 2 - prompt respondido: %s", resultado)


def parte_3_iframe(driver):
    driver.get(URL_BASE + "/iframe")
    espera = WebDriverWait(driver, TEMPO_ESPERA)

    # CSS selector pela estrutura do editor, sem usar o id mce_0_ifr
    espera.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "div.tox-edit-area iframe")))
    corpo = espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce")))

    mensagem = f"Mensagem do robo - RA {RA}"
    # limpa selecionando tudo e apagando, depois digita a mensagem
    corpo.send_keys(Keys.CONTROL, "a")
    corpo.send_keys(Keys.DELETE)
    corpo.send_keys(mensagem)

    # o editor do site as vezes fica somente leitura (TinyMCE sem chave),
    # nesse caso o conteudo e trocado via JS
    if RA not in corpo.text:
        logging.warning("Parte 3 - editor nao aceitou digitacao, escrevendo via JS")
        driver.execute_script("arguments[0].innerHTML = '<p>' + arguments[1] + '</p>';", corpo, mensagem)

    assert RA in corpo.text, "Mensagem com o RA nao foi escrita no iframe"
    logging.info("Parte 3 - texto no iframe: %s", corpo.text)

    driver.switch_to.default_content()
    titulo = espera.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert titulo == "An iFrame containing the TinyMCE WYSIWYG Editor", f"h3 inesperado: {titulo}"
    logging.info("Parte 3 - de volta ao documento principal, h3: %s", titulo)


def parte_4_abas(driver):
    driver.get(URL_BASE + "/windows")
    espera = WebDriverWait(driver, TEMPO_ESPERA)
    handle_original = driver.current_window_handle
    titulo_original = driver.title

    espera.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
    espera.until(EC.number_of_windows_to_be(2))

    nova_aba = [h for h in driver.window_handles if h != handle_original][0]
    driver.switch_to.window(nova_aba)
    texto = espera.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert texto == "New Window", f"Texto inesperado na nova aba: {texto}"
    logging.info("Parte 4 - nova aba aberta com o texto: %s", texto)

    driver.close()
    driver.switch_to.window(handle_original)

    assert len(driver.window_handles) == 1, "Ainda existe mais de uma aba aberta"
    assert driver.title == titulo_original, f"Titulo inesperado: {driver.title}"
    logging.info("Parte 4 - de volta a aba original: %s", driver.title)


def percorrer_abas_novas(driver, handle_original, handles):
    # le o conteudo de cada aba nova, fecha e volta para a original
    conteudos = []
    for handle in handles:
        if handle == handle_original:
            continue
        driver.switch_to.window(handle)
        texto = WebDriverWait(driver, TEMPO_ESPERA).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        ).text
        logging.info("Bonus - aba %s: %s", handle, texto)
        conteudos.append(texto)
        driver.close()
    driver.switch_to.window(handle_original)
    return conteudos


def bonus_varias_abas(driver, quantidade=3):
    driver.get(URL_BASE + "/windows")
    espera = WebDriverWait(driver, TEMPO_ESPERA)
    handle_original = driver.current_window_handle

    link = espera.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
    for i in range(quantidade):
        link.click()
        espera.until(EC.number_of_windows_to_be(i + 2))

    conteudos = percorrer_abas_novas(driver, handle_original, driver.window_handles)
    assert len(conteudos) == quantidade, f"Esperado {quantidade} abas, lidas {len(conteudos)}"
    assert all("New Window" in c for c in conteudos)
    assert len(driver.window_handles) == 1
    assert driver.current_window_handle == handle_original
    logging.info("Bonus - %d abas lidas e fechadas", len(conteudos))


def main():
    driver = None
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframe(driver)
        parte_4_abas(driver)
        bonus_varias_abas(driver)
        logging.info("Todas as partes concluidas com sucesso")
    except AssertionError as erro:
        logging.error("Validacao falhou: %s", erro)
    except Exception as erro:
        logging.exception("Erro na execucao do robo: %s", erro)
    finally:
        if driver is not None:
            driver.quit()
        logging.info("Navegador fechado")


if __name__ == "__main__":
    main()
