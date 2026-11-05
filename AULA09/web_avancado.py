"""Exercicios da Aula 09: dropdowns, alerts, iframes e janelas."""

import logging
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


URL_DROPDOWN = "https://the-internet.herokuapp.com/dropdown"
URL_ALERTS = "https://the-internet.herokuapp.com/javascript_alerts"
URL_IFRAME = "https://the-internet.herokuapp.com/iframe"
URL_WINDOWS = "https://the-internet.herokuapp.com/windows"
TIMEOUT = 10


def parte_1_selects(driver: WebDriver) -> None:
    driver.get(URL_DROPDOWN)
    wait = WebDriverWait(driver, TIMEOUT)
    elemento = wait.until(EC.presence_of_element_located((By.ID, "dropdown")))
    select = Select(elemento)

    for opcao in select.options:
        logging.info("Opcao do dropdown: %s", opcao.text)

    select.select_by_index(2)
    opcao_selecionada = select.first_selected_option.text
    assert opcao_selecionada == "Option 2"
    logging.info("Dropdown validado: %s", opcao_selecionada)


def parte_2_alerts(driver: WebDriver, ra: str) -> None:
    driver.get(URL_ALERTS)
    wait = WebDriverWait(driver, TIMEOUT)
    conteudo = wait.until(EC.presence_of_element_located((By.ID, "content")))

    botao_alert = conteudo.find_element(
        By.XPATH, ".//button[normalize-space()='Click for JS Alert']"
    )
    wait.until(EC.element_to_be_clickable(botao_alert)).click()
    alerta = wait.until(EC.alert_is_present())
    texto_alerta = alerta.text
    assert texto_alerta
    logging.info("Texto do JS Alert capturado: %s", texto_alerta)
    alerta.accept()

    botao_confirm = conteudo.find_element(
        By.XPATH, ".//button[normalize-space()='Click for JS Confirm']"
    )
    wait.until(EC.element_to_be_clickable(botao_confirm)).click()
    alerta = wait.until(EC.alert_is_present())
    alerta.dismiss()
    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    ).text
    assert "You clicked: Cancel" in resultado
    logging.info("JS Confirm cancelado e validado: %s", resultado)

    botao_prompt = conteudo.find_element(
        By.XPATH, ".//button[normalize-space()='Click for JS Prompt']"
    )
    wait.until(EC.element_to_be_clickable(botao_prompt)).click()
    alerta = wait.until(EC.alert_is_present())
    alerta.send_keys(ra)
    alerta.accept()
    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    ).text
    assert ra in resultado
    logging.info("JS Prompt validado com o RA informado.")


def parte_3_iframes(driver: WebDriver, ra: str) -> None:
    driver.get(URL_IFRAME)
    wait = WebDriverWait(driver, TIMEOUT)
    seletor_iframe = (By.CSS_SELECTOR, "iframe.tox-edit-area__iframe")
    wait.until(EC.frame_to_be_available_and_switch_to_it(seletor_iframe))

    mensagem = f"Automacao da Aula 09 - RA: {ra}"
    try:
        editor = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )
        editor.clear()
        editor.send_keys(mensagem)
        assert editor.text == mensagem
        logging.info("Conteudo do editor validado.")
    finally:
        driver.switch_to.default_content()

    cabecalho = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )
    assert cabecalho.text.strip() == (
        "An iFrame containing the TinyMCE WYSIWYG Editor"
    )
    logging.info("Retorno ao documento principal confirmado pelo h3.")


def ler_e_fechar_janelas_novas(
    driver: WebDriver, handles: list[str], handle_original: str
) -> list[str]:
    """Leia o conteudo de cada janela nova, feche-a e restaure a janela original."""
    conteudos = []
    try:
        for handle in handles:
            if handle == handle_original:
                continue
            driver.switch_to.window(handle)
            corpo = WebDriverWait(driver, TIMEOUT).until(
                EC.visibility_of_element_located((By.TAG_NAME, "body"))
            )
            conteudos.append(corpo.text)
            logging.info("Conteudo da nova janela: %s", corpo.text)
    finally:
        for handle in handles:
            if handle != handle_original and handle in driver.window_handles:
                driver.switch_to.window(handle)
                driver.close()
        if handle_original in driver.window_handles:
            driver.switch_to.window(handle_original)

    return conteudos


def parte_4_janelas(driver: WebDriver) -> None:
    driver.get(URL_WINDOWS)
    wait = WebDriverWait(driver, TIMEOUT)
    handle_original = driver.current_window_handle
    titulo_original = driver.title

    link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
    link.click()
    wait.until(EC.number_of_windows_to_be(2))
    handles = driver.window_handles
    assert len(handles) == 2
    assert handle_original in handles

    conteudos = ler_e_fechar_janelas_novas(driver, handles, handle_original)
    assert any(conteudo.strip() == "New Window" for conteudo in conteudos)
    logging.info("Conteudo 'New Window' validado.")

    wait.until(EC.number_of_windows_to_be(1))
    assert len(driver.window_handles) == 1
    assert driver.current_window_handle == handle_original
    assert driver.title == titulo_original
    logging.info("Retorno a aba original validado: %s", driver.title)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        stream=sys.stdout,
    )
    ra = input("Digite seu RA: ").strip()
    if not ra:
        raise ValueError("O RA nao pode estar vazio.")

    driver = webdriver.Chrome()
    try:
        parte_1_selects(driver)
        parte_2_alerts(driver, ra)
        parte_3_iframes(driver, ra)
        parte_4_janelas(driver)
        logging.info("Todas as partes da Aula 09 foram concluidas.")
    except Exception:
        logging.exception("Falha durante a execucao da Aula 09.")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
