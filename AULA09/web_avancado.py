import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"    
)

def parte_1_selects(driver):
    logging.info("Iniciando Parte 1 - Selects")

    driver.get("https://the-internet.herokuapp.com/dropdown")

    elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "select"))
    )

    select = Select(elemento)

    logging.info("Opções disponíveis no dropdown:")

    for indice, opcao in enumerate(select.options):
        logging.info("Índice %d: %s", indice, opcao.text)

    select.select_by_index(2)

    assert select.first_selected_option.text == "Option 2"

    logging.info("Opção 2 selecionada e validada com sucesso")

def parte_2_alerts(driver):
    logging.info("Iniciando Parte 2 - Alerts")

    driver.get("https://the-internet.herokuapp.com/javascript_alerts")

    body = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    logging.info("Executando alertas JS")

    botao_alert = body.find_element(
        By.XPATH, ".//button[normalize-space()='Click for JS Alert']"
    )

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(botao_alert)
    ).click()

    alert = WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )

    texto_alert = alert.text

    logging.info("Texto do alerta: %s", texto_alert)

    assert texto_alert == "I am a JS Alert"

    alert.accept()

    logging.info("Alerta confirmado")

    logging.info("Executando alerta de confirmação")

    botao_confirm = body.find_element(
        By.XPATH, ".//button[normalize-space()='Click for JS Confirm']"
    )

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(botao_confirm)
    ).click()

    alert = WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )

    logging.info("Texto do alerta de confirmação: %s", alert.text)

    alert.dismiss()

    resultado = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "result"))
    )

    assert "You clicked: Cancel" in resultado.text

    logging.info('JS confirm cancelado e validado com sucesso')

    logging.info('Executando JS Prompt')

    botao_prompt = body.find_element(
        By.XPATH, ".//button[normalize-space()='Click for JS Prompt']"
    )

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(botao_prompt)
    ).click()

    alert = WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )

    ra = "6326018"

    logging.info("Digitando RA no Js Prompt: %s", ra)

    alert.send_keys(ra)
    alert.accept()

    resultado = WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.ID, "result"), ra
            )
        )

    assert resultado is True
    assert ra in driver.find_element(By.ID, "result").text

    logging.info("JS Prompt confirmado e RA validado com sucesso")

def parte_3_iframes(driver):
    logging.info("Iniciando Parte 3 - Iframes")

    driver.get("https://the-internet.herokuapp.com/iframe")

    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[title='Rich Text Area']")
        )
    )

    logging.info("Entrou no iframe do editor")

    editor = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "body"))
    )

    editor.click()
    editor.send_keys(Keys.CONTROL, "a")
    editor.send_keys(Keys.BACKSPACE)

    logging.info("Conteúdo anterior do editor removido")

    ra = "6326018"
    mensagem = f"Automação Selenium - RA: {ra}"

    editor.send_keys(mensagem)

    logging.info("Mensagem enviada ao editor: %s", mensagem)

    conteudo = driver.execute_script(
        "return arguments[0].innerHTML;", editor
    )

    logging.info("HTML retornado pelo editor: %r", conteudo)

    assert ra in conteudo, "O RA não foi encontrado no conteúdo do editor"

    logging.info("Conteúdo do editor validado com sucesso")

    driver.switch_to.default_content()

    logging.info("Retornou ao documento principal")

    cabecalho = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )

    logging.info("Texto do cabeçalho: %s", cabecalho.text)

    assert "An iFrame containing" in cabecalho.text
    logging.info("Retorno ao documento principal validado com sucesso")

def parte_4_janelas(driver):
    logging.info("Iniciando Parte 4 - Múltiplas Janelas")

    driver.get("https://the-internet.herokuapp.com/windows")

    janela_original = driver.current_window_handle

    logging.info("Janela original identificada: %s", janela_original)

    botao = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Click Here")
        )
    )

    botao.click()

    logging.info("Botão Click Here clicado")

    WebDriverWait(driver, 10).until(
        EC.number_of_windows_to_be(2)
    )

    logging.info("Duas janelas abertas")

    for janela in driver.window_handles:
        if janela != janela_original:
            janela_nova = janela
            break

    driver.switch_to.window(janela_nova)

    logging.info("Alternou para a nova janela")

    novo_texto = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.TAG_NAME, "h3")
        )
    )

    logging.info("Texto encontrado na nova janela: %s", novo_texto.text)

    assert novo_texto.text == "New Window"

    logging.info("Nova janela validada com sucesso")

    driver.close()

    logging.info("Nova janela fechada")

    driver.switch_to.window(janela_original)

    assert len(driver.window_handles) == 1

    assert driver.current_window_handle == janela_original

    assert driver.title == "The Internet"

    logging.info("Retorno à janela original validado com sucesso")

def main():
    driver = None
    try:
        driver = webdriver.Chrome()

        parte_1_selects(driver)

        parte_2_alerts(driver)

        parte_3_iframes(driver)

        parte_4_janelas(driver)

    except Exception:
        logging.exception("Ocorreu um erro durante a execução")
        raise

    finally:
        if driver is not None:
            driver.quit()
            logging.info("Navegador encerrado.")

if __name__  == "__main__":
    main()