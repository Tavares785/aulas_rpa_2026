import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==========================================
# CONFIGURAÇÕES
# ==========================================

RA = "6326158"  

URL = "https://the-internet.herokuapp.com"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================
# PARTE 1 - SELECTS
# ==========================================

def parte_1_selects(driver):

    logging.info("Iniciando Parte 1 - Selects")

    driver.get(f"{URL}/dropdown")

    wait = WebDriverWait(driver, 10)

    elemento = wait.until(
        EC.presence_of_element_located((By.ID, "dropdown"))
    )

    select = Select(elemento)

    # Listar todas as opções
    logging.info("Opções disponíveis:")

    for opcao in select.options:
        logging.info("Opção encontrada: %s", opcao.text)

    # Selecionar pelo índice
    select.select_by_index(2)

    # Validar seleção
    assert select.first_selected_option.text == "Option 2"

    logging.info("Parte 1 concluída com sucesso!")


# ==========================================
# PARTE 2 - ALERTAS JAVASCRIPT
# ==========================================

def parte_2_alerts(driver):

    logging.info("Iniciando Parte 2 - Alertas JS")

    driver.get(f"{URL}/javascript_alerts")

    wait = WebDriverWait(driver, 10)

    # 1 - JavaScript Alert
    botao_alert = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Click for JS Alert')]")
        )
    )

    botao_alert.click()

    alerta = wait.until(EC.alert_is_present())

    logging.info("Texto do alerta: %s", alerta.text)

    assert alerta.text == "I am a JS Alert"

    alerta.accept()

    logging.info("Alerta aceito com sucesso!")

    # 2 - JavaScript Confirm - Cancelar
    botao_confirm = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Click for JS Confirm')]")
        )
    )

    botao_confirm.click()

    alerta = wait.until(EC.alert_is_present())

    alerta.dismiss()

    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    )

    assert "Cancel" in resultado.text

    logging.info("Confirmação cancelada corretamente!")

    # 3 - JavaScript Prompt
    botao_prompt = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Click for JS Prompt')]")
        )
    )

    botao_prompt.click()

    alerta = wait.until(EC.alert_is_present())

    alerta.send_keys(RA)

    alerta.accept()

    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    )

    assert RA in resultado.text

    logging.info("RA enviado corretamente no Prompt!")


# ==========================================
# PARTE 3 - IFRAMES
# ==========================================

def parte_3_iframes(driver):

    logging.info("Iniciando Parte 3 - Iframes")

    driver.get(f"{URL}/iframe")

    wait = WebDriverWait(driver, 10)

    # Localizar iframe por CSS Selector
    iframe = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "iframe.tox-edit-area__iframe")
        )
    )

    # Entrar no iframe
    driver.switch_to.frame(iframe)

    editor = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Limpar e escrever mensagem
    editor.clear()

    editor.send_keys(f"Meu RA é: {RA}")

    logging.info("Mensagem escrita no editor!")

    # Voltar ao documento principal
    driver.switch_to.default_content()

    cabecalho = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )

    assert "Editor" in cabecalho.text

    logging.info("Retornou ao documento principal!")


# ==========================================
# BÔNUS - PROCESSAR VÁRIAS JANELAS
# ==========================================

def processar_novas_janelas(driver, handle_original, handles):

    logging.info("Iniciando processamento das novas janelas")

    try:

        for handle in handles:

            if handle != handle_original:

                driver.switch_to.window(handle)

                wait = WebDriverWait(driver, 10)

                wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                conteudo = driver.find_element(
                    By.TAG_NAME, "body"
                ).text

                logging.info(
                    "Conteúdo da nova janela: %s",
                    conteudo
                )

                driver.close()

    finally:

        # Retornar à aba original
        driver.switch_to.window(handle_original)

    logging.info("Todas as janelas novas foram processadas!")


# ==========================================
# PARTE 4 - TROCA DE ABAS E JANELAS
# ==========================================

def parte_4_janelas(driver):

    logging.info("Iniciando Parte 4 - Janelas")

    driver.get(f"{URL}/windows")

    wait = WebDriverWait(driver, 10)

    # Guardar identificador da aba original
    handle_original = driver.current_window_handle

    # Localizar e clicar no link
    link = wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Click Here")
        )
    )

    link.click()

    # Esperar até existirem duas janelas
    wait.until(EC.number_of_windows_to_be(2))

    handles = driver.window_handles

    assert len(handles) == 2

    # Encontrar a nova janela
    nova_janela = next(
        handle for handle in handles
        if handle != handle_original
    )

    # Trocar o foco
    driver.switch_to.window(nova_janela)

    # Validar texto da nova janela
    cabecalho = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )

    assert cabecalho.text == "New Window"

    logging.info("Nova janela aberta e validada!")

    # Fechar nova aba
    driver.close()

    # Retornar para a aba original
    driver.switch_to.window(handle_original)

    # Esperar o retorno ao documento original
    wait.until(
        EC.presence_of_element_located((By.LINK_TEXT, "Click Here"))
    )

    # Validar quantidade de janelas
    assert len(driver.window_handles) == 1

    # Validar título correto da página
    assert driver.title == "The Internet"

    logging.info("Título da página original: %s", driver.title)

    logging.info("Parte 4 concluída com sucesso!")


# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================

def main():

    driver = None

    try:

        logging.info("INICIANDO LABORATÓRIO 09")

        driver = webdriver.Chrome()

        driver.maximize_window()

        parte_1_selects(driver)

        parte_2_alerts(driver)

        parte_3_iframes(driver)

        parte_4_janelas(driver)

        logging.info("TODAS AS PARTES CONCLUÍDAS COM SUCESSO!")

    except Exception:

        logging.exception("Erro durante a execução do laboratório!")

        raise

    finally:

        if driver:

            driver.quit()

            logging.info("Navegador fechado!")


# ==========================================
# INÍCIO DO PROGRAMA
# ==========================================

if __name__ == "__main__":

    main()
