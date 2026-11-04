
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==========================================
# CONFIGURAÇÕES
# ==========================================

RA = "6326072"
URL_BASE = "https://the-internet.herokuapp.com"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================
# PARTE 1 - SELECTS
# ==========================================

def parte_1_selects(driver):

    logging.info("Iniciando Parte 1 - Selects")

    driver.get(f"{URL_BASE}/dropdown")

    wait = WebDriverWait(driver, 10)

    elemento = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "select"))
    )

    select = Select(elemento)

    # Listar todas as opções
    for opcao in select.options:
        logging.info(f"Opção disponível: {opcao.text}")

    # Selecionar Option 2 pelo índice
    select.select_by_index(2)

    # Validar seleção
    selecionada = select.first_selected_option.text

    assert selecionada == "Option 2"

    logging.info(f"Opção selecionada corretamente: {selecionada}")


# ==========================================
# PARTE 2 - JAVASCRIPT ALERTS
# ==========================================

def parte_2_alerts(driver):

    logging.info("Iniciando Parte 2 - JavaScript Alerts")

    driver.get(f"{URL_BASE}/javascript_alerts")

    wait = WebDriverWait(driver, 10)

    # JS ALERT
    botao_alert = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(text(), 'Click for JS Alert')]"
        ))
    )

    botao_alert.click()

    alerta = wait.until(EC.alert_is_present())

    texto_alert = alerta.text

    logging.info(f"Texto do JS Alert: {texto_alert}")

    assert texto_alert == "I am a JS Alert"

    alerta.accept()

    # JS CONFIRM
    botao_confirm = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(text(), 'Click for JS Confirm')]"
        ))
    )

    botao_confirm.click()

    alerta = wait.until(EC.alert_is_present())

    texto_confirm = alerta.text

    logging.info(f"Texto do JS Confirm: {texto_confirm}")

    alerta.dismiss()

    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    )

    assert "You clicked: Cancel" in resultado.text

    logging.info("JS Confirm cancelado corretamente.")

    # JS PROMPT
    botao_prompt = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(text(), 'Click for JS Prompt')]"
        ))
    )

    botao_prompt.click()

    alerta = wait.until(EC.alert_is_present())

    texto_prompt = alerta.text

    logging.info(f"Texto do JS Prompt: {texto_prompt}")

    alerta.send_keys(RA)
    alerta.accept()

    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "result"))
    )

    assert RA in resultado.text

    logging.info(f"JS Prompt validado com RA: {RA}")


# ==========================================
# PARTE 3 - IFRAMES
# ==========================================

def parte_3_iframes(driver):

    logging.info("Iniciando Parte 3 - Iframes")

    driver.get(f"{URL_BASE}/iframe")

    wait = WebDriverWait(driver, 10)

    # Localizar iframe por CSS Selector
    iframe = wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "iframe.tox-edit-area__iframe"
        ))
    )

    # Entrar no iframe
    driver.switch_to.frame(iframe)

    # Localizar editor
    editor = wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "body#tinymce"
        ))
    )

    # Limpar conteúdo e escrever mensagem
    editor.clear()
    editor.send_keys(f"Laboratório 09 - RA: {RA}")

    logging.info("Mensagem inserida no editor.")

    # Retornar ao DOM principal
    driver.switch_to.default_content()

    # Validar cabeçalho da página principal
    cabecalho = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )

    assert "An iFrame containing the TinyMCE WYSIWYG Editor" in cabecalho.text

    logging.info(f"Retorno ao DOM principal confirmado: {cabecalho.text}")


# ==========================================
# PARTE 4 - TROCA DE ABAS E JANELAS
# ==========================================

def parte_4_janelas(driver):

    logging.info("Iniciando Parte 4 - Múltiplas Janelas")

    driver.get(f"{URL_BASE}/windows")

    wait = WebDriverWait(driver, 10)

    # Guardar handle original
    handle_original = driver.current_window_handle

    titulo_original = driver.title

    logging.info(f"Handle original: {handle_original}")

    # Clicar no link Click Here
    link = wait.until(
        EC.element_to_be_clickable((
            By.LINK_TEXT,
            "Click Here"
        ))
    )

    link.click()

    # Esperar existirem duas janelas
    wait.until(EC.number_of_windows_to_be(2))

    handles = driver.window_handles

    assert len(handles) == 2

    # Identificar a nova aba
    handle_novo = next(
        handle for handle in handles
        if handle != handle_original
    )

    # Trocar o foco
    driver.switch_to.window(handle_novo)

    logging.info(f"Nova aba aberta: {handle_novo}")

    # Validar conteúdo da nova aba
    novo_conteudo = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )

    assert novo_conteudo.text == "New Window"

    logging.info("Nova aba validada corretamente.")

    # Fechar nova aba
    driver.close()

    # Retornar à aba original
    driver.switch_to.window(handle_original)

    # Validar quantidade de janelas
    assert len(driver.window_handles) == 1

    # Validar título original
    assert driver.title == titulo_original

    logging.info("Retorno à aba original confirmado.")
    logging.info("Parte 4 concluída com sucesso.")


# ==========================================
# BÔNUS - MÚLTIPLAS JANELAS
# ==========================================

def fechar_janelas_novas(driver, handles_originais):

    wait = WebDriverWait(driver, 10)

    handle_original = driver.current_window_handle

    for handle in list(handles_originais):

        if handle == handle_original:
            continue

        if handle not in driver.window_handles:
            continue

        driver.switch_to.window(handle)

        try:
            conteudo = wait.until(
                EC.presence_of_element_located((
                    By.TAG_NAME,
                    "body"
                ))
            )

            logging.info(
                f"Conteúdo da janela {handle}: {conteudo.text}"
            )

        finally:
            driver.close()

    # Garantir retorno à aba original
    if handle_original in driver.window_handles:
        driver.switch_to.window(handle_original)

    assert driver.current_window_handle == handle_original

    logging.info("Todas as janelas novas foram fechadas.")


# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================

def main():

    driver = None

    try:

        driver = webdriver.Chrome()

        driver.maximize_window()

        parte_1_selects(driver)

        parte_2_alerts(driver)

        parte_3_iframes(driver)

        parte_4_janelas(driver)

        logging.info("TODAS AS PARTES FORAM EXECUTADAS COM SUCESSO!")

    except Exception:

        logging.exception("Erro durante a execução do laboratório.")

        raise

    finally:

        if driver is not None:

            driver.quit()

            logging.info("Navegador encerrado com driver.quit().")


if __name__ == "__main__":
    main()
