import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

RA = "123456"

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
except ImportError:
    webdriver = None
    logger.error("Selenium não instalado. Execute: pip install selenium")


def parte_1_selects(driver):
    URL = "https://the-internet.herokuapp.com/dropdown"
    logger.info("[Parte 1] Acessando: %s", URL)
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    elemento_select = wait.until(
        EC.presence_of_element_located((By.ID, "dropdown"))
    )
    logger.info("[Parte 1] Elemento <select> localizado.")

    select = Select(elemento_select)

    logger.info("[Parte 1] Opções disponíveis no dropdown:")
    for opcao in select.options:
        logger.info("  -> '%s' (value='%s')", opcao.text, opcao.get_attribute("value"))

    select.select_by_index(2)
    logger.info("[Parte 1] 'Option 2' selecionada pelo índice 2.")

    opcao_selecionada = select.first_selected_option.text
    assert opcao_selecionada == "Option 2", (
        f"Esperado 'Option 2', mas encontrado '{opcao_selecionada}'"
    )
    logger.info("[Parte 1] ✓ Assert OK — opção selecionada: '%s'", opcao_selecionada)


def parte_2_alerts(driver):
    URL = "https://the-internet.herokuapp.com/javascript_alerts"
    logger.info("[Parte 2] Acessando: %s", URL)
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    logger.info("[Parte 2] JS Alert: localizando botão via XPath relativo...")
    btn_alert = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space(text())='Click for JS Alert']")
        )
    )
    btn_alert.click()

    wait.until(EC.alert_is_present())
    alerta = driver.switch_to.alert
    texto_alert = alerta.text
    logger.info("[Parte 2] JS Alert: texto capturado = '%s'", texto_alert)
    alerta.accept()
    logger.info("[Parte 2] JS Alert: confirmado com accept().")

    logger.info("[Parte 2] JS Confirm: localizando botão via XPath relativo...")
    btn_confirm = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space(text())='Click for JS Confirm']")
        )
    )
    btn_confirm.click()

    wait.until(EC.alert_is_present())
    confirmacao = driver.switch_to.alert
    logger.info("[Parte 2] JS Confirm: texto = '%s' — cancelando com dismiss()...", confirmacao.text)
    confirmacao.dismiss()
    logger.info("[Parte 2] JS Confirm: cancelado com dismiss().")

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "result"), "Cancel")
    )
    texto_resultado = driver.find_element(By.ID, "result").text
    assert "Cancel" in texto_resultado, (
        f"Esperado 'Cancel' no resultado, mas encontrado: '{texto_resultado}'"
    )
    logger.info("[Parte 2] ✓ Assert OK — resultado do Confirm: '%s'", texto_resultado)

    logger.info("[Parte 2] JS Prompt: localizando botão via XPath relativo...")
    btn_prompt = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space(text())='Click for JS Prompt']")
        )
    )
    btn_prompt.click()

    wait.until(EC.alert_is_present())
    prompt = driver.switch_to.alert
    logger.info("[Parte 2] JS Prompt: texto = '%s' — enviando RA '%s'...", prompt.text, RA)
    prompt.send_keys(RA)
    prompt.accept()
    logger.info("[Parte 2] JS Prompt: RA enviado e confirmado com accept().")

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "result"), RA)
    )
    texto_prompt_resultado = driver.find_element(By.ID, "result").text
    assert RA in texto_prompt_resultado, (
        f"Esperado RA '{RA}' no resultado, mas encontrado: '{texto_prompt_resultado}'"
    )
    logger.info("[Parte 2] ✓ Assert OK — resultado do Prompt: '%s'", texto_prompt_resultado)


def parte_3_iframes(driver):
    URL = "https://the-internet.herokuapp.com/iframe"
    logger.info("[Parte 3] Acessando: %s", URL)
    driver.get(URL)

    wait = WebDriverWait(driver, 15)

    logger.info("[Parte 3] Localizando iframe do editor por CSS Selector...")
    iframe_editor = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "iframe[id$='_ifr']")
        )
    )
    logger.info("[Parte 3] Iframe localizado. Trocando contexto para o iframe...")
    driver.switch_to.frame(iframe_editor)

    corpo = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce"))
    )
    logger.info("[Parte 3] Corpo do editor localizado. Limpando conteúdo...")

    corpo.click()
    corpo.send_keys(Keys.CONTROL, "a")
    corpo.send_keys(Keys.DELETE)

    mensagem = f"Automação RPA - RA: {RA}"
    corpo.send_keys(mensagem)
    logger.info("[Parte 3] Mensagem digitada no editor: '%s'", mensagem)

    driver.switch_to.default_content()
    logger.info("[Parte 3] Retornado ao documento principal com default_content().")

    h3 = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "h3"))
    )
    texto_h3 = h3.text
    logger.info("[Parte 3] Texto do <h3> encontrado: '%s'", texto_h3)

    assert len(texto_h3) > 0, "O <h3> da página está vazio — possível falha ao sair do iframe."
    logger.info("[Parte 3] ✓ Assert OK — <h3> visível no DOM raiz: '%s'", texto_h3)


def parte_4_abas(driver):
    URL = "https://the-internet.herokuapp.com/windows"
    logger.info("[Parte 4] Acessando: %s", URL)
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    handle_original = driver.current_window_handle
    logger.info("[Parte 4] Handle da aba original: %s", handle_original)

    link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
    )
    logger.info("[Parte 4] Clicando em 'Click Here' para abrir nova aba...")
    link.click()

    wait.until(EC.number_of_windows_to_be(2))
    logger.info("[Parte 4] 2 handles detectados.")

    handle_nova = next(
        h for h in driver.window_handles if h != handle_original
    )
    logger.info("[Parte 4] Handle da nova aba: %s", handle_nova)

    driver.switch_to.window(handle_nova)
    logger.info("[Parte 4] Foco trocado para a nova aba.")

    h3_nova = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "h3"))
    )
    texto_nova = h3_nova.text
    logger.info("[Parte 4] Texto exibido na nova aba: '%s'", texto_nova)

    assert texto_nova == "New Window", (
        f"Esperado 'New Window' na nova aba, mas encontrado: '{texto_nova}'"
    )
    logger.info("[Parte 4] ✓ Assert OK — nova aba exibe: '%s'", texto_nova)

    driver.close()
    logger.info("[Parte 4] Nova aba fechada.")
    driver.switch_to.window(handle_original)
    logger.info("[Parte 4] Foco retornado para a aba original.")

    assert len(driver.window_handles) == 1, (
        f"Esperado 1 handle ao final, mas há {len(driver.window_handles)}"
    )
    logger.info("[Parte 4] ✓ Assert OK — apenas 1 handle restante.")

    titulo_final = driver.title
    assert titulo_final != "", "Título da aba original está vazio."
    logger.info("[Parte 4] ✓ Assert OK — título da aba original: '%s'", titulo_final)


def bonus_multiplas_abas(driver, handles, handle_original):
    wait = WebDriverWait(driver, 10)
    abas_novas = [h for h in handles if h != handle_original]
    logger.info("[Bônus] Total de abas novas a processar: %d", len(abas_novas))

    for i, handle in enumerate(abas_novas, start=1):
        driver.switch_to.window(handle)
        logger.info("[Bônus] Aba %d/%d — handle: %s", i, len(abas_novas), handle)
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            titulo = driver.title
            try:
                conteudo = driver.find_element(By.TAG_NAME, "h3").text
            except Exception:
                conteudo = driver.find_element(By.TAG_NAME, "body").text[:100]
            logger.info("[Bônus]   Título: '%s' | Conteúdo: '%s'", titulo, conteudo)
        except Exception as err:
            logger.warning("[Bônus]   Não foi possível ler a aba %d: %s", i, err)
        finally:
            driver.close()
            logger.info("[Bônus]   Aba %d fechada.", i)

    driver.switch_to.window(handle_original)
    assert len(driver.window_handles) == 1, (
        f"[Bônus] Esperado 1 handle ao final, mas há {len(driver.window_handles)}"
    )
    logger.info("[Bônus] ✓ Assert OK — foco restaurado para a aba original.")


def main():
    if webdriver is None:
        logger.error("Selenium não disponível. Encerrando.")
        raise SystemExit(0)

    opcoes = Options()

    driver = None
    try:
        driver = webdriver.Chrome(options=opcoes)
        driver.maximize_window()
        logger.info("Navegador iniciado com sucesso.")

        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_abas(driver)

        logger.info("=== Todas as partes concluídas com sucesso! ===")

    except AssertionError as err:
        logger.error("Falha de validação: %s", err)
        sys.exit(1)
    except Exception as err:
        logger.error("Erro inesperado: %s", err)
        if "executable" in str(err).lower() or "session" in str(err).lower():
            logger.warning("Navegador/driver indisponível. Encerrando graciosamente.")
            raise SystemExit(0)
        raise
    finally:
        if driver is not None:
            driver.quit()
            logger.info("Driver encerrado (finally).")


if __name__ == "__main__":
    main()
