import logging
import sys
 
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
 
# settings

BASE_URL = "https://the-internet.herokuapp.com"
RA = "6326082"
TIMEOUT = 10
 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(funcName)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("web_avancado")
 
 
def criar_driver() -> webdriver.Chrome:
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--start-maximized")
    return webdriver.Chrome(options=opcoes)
 
 

def parte_1_selects(driver: webdriver.Chrome) -> None:
    log.info("=== PARTE 1: Selects ===")
    wait = WebDriverWait(driver, TIMEOUT)
    driver.get(f"{BASE_URL}/dropdown")
 
    elemento = wait.until(EC.presence_of_element_located((By.ID, "dropdown")))
    select = Select(elemento)
 
    # Lists ALL available options
    log.info("Opções disponíveis no dropdown:")
    for indice, opcao in enumerate(select.options):
        log.info("  [%d] %s", indice, opcao.text)
    assert len(select.options) >= 3, "O dropdown deveria ter ao menos 3 opções"
 
    # selects option 2 in the index (0 = placeholder, 1 = Option 1, 2 = Option 2)
    select.select_by_index(2)
    selecionada = select.first_selected_option.text
    log.info("Opção selecionada: %s", selecionada)
    assert selecionada == "Option 2", f"Esperado 'Option 2', obtido {selecionada!r}"
    log.info("Parte 1 validada com sucesso.")
 
 
#  JS Alerts
def _esperar_alerta(driver: webdriver.Chrome):
    return WebDriverWait(driver, TIMEOUT).until(EC.alert_is_present())
 
 
def _esperar_resultado(driver: webdriver.Chrome, trecho: str) -> str:
    """Espera o #result conter o trecho e devolve o texto completo."""
    WebDriverWait(driver, TIMEOUT).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#result"), trecho)
    )
    return driver.find_element(By.CSS_SELECTOR, "#result").text
 
 
def parte_2_alerts(driver: webdriver.Chrome) -> None:
    log.info("=== PARTE 2: Alerts JS ===")
    wait = WebDriverWait(driver, TIMEOUT)
    driver.get(f"{BASE_URL}/javascript_alerts")
 
    # buttons located ONLY via relative XPath (no IDs)
    xpath_alert = "//button[normalize-space()='Click for JS Alert']"
    xpath_confirm = "//button[normalize-space()='Click for JS Confirm']"
    xpath_prompt = "//button[normalize-space()='Click for JS Prompt']"
 
    # ---- JS Alert ----
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_alert))).click()
    alerta = _esperar_alerta(driver)
    texto = alerta.text
    log.info("Texto do JS Alert: %s", texto)
    assert texto == "I am a JS Alert", f"Texto inesperado no alert: {texto!r}"
    alerta.accept()
    resultado = _esperar_resultado(driver, "successfully clicked an alert")
    assert "You successfully clicked an alert" in resultado, resultado
    log.info("JS Alert aceito. #result = %s", resultado)
 
    # ---- JS Confirm (cancel) ----
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_confirm))).click()
    alerta = _esperar_alerta(driver)
    log.info("Texto do JS Confirm: %s", alerta.text)
    alerta.dismiss()
    resultado = _esperar_resultado(driver, "You clicked: Cancel")
    assert "You clicked: Cancel" in resultado, f"#result inesperado: {resultado!r}"
    log.info("JS Confirm cancelado. #result = %s", resultado)
 
    # ---- JS Prompt (sends RA) ----
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath_prompt))).click()
    alerta = _esperar_alerta(driver)
    log.info("Texto do JS Prompt: %s", alerta.text)
    alerta.send_keys(RA)
    alerta.accept()
    resultado = _esperar_resultado(driver, RA)
    assert RA in resultado, f"RA {RA!r} não encontrado em #result: {resultado!r}"
    log.info("JS Prompt aceito. #result = %s", resultado)
    log.info("Parte 2 validada com sucesso.")
 
 
# Iframes

def parte_3_iframes(driver: webdriver.Chrome) -> None:
    log.info("=== PARTE 3: Iframes ===")
    wait = WebDriverWait(driver, TIMEOUT)
    driver.get(f"{BASE_URL}/iframe")
 
    # changes to iframe, locating via CSS Selector (without using mce_0_ifr)
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[id$='_ifr']")
        )
    )
    log.info("Foco movido para o iframe do editor.")
 
    corpo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce")))
 
    # TinyMCE/iframe bodies do not reliably accept Selenium's .clear()/send_keys() apparently
    # in this page, so i'm clearing and setting the editor text directly via JS.
    driver.execute_script("arguments[0].innerHTML = ''; arguments[0].textContent = '';", corpo)
    assert corpo.text.strip() == "", "O editor deveria estar vazio após limpar"
    log.info("Editor limpo.")

    mensagem = f"Ola do robo Selenium! RA: {RA}"
    driver.execute_script("arguments[0].textContent = arguments[1];", corpo, mensagem)
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body#tinymce"), RA))
    assert RA in corpo.text, f"RA não encontrado no editor: {corpo.text!r}"
    log.info("Texto escrito no editor: %s", corpo.text)
 
    # goes back to main doc
    driver.switch_to.default_content()
    log.info("Foco devolvido ao documento principal.")
 
    # at root DOM: <h3> confirms that you left the iframe
    cabecalho = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    log.info("Cabeçalho <h3>: %s", cabecalho)
    assert "An iFrame containing the TinyMCE WYSIWYG Editor" in cabecalho, (
        f"<h3> inesperado: {cabecalho!r}"
    )
    log.info("Parte 3 validada com sucesso.")
 
 
# window/tab switching

XPATH_CLICK_HERE = "//a[normalize-space()='Click Here']"
 
 
def parte_4_janelas(driver: webdriver.Chrome) -> None:
    log.info("=== PARTE 4: Troca de abas ===")
    wait = WebDriverWait(driver, TIMEOUT)
    driver.get(f"{BASE_URL}/windows")
 
    handle_original = driver.current_window_handle
    titulo_original = driver.title
    log.info("Aba original: handle=%s | título=%r", handle_original, titulo_original)
 
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CLICK_HERE))).click()
 
    # waits till 2 windows
    wait.until(EC.number_of_windows_to_be(2))
    assert len(driver.window_handles) == 2, "Deveriam existir 2 handles"
    log.info("Nova aba detectada. Handles: %s", driver.window_handles)
 
    # changes focus to a different handle than main
    novo_handle = next(h for h in driver.window_handles if h != handle_original)
    driver.switch_to.window(novo_handle)
    assert driver.current_window_handle == novo_handle
 
    texto = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    log.info("Texto na nova aba: %s", texto)
    assert texto == "New Window", f"Esperado 'New Window', obtido {texto!r}"
 
    # closes new tab and returns to original
    driver.close()
    driver.switch_to.window(handle_original)
    wait.until(EC.number_of_windows_to_be(1))
 
    assert len(driver.window_handles) == 1, "Deveria restar apenas 1 handle"
    assert driver.title == titulo_original, (
        f"Título esperado {titulo_original!r}, obtido {driver.title!r}"
    )
    log.info("De volta à aba original (título=%r). Parte 4 validada.", driver.title)
 
 
# Bonus (hopefully)

def processar_novas_abas(
    driver: webdriver.Chrome, handle_original: str, handles_novos: list[str]
) -> dict[str, str]:
    wait = WebDriverWait(driver, TIMEOUT)
    conteudos: dict[str, str] = {}
    try:
        for handle in handles_novos:
            if handle == handle_original:
                continue  # doesn't close the original tab by mistake
            try:
                driver.switch_to.window(handle)
                texto = wait.until(
                    EC.visibility_of_element_located((By.TAG_NAME, "h3"))
                ).text
                conteudos[handle] = texto
                log.info("Aba %s -> %r", handle, texto)
                driver.close()
            except NoSuchWindowException:
                log.warning("Aba %s já havia sido fechada; ignorando.", handle)
    finally:
        # safe return to main tab
        driver.switch_to.window(handle_original)
    return conteudos
 
 
def parte_5_bonus(driver: webdriver.Chrome, qtd_cliques: int = 3) -> None:
    log.info("=== BÔNUS: múltiplas janelas (%d) ===", qtd_cliques)
    wait = WebDriverWait(driver, TIMEOUT)
    driver.get(f"{BASE_URL}/windows")
 
    handle_original = driver.current_window_handle
    titulo_original = driver.title
 
    # every click opens a new tab
    for _ in range(qtd_cliques):
        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CLICK_HERE))).click()
    wait.until(EC.number_of_windows_to_be(1 + qtd_cliques))
 
    handles_novos = [h for h in driver.window_handles if h != handle_original]
    assert len(handles_novos) == qtd_cliques, (
        f"Esperadas {qtd_cliques} abas novas, achei {len(handles_novos)}"
    )
 
    conteudos = processar_novas_abas(driver, handle_original, handles_novos)
 
    assert len(conteudos) == qtd_cliques, "Nem todas as abas foram lidas"
    assert all(t == "New Window" for t in conteudos.values()), conteudos
    wait.until(EC.number_of_windows_to_be(1))
    assert len(driver.window_handles) == 1, "Deveria restar apenas 1 handle"
    assert driver.current_window_handle == handle_original
    assert driver.title == titulo_original
    log.info("Bônus validado: %d abas lidas e fechadas.", len(conteudos))
 
 
# Main

def main() -> int:
    driver = criar_driver()
    try:
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_janelas(driver)
        parte_5_bonus(driver)
        log.info("Todas as partes foram concluídas com sucesso.")
        return 0
    except AssertionError:
        log.exception("Falha em uma validação (assert).")
        return 1
    except Exception:
        log.exception("Erro inesperado durante a execução.")
        return 1
    finally:
        driver.quit()
        log.info("Navegador encerrado.")
 
 
if __name__ == "__main__":
    sys.exit(main())