import logging
import os
 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
 
RA = "6326057"
BASE_URL = "https://the-internet.herokuapp.com"
TIMEOUT = 10
 
# ---------------------------------------------------------------------------
# Configuração do logging (terminal + arquivo)
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("web_avancado.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)
 
 
def criar_driver():
    """Cria o Chrome. No CI (GitHub Actions) roda em modo headless."""
    opcoes = webdriver.ChromeOptions()
    if os.environ.get("CI"):
        opcoes.add_argument("--headless=new")
        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=opcoes)
 
 
# ---------------------------------------------------------------------------
# Parte 1 - Selects
# ---------------------------------------------------------------------------
def parte_1_selects(driver):
    logger.info("=== PARTE 1: Selects ===")
    driver.get(f"{BASE_URL}/dropdown")
    wait = WebDriverWait(driver, TIMEOUT)
 
    elemento = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select#dropdown")))
    select = Select(elemento)
 
    logger.info("Opções disponíveis no dropdown:")
    for indice, opcao in enumerate(select.options):
        logger.info("  [%d] %s", indice, opcao.text)
 
    select.select_by_index(2)  # índice 0 = "Please select an option", 1 = Option 1, 2 = Option 2
 
    selecionada = select.first_selected_option.text
    assert selecionada == "Option 2", f"Esperado 'Option 2', obtido '{selecionada}'"
    logger.info("Opção selecionada com sucesso: %s", selecionada)
 
 
# ---------------------------------------------------------------------------
# Parte 2 - Alerts JS (Alert, Confirm, Prompt)
# ---------------------------------------------------------------------------
def parte_2_alerts(driver):
    logger.info("=== PARTE 2: Alerts JS ===")
    driver.get(f"{BASE_URL}/javascript_alerts")
    wait = WebDriverWait(driver, TIMEOUT)
 
    # --- JS Alert ---
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']"))).click()
    alerta = wait.until(EC.alert_is_present())
    logger.info("Texto do JS Alert: %s", alerta.text)
    alerta.accept()
    resultado = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[@id='result']"))).text
    assert resultado == "You successfully clicked an alert", f"Resultado inesperado: {resultado}"
    logger.info("JS Alert aceito. Resultado: %s", resultado)
 
    # --- JS Confirm (cancelar) ---
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Confirm']"))).click()
    confirm = wait.until(EC.alert_is_present())
    logger.info("Texto do JS Confirm: %s", confirm.text)
    confirm.dismiss()
    wait.until(EC.text_to_be_present_in_element((By.ID, "result"), "Cancel"))
    resultado = driver.find_element(By.ID, "result").text
    assert resultado == "You clicked: Cancel", f"Resultado inesperado: {resultado}"
    logger.info("JS Confirm cancelado. Resultado: %s", resultado)
 
    # --- JS Prompt (enviar RA) ---
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Prompt']"))).click()
    prompt = wait.until(EC.alert_is_present())
    logger.info("Texto do JS Prompt: %s", prompt.text)
    prompt.send_keys(RA)
    prompt.accept()
    wait.until(EC.text_to_be_present_in_element((By.ID, "result"), RA))
    resultado = driver.find_element(By.ID, "result").text
    assert RA in resultado, f"RA não encontrado no resultado: {resultado}"
    logger.info("JS Prompt confirmado. Resultado: %s", resultado)
 
 
# ---------------------------------------------------------------------------
# Parte 3 - Iframes
# ---------------------------------------------------------------------------
def parte_3_iframes(driver):
    logger.info("=== PARTE 3: Iframes ===")
    driver.get(f"{BASE_URL}/iframe")
    wait = WebDriverWait(driver, TIMEOUT)

    # Espera o TinyMCE terminar de inicializar (senão ele sobrescreve o que digitarmos)
    wait.until(lambda d: d.execute_script(
        "return !!(window.tinymce && tinymce.activeEditor && tinymce.activeEditor.initialized);"
    ))
    logger.info("Editor TinyMCE inicializado")

    # Se o editor estiver em modo somente leitura, liberamos a edição
    modo = driver.execute_script("return tinymce.activeEditor.mode.get();")
    if modo != "design":
        logger.warning("Editor em modo '%s' - liberando edição", modo)
        driver.execute_script("tinymce.activeEditor.mode.set('design');")

    # Localiza o iframe por CSS Selector (sem usar o ID fixo mce_0_ifr)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "div.tox-edit-area iframe")))
    logger.info("Foco trocado para o iframe do editor")

    corpo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body#tinymce")))
    corpo.click()                                   # coloca o cursor dentro do editor
    corpo.send_keys(Keys.CONTROL, "a")              # seleciona todo o conteúdo
    corpo.send_keys(Keys.DELETE)                    # apaga (limpa o editor)

    mensagem = f"Lab 09 concluído - RA {RA}"
    corpo.send_keys(mensagem)

    try:
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body#tinymce"), RA))
    except Exception:
        # Plano B: escreve direto no editor via JavaScript
        logger.warning("Digitação não refletiu no editor - escrevendo via JavaScript")
        driver.execute_script("arguments[0].innerHTML = '<p>' + arguments[1] + '</p>';", corpo, mensagem)

    texto_editor = driver.find_element(By.CSS_SELECTOR, "body#tinymce").text
    assert RA in texto_editor, f"Mensagem não foi escrita no editor: {texto_editor}"
    logger.info("Mensagem escrita no editor: %s", texto_editor)

    # Volta para o documento principal
    driver.switch_to.default_content()
    titulo = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert "iFrame" in titulo, f"Cabeçalho inesperado (ainda dentro do iframe?): {titulo}"
    logger.info("De volta ao DOM principal. <h3>: %s", titulo)


# ---------------------------------------------------------------------------
# Parte 4 - Troca de abas / janelas
# ---------------------------------------------------------------------------
def parte_4_janelas(driver):
    logger.info("=== PARTE 4: Abas / Janelas ===")
    driver.get(f"{BASE_URL}/windows")
    wait = WebDriverWait(driver, TIMEOUT)
 
    handle_original = driver.current_window_handle
    titulo_original = driver.title
    logger.info("Handle original: %s | Título: %s", handle_original, titulo_original)
 
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
    wait.until(EC.number_of_windows_to_be(2))
    logger.info("Nova aba detectada. Total de handles: %d", len(driver.window_handles))
 
    nova_aba = next(h for h in driver.window_handles if h != handle_original)
    driver.switch_to.window(nova_aba)
 
    texto = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert texto == "New Window", f"Texto inesperado na nova aba: {texto}"
    logger.info("Na nova aba. Texto exibido: %s", texto)
 
    driver.close()
    driver.switch_to.window(handle_original)
 
    assert len(driver.window_handles) == 1, f"Esperado 1 handle, existem {len(driver.window_handles)}"
    assert driver.title == titulo_original, f"Título inesperado: {driver.title}"
    logger.info("Nova aba fechada. De volta à aba original: %s", driver.title)
 
 
# ---------------------------------------------------------------------------
# Bônus - várias abas
# ---------------------------------------------------------------------------
def processar_novas_abas(driver, handle_original, handles):
    """Percorre todas as abas diferentes da original, lê o conteúdo, fecha
    cada uma e sempre retorna à aba original. Devolve a lista de conteúdos."""
    wait = WebDriverWait(driver, TIMEOUT)
    conteudos = []
 
    for handle in handles:
        if handle == handle_original:
            continue
        try:
            driver.switch_to.window(handle)
            texto = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).text
            conteudos.append(texto)
            logger.info("Aba %s lida: %s", handle, texto)
            driver.close()
        except Exception as erro:
            logger.error("Falha ao processar a aba %s: %s", handle, erro)
        finally:
            driver.switch_to.window(handle_original)
 
    return conteudos
 
 
def bonus_varias_janelas(driver, quantidade=3):
    logger.info("=== BÔNUS: %d abas ===", quantidade)
    driver.get(f"{BASE_URL}/windows")
    wait = WebDriverWait(driver, TIMEOUT)
    handle_original = driver.current_window_handle
 
    for i in range(quantidade):
        driver.switch_to.window(handle_original)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
        wait.until(EC.number_of_windows_to_be(i + 2))
 
    logger.info("Abas abertas: %d", len(driver.window_handles))
    conteudos = processar_novas_abas(driver, handle_original, driver.window_handles)
 
    assert len(conteudos) == quantidade, f"Esperado {quantidade} abas lidas, lidas {len(conteudos)}"
    assert all("New Window" in c for c in conteudos), "Alguma aba não exibiu 'New Window'"
    assert len(driver.window_handles) == 1, "Ainda existem abas extras abertas"
    assert driver.current_window_handle == handle_original
    logger.info("Bônus concluído: %d abas lidas e fechadas", len(conteudos))
 
 
# ---------------------------------------------------------------------------
# Execução principal
# ---------------------------------------------------------------------------
def main():
    driver = None
    try:
        driver = criar_driver()
        logger.info("Navegador iniciado")
 
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_janelas(driver)
        bonus_varias_janelas(driver)
 
        logger.info("Todas as partes foram concluídas com sucesso!")
    except AssertionError as erro:
        logger.error("Validação falhou: %s", erro)
        raise
    except Exception as erro:
        logger.critical("Erro inesperado: %s", erro)
        raise
    finally:
        if driver:
            driver.quit()
            logger.info("Navegador encerrado")
 
 
if __name__ == "__main__":
    main()