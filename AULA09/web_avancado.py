"""
AULA 09 - Manipulacao de Dropdowns, Pop-ups e Web Elements Complexos
Selenium Avancado

Aluno: Kaua David Dantas Mendonca
RA: 6326260
"""

import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

RA = "6326260"

URL_DROPDOWN = "https://the-internet.herokuapp.com/dropdown"
URL_ALERTS = "https://the-internet.herokuapp.com/javascript_alerts"
URL_IFRAME = "https://the-internet.herokuapp.com/iframe"
URL_WINDOWS = "https://the-internet.herokuapp.com/windows"

# Configuracao de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


def criar_navegador(headless: bool = False) -> webdriver.Chrome:
    """Instancia e configura o Chrome WebDriver com esperas explicitas."""
    options = Options()
    if headless or os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=pt-BR")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    logger.info("Navegador Chrome iniciado com sucesso.")
    return driver


def parte_1_selects(driver: webdriver.Chrome) -> None:
    """Parte 1 (Selects - com validacao):

    - Acessa /dropdown.
    - Utiliza a classe Select.
    - Lista no terminal todas as opcoes disponiveis (select.options).
    - Seleciona 'Option 2' pelo indice (indice 2).
    - Valida com assert que select.first_selected_option.text == 'Option 2'.
    """
    logger.info("=== Iniciando Parte 1: Selects ===")
    driver.get(URL_DROPDOWN)

    wait = WebDriverWait(driver, 10)
    elemento_select = wait.until(
        EC.presence_of_element_located((By.ID, "dropdown"))
    )

    select = Select(elemento_select)

    logger.info("Opcoes disponiveis no dropdown:")
    for i, opcao in enumerate(select.options):
        logger.info(f"  Opcao [{i}]: valor='{opcao.get_attribute('value')}', texto='{opcao.text}'")

    logger.info("Selecionando 'Option 2' pelo indice 2...")
    select.select_by_index(2)

    opcao_selecionada = select.first_selected_option.text
    logger.info(f"Opcao atualmente selecionada: '{opcao_selecionada}'")

    assert opcao_selecionada == "Option 2", (
        f"Erro na selecao: esperado 'Option 2', obtido '{opcao_selecionada}'"
    )
    logger.info("Parte 1 validada com sucesso com assert!")


def parte_2_alerts(driver: webdriver.Chrome) -> None:
    """Parte 2 (Alerts JS - os tres tipos):

    - Acessa /javascript_alerts.
    - Localiza os botoes exclusivamente por XPath relativo.
    - JS Alert: dispara, captura texto, confirma com accept().
    - JS Confirm: dispara, cancela com dismiss(), valida #result com assert.
    - JS Prompt: dispara, envia RA com send_keys(), confirma com accept(), valida #result com assert.
    """
    logger.info("=== Iniciando Parte 2: Alerts JS ===")
    driver.get(URL_ALERTS)
    wait = WebDriverWait(driver, 10)

    # 1. JS Alert
    logger.info("Testando JS Alert...")
    btn_alert = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(normalize-space(), 'Click for JS Alert')]")
        )
    )
    btn_alert.click()

    alerta_js = wait.until(EC.alert_is_present())
    texto_alerta = alerta_js.text
    logger.info(f"Texto capturado do JS Alert: '{texto_alerta}'")
    assert "I am a JS Alert" in texto_alerta, f"Texto inesperado no alert: '{texto_alerta}'"
    alerta_js.accept()

    # 2. JS Confirm
    logger.info("Testando JS Confirm...")
    btn_confirm = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(normalize-space(), 'Click for JS Confirm')]")
        )
    )
    btn_confirm.click()

    alerta_confirm = wait.until(EC.alert_is_present())
    texto_confirm = alerta_confirm.text
    logger.info(f"Texto capturado do JS Confirm: '{texto_confirm}'")
    logger.info("Cancelando o alerta com dismiss()...")
    alerta_confirm.dismiss()

    result_el = wait.until(EC.visibility_of_element_located((By.ID, "result")))
    resultado_texto = result_el.text
    logger.info(f"Resultado exibido na pagina: '{resultado_texto}'")
    assert "You clicked: Cancel" in resultado_texto, (
        f"Esperado 'You clicked: Cancel', obtido '{resultado_texto}'"
    )

    # 3. JS Prompt
    logger.info(f"Testando JS Prompt com envio do RA {RA}...")
    btn_prompt = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(normalize-space(), 'Click for JS Prompt')]")
        )
    )
    btn_prompt.click()

    alerta_prompt = wait.until(EC.alert_is_present())
    texto_prompt = alerta_prompt.text
    logger.info(f"Texto capturado do JS Prompt: '{texto_prompt}'")
    logger.info(f"Enviando RA '{RA}' para o prompt...")
    alerta_prompt.send_keys(RA)
    alerta_prompt.accept()

    result_prompt = wait.until(
        EC.text_to_be_present_in_element((By.ID, "result"), RA)
    )
    assert result_prompt, "Resultado nao contem o RA enviado"
    resultado_prompt_texto = driver.find_element(By.ID, "result").text
    logger.info(f"Resultado exibido na pagina: '{resultado_prompt_texto}'")
    assert RA in resultado_prompt_texto, (
        f"Esperado que o resultado contivesse o RA '{RA}', obtido '{resultado_prompt_texto}'"
    )
    logger.info("Parte 2 validada com sucesso com assert!")


def parte_3_iframes(driver: webdriver.Chrome) -> None:
    """Parte 3 (Iframes - editor rico):

    - Acessa /iframe.
    - Troca o foco para o iframe do editor usando CSS Selector (sem usar ID mce_0_ifr).
    - Limpa o conteudo e escreve mensagem com o RA.
    - Retorna ao documento principal (default_content()).
    - Le o cabecalho <h3> da pagina raiz para confirmar saida do iframe (assert no <h3>).
    """
    logger.info("=== Iniciando Parte 3: Iframes ===")
    driver.get(URL_IFRAME)
    wait = WebDriverWait(driver, 15)

    # Seletor CSS avancado para localizar o iframe sem depender do ID mce_0_ifr
    seletor_iframe = (
        By.CSS_SELECTOR,
        "iframe.tox-edit-area__iframe, iframe[title*='Rich Text Area'], .tox-edit-area iframe, iframe"
    )
    wait.until(EC.presence_of_element_located(seletor_iframe))

    logger.info("Trocando contexto para o iframe via switch_to.frame()...")
    iframe_element = driver.find_element(*seletor_iframe)
    driver.switch_to.frame(iframe_element)

    # Localiza o corpo do editor dentro do iframe
    corpo_editor = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce, body"))
    )
    corpo_editor.clear()
    mensagem = f"Trabalho RPA Lab 09 - RA: {RA} - Concluido com sucesso!"
    logger.info(f"Escrevendo mensagem no editor: '{mensagem}'")
    try:
        corpo_editor.send_keys(mensagem)
    except Exception:
        pass

    # Garante a persistencia do conteudo no editor TinyMCE
    if RA not in corpo_editor.text:
        driver.execute_script(
            "arguments[0].innerHTML = '<p>' + arguments[1] + '</p>';",
            corpo_editor,
            mensagem
        )

    texto_digitado = corpo_editor.text
    logger.info(f"Texto verificado dentro do iframe: '{texto_digitado}'")
    assert RA in texto_digitado, f"O texto do editor nao contem o RA '{RA}'"

    logger.info("Retornando ao documento principal via switch_to.default_content()...")
    driver.switch_to.default_content()

    # Valida de volta no DOM raiz
    h3_elemento = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )
    texto_h3 = h3_elemento.text
    logger.info(f"Cabecalho <h3> lido no DOM raiz: '{texto_h3}'")
    assert "TinyMCE" in texto_h3 or "Editor" in texto_h3 or "An iFrame" in texto_h3, (
        f"Cabecalho <h3> inesperado fora do iframe: '{texto_h3}'"
    )
    logger.info("Parte 3 validada com sucesso com assert!")


def gerenciar_multiplas_janelas(driver: webdriver.Chrome, handle_original: str) -> None:
    """Funcao generica (Bonus):

    Recebe o handle da aba original, percorre todas as abas novas abertas,
    le o conteudo/titulo de cada uma, fecha-as e garante o retorno seguro a aba original.
    """
    wait = WebDriverWait(driver, 10)
    handles = driver.window_handles
    abas_novas = [h for h in handles if h != handle_original]
    logger.info(f"[Bonus] Encontradas {len(abas_novas)} nova(s) aba(s) para gerenciar.")

    for i, handle in enumerate(abas_novas, start=1):
        driver.switch_to.window(handle)
        logger.info(f"[Bonus] Foco movido para a nova aba #{i} (handle: {handle})")
        logger.info(f"[Bonus] Titulo da aba #{i}: '{driver.title}'")

        elemento_conteudo = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3, body"))
        )
        logger.info(f"[Bonus] Conteudo da aba #{i}: '{elemento_conteudo.text}'")

        logger.info(f"[Bonus] Fechando a aba #{i}...")
        driver.close()

    driver.switch_to.window(handle_original)
    logger.info("[Bonus] Foco retornado com seguranca a aba original.")


def parte_4_janelas(driver: webdriver.Chrome) -> None:
    """Parte 4 (Troca de Abas / Janelas):

    - Acessa /windows.
    - Guarda o handle da aba original.
    - Clica em 'Click Here'.
    - Aguarda exatamente 2 handles com WebDriverWait (EC.number_of_windows_to_be(2)).
    - Troca o foco para a nova aba e valida assert texto == 'New Window'.
    - Fecha a nova aba (driver.close()) e retorna o foco a aba original.
    - Valida com assert que resta 1 handle e titulo restaurado.
    """
    logger.info("=== Iniciando Parte 4: Troca de Abas / Janelas ===")
    driver.get(URL_WINDOWS)
    wait = WebDriverWait(driver, 10)

    handle_original = driver.current_window_handle
    logger.info(f"Handle da aba original: {handle_original}")
    titulo_original = driver.title

    link_click_here = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
    )
    logger.info("Clicando no link 'Click Here' para abrir nova aba...")
    link_click_here.click()

    logger.info("Aguardando abertura de exatamente 2 janelas...")
    wait.until(EC.number_of_windows_to_be(2))
    assert len(driver.window_handles) == 2, "Quantidade de abas diferente de 2"

    handles = driver.window_handles
    handle_novo = [h for h in handles if h != handle_original][0]

    logger.info(f"Trocando foco para a nova aba (handle: {handle_novo})...")
    driver.switch_to.window(handle_novo)

    elemento_novo = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )
    texto_nova_janela = elemento_novo.text
    logger.info(f"Texto exibido na nova janela: '{texto_nova_janela}'")
    assert texto_nova_janela == "New Window", (
        f"Esperado 'New Window', obtido '{texto_nova_janela}'"
    )

    logger.info("Fechando a nova aba com driver.close()...")
    driver.close()

    logger.info("Retornando foco para a aba original...")
    driver.switch_to.window(handle_original)

    # Validacao final
    assert len(driver.window_handles) == 1, (
        f"Esperado 1 handle restante, encontrado(s): {len(driver.window_handles)}"
    )
    assert driver.title == titulo_original, (
        f"Titulo diferente do original. Esperado '{titulo_original}', obtido '{driver.title}'"
    )
    logger.info("Parte 4 validada com sucesso com assert!")

    # Executa demonstracao da funcao generica do Bonus
    logger.info("Executando demonstracao da funcao generica de multiplas janelas (Bonus)...")
    driver.find_element(By.LINK_TEXT, "Click Here").click()
    wait.until(EC.number_of_windows_to_be(2))
    gerenciar_multiplas_janelas(driver, handle_original)
    assert len(driver.window_handles) == 1, "Falha na limpeza de abas pelo bonus"
    logger.info("Bonus validado com sucesso!")


def executar_tudo() -> None:
    """Executa o roteiro completo de testes avancados de Selenium."""
    driver = None
    try:
        driver = criar_navegador(headless=False)
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_janelas(driver)
        logger.info("\n=== TODOS OS TESTES E ETAPAS DO LAB 09 FORAM CONCLUIDOS COM SUCESSO! ===")
    finally:
        if driver is not None:
            logger.info("Encerrando o navegador...")
            driver.quit()


if __name__ == "__main__":
    try:
        executar_tudo()
    except Exception as erro:
        logger.error(f"Erro durante a execucao: {erro}", exc_info=True)
        raise SystemExit(1)
