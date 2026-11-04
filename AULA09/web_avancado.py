"""
Lab 09 - Manipulacao de Dropdowns, Pop-ups e Web Elements Complexos
Aluno RA: 6326017

Roteiro (cada parte em sua propria funcao):
    Parte 1 - Select: lista as opcoes e seleciona "Option 2" pelo indice.
    Parte 2 - Alerts JS: Alert (accept), Confirm (dismiss) e Prompt (send_keys).
    Parte 3 - Iframe: escreve no editor TinyMCE e volta ao documento principal.
    Parte 4 - Abas/Janelas: abre nova aba, valida o conteudo, fecha e volta.
    Bonus   - Varias abas novas tratadas por uma funcao generica.

Regras seguidas:
    - Sincronizacao SOMENTE com WebDriverWait + expected_conditions
      (nada de time.sleep e nada de implicitly_wait misturado com esperas explicitas).
    - Toda acao relevante validada por assert e registrada com logging.
    - try/except/finally garantindo driver.quit().

Uso:
    python AULA09/web_avancado.py              # abre o Chrome visivel
    python AULA09/web_avancado.py --headless   # roda sem abrir janela
"""
import logging
import sys

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

RA = "6326017"
BASE_URL = "https://the-internet.herokuapp.com"
TIMEOUT = 10  # segundos maximos de espera explicita

# Parte 1: o indice 0 e o placeholder desabilitado "Please select an option",
# entao "Option 1" fica no indice 1 e "Option 2" no indice 2.
INDICE_OPTION_2 = 2

# Parte 2: XPath RELATIVO (comeca com //) localizando o botao pelo texto,
# sem depender de nenhum id da pagina.
XPATH_BOTAO_POR_TEXTO = "//button[normalize-space()='{}']"
CSS_RESULTADO = "#result"

# Parte 3: CSS Selector pela classe do iframe do TinyMCE (nao usa o id fixo mce_0_ifr).
CSS_IFRAME_EDITOR = "iframe.tox-edit-area__iframe"
H3_PAGINA_IFRAME = "An iFrame containing the TinyMCE WYSIWYG Editor"

# Parte 4 / Bonus
TITULO_PAGINA_JANELAS = "The Internet"
H3_PAGINA_JANELAS = "Opening a new window"
H3_NOVA_JANELA = "New Window"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("web_avancado")


def esperar(driver: webdriver.Chrome) -> WebDriverWait:
    # Atalho para criar a espera explicita padrao do roteiro.
    return WebDriverWait(driver, TIMEOUT)


def criar_driver(headless: bool) -> webdriver.Chrome:
    # O Selenium 4.6+ baixa o chromedriver sozinho (Selenium Manager).
    opcoes = Options()
    if headless:
        opcoes.add_argument("--headless=new")
    opcoes.add_argument("--window-size=1366,768")
    driver = webdriver.Chrome(options=opcoes)
    log.info("Chrome iniciado (headless=%s).", headless)
    return driver


# --------------------------------------------------------------------------
# PARTE 1 - Selects
# --------------------------------------------------------------------------
def parte_1_selects(driver: webdriver.Chrome) -> None:
    log.info("===== PARTE 1: Selects =====")
    driver.get(f"{BASE_URL}/dropdown")

    elemento = esperar(driver).until(EC.element_to_be_clickable((By.ID, "dropdown")))
    select = Select(elemento)

    # Lista TODAS as opcoes disponiveis do dropdown.
    textos = []
    for indice, opcao in enumerate(select.options):
        situacao = "habilitada" if opcao.is_enabled() else "desabilitada"
        log.info("Opcao [%d]: %s (%s)", indice, opcao.text, situacao)
        textos.append(opcao.text)
    assert "Option 2" in textos, f"'Option 2' nao existe no dropdown: {textos}"

    # Seleciona pelo INDICE (nao pelo texto).
    select.select_by_index(INDICE_OPTION_2)
    selecionada = select.first_selected_option.text
    assert selecionada == "Option 2", f"Esperado 'Option 2', obtido '{selecionada}'"
    log.info("OK - indice %d selecionado: '%s'", INDICE_OPTION_2, selecionada)


# --------------------------------------------------------------------------
# PARTE 2 - Alerts JS (Alert, Confirm e Prompt)
# --------------------------------------------------------------------------
def disparar_alerta(driver: webdriver.Chrome, texto_botao: str):
    # Clica no botao (localizado por XPath relativo) e espera o alert nativo abrir.
    xpath = XPATH_BOTAO_POR_TEXTO.format(texto_botao)
    botao = esperar(driver).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    botao.click()
    # alert_is_present() ja devolve o objeto Alert quando ele aparece.
    # ATENCAO: com o alert aberto o navegador nao aceita outros comandos
    # (find_element, execute_script...) ate ele ser fechado.
    return esperar(driver).until(EC.alert_is_present(), message=f"Alert de '{texto_botao}' nao abriu")


def ler_resultado(driver: webdriver.Chrome, texto_esperado: str) -> str:
    # Espera o #result ser atualizado com o texto esperado e devolve o texto lido.
    esperar(driver).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, CSS_RESULTADO), texto_esperado),
        message=f"#result nao exibiu '{texto_esperado}'",
    )
    return driver.find_element(By.CSS_SELECTOR, CSS_RESULTADO).text


def parte_2_alerts(driver: webdriver.Chrome) -> None:
    log.info("===== PARTE 2: Alerts JS =====")
    driver.get(f"{BASE_URL}/javascript_alerts")

    # 2.1 JS Alert -> captura o texto e confirma com accept()
    alerta = disparar_alerta(driver, "Click for JS Alert")
    texto_alerta = alerta.text
    alerta.accept()
    log.info("JS Alert capturado: '%s' -> accept()", texto_alerta)
    assert texto_alerta == "I am a JS Alert", f"Texto inesperado no alert: '{texto_alerta}'"
    resultado = ler_resultado(driver, "You successfully clicked an alert")
    log.info("OK - #result: '%s'", resultado)

    # 2.2 JS Confirm -> cancela com dismiss()
    confirmacao = disparar_alerta(driver, "Click for JS Confirm")
    log.info("JS Confirm capturado: '%s' -> dismiss()", confirmacao.text)
    confirmacao.dismiss()
    resultado = ler_resultado(driver, "You clicked: Cancel")
    assert resultado == "You clicked: Cancel", f"#result inesperado: '{resultado}'"
    log.info("OK - #result: '%s'", resultado)

    # 2.3 JS Prompt -> digita o RA com send_keys() e confirma com accept()
    prompt = disparar_alerta(driver, "Click for JS Prompt")
    log.info("JS Prompt capturado: '%s' -> send_keys('%s') + accept()", prompt.text, RA)
    prompt.send_keys(RA)
    prompt.accept()
    resultado = ler_resultado(driver, RA)
    assert RA in resultado, f"RA '{RA}' nao aparece no #result: '{resultado}'"
    log.info("OK - #result: '%s'", resultado)


# --------------------------------------------------------------------------
# PARTE 3 - Iframe (editor rico TinyMCE)
# --------------------------------------------------------------------------
def parte_3_iframe(driver: webdriver.Chrome) -> None:
    log.info("===== PARTE 3: Iframe =====")
    driver.get(f"{BASE_URL}/iframe")

    # Espera o iframe existir e JA troca o contexto para dentro dele.
    esperar(driver).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, CSS_IFRAME_EDITOR)))
    log.info("Contexto trocado para o iframe do editor.")

    # Dentro do iframe o editor e o proprio <body id="tinymce" contenteditable>.
    editor = esperar(driver).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body#tinymce")))
    editor.clear()
    # O click() da o foco ao editor; sem ele o send_keys nao chega ao TinyMCE.
    editor.click()
    mensagem = f"Mensagem escrita pelo robo RPA - RA {RA}"
    editor.send_keys(mensagem)

    esperar(driver).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body#tinymce"), RA))
    assert editor.text == mensagem, f"Conteudo do editor inesperado: '{editor.text}'"
    log.info("OK - texto no editor: '%s'", editor.text)

    # Volta para o documento principal (DOM raiz).
    driver.switch_to.default_content()
    h3 = esperar(driver).until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
    assert h3.text == H3_PAGINA_IFRAME, f"<h3> inesperado (ainda dentro do iframe?): '{h3.text}'"
    log.info("OK - fora do iframe, <h3>: '%s'", h3.text)


# --------------------------------------------------------------------------
# PARTE 4 - Troca de abas / janelas
# --------------------------------------------------------------------------
def parte_4_janelas(driver: webdriver.Chrome) -> None:
    log.info("===== PARTE 4: Abas / Janelas =====")
    driver.get(f"{BASE_URL}/windows")

    handle_original = driver.current_window_handle
    log.info("Handle da aba original: %s", handle_original)

    link = esperar(driver).until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
    link.click()
    esperar(driver).until(EC.number_of_windows_to_be(2), message="A nova aba nao abriu")
    log.info("Abas abertas: %d", len(driver.window_handles))

    # A nova aba e o handle diferente do original.
    handle_nova = next(h for h in driver.window_handles if h != handle_original)
    driver.switch_to.window(handle_nova)
    h3 = esperar(driver).until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
    assert h3.text == H3_NOVA_JANELA, f"Texto da nova aba inesperado: '{h3.text}'"
    log.info("OK - foco na nova aba (%s), texto: '%s'", handle_nova, h3.text)

    # Fecha a nova aba e devolve o foco para a original.
    driver.close()
    driver.switch_to.window(handle_original)

    assert len(driver.window_handles) == 1, f"Esperado 1 handle, existem {len(driver.window_handles)}"
    assert driver.title == TITULO_PAGINA_JANELAS, f"Titulo inesperado: '{driver.title}'"
    h3_original = driver.find_element(By.TAG_NAME, "h3").text
    assert h3_original == H3_PAGINA_JANELAS, f"<h3> inesperado na aba original: '{h3_original}'"
    log.info("OK - 1 handle aberto, de volta em '%s' (%s)", driver.title, h3_original)


# --------------------------------------------------------------------------
# BONUS - Varias abas novas
# --------------------------------------------------------------------------
def fechar_abas_extras(driver: webdriver.Chrome, handle_original: str) -> None:
    # Fecha qualquer aba que nao seja a original e devolve o foco a ela.
    for handle in driver.window_handles:
        if handle != handle_original:
            driver.switch_to.window(handle)
            driver.close()
    driver.switch_to.window(handle_original)


def processar_abas_novas(driver: webdriver.Chrome, handle_original: str, handles: list) -> list:
    """Percorre todas as abas novas da lista, le o conteudo de cada uma e a fecha.

    Funciona para qualquer quantidade de abas. O finally garante que, mesmo
    se algo falhar no meio do caminho, nenhuma aba extra fique aberta e o
    foco volte para a aba original.
    """
    conteudos = []
    abas_novas = [h for h in handles if h != handle_original]
    try:
        for posicao, handle in enumerate(abas_novas, start=1):
            driver.switch_to.window(handle)
            h3 = esperar(driver).until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
            conteudos.append({"handle": handle, "titulo": driver.title, "texto": h3.text})
            log.info("Aba nova %d/%d (%s): titulo='%s' texto='%s'",
                     posicao, len(abas_novas), handle, driver.title, h3.text)
            driver.close()
    finally:
        fechar_abas_extras(driver, handle_original)
    return conteudos


def bonus_multiplas_janelas(driver: webdriver.Chrome, quantidade: int = 3) -> None:
    log.info("===== BONUS: %d abas novas =====", quantidade)
    driver.get(f"{BASE_URL}/windows")
    handle_original = driver.current_window_handle

    link = esperar(driver).until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
    for aberta in range(1, quantidade + 1):
        link.click()
        # Espera cada aba nova existir antes do proximo clique.
        esperar(driver).until(EC.number_of_windows_to_be(1 + aberta), message=f"Aba {aberta} nao abriu")
    log.info("Abas abertas: %d", len(driver.window_handles))

    conteudos = processar_abas_novas(driver, handle_original, driver.window_handles)

    assert len(conteudos) == quantidade, f"Esperado {quantidade} abas lidas, lidas {len(conteudos)}"
    assert all(c["texto"] == H3_NOVA_JANELA for c in conteudos), f"Conteudo inesperado: {conteudos}"
    assert driver.window_handles == [handle_original], "Sobraram abas abertas"
    assert driver.current_window_handle == handle_original, "O foco nao voltou para a aba original"
    assert driver.title == TITULO_PAGINA_JANELAS, f"Titulo inesperado: '{driver.title}'"
    log.info("OK - %d abas lidas e fechadas, foco de volta na aba original.", len(conteudos))


# --------------------------------------------------------------------------
# Execucao
# --------------------------------------------------------------------------
def main() -> int:
    headless = "--headless" in sys.argv
    driver = None
    try:
        driver = criar_driver(headless)
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframe(driver)
        parte_4_janelas(driver)
        bonus_multiplas_janelas(driver)
        log.info("Todas as partes concluidas com sucesso!")
        return 0
    except AssertionError as erro:
        log.error("Validacao falhou: %s", erro)
        return 1
    except WebDriverException as erro:
        # Inclui TimeoutException (espera explicita estourada) e falhas do navegador.
        log.error("Erro do Selenium/navegador: %s", erro.msg or erro)
        return 1
    except Exception:
        log.exception("Erro inesperado")
        return 1
    finally:
        if driver is not None:
            driver.quit()
            log.info("Navegador encerrado (driver.quit).")


if __name__ == "__main__":
    sys.exit(main())
