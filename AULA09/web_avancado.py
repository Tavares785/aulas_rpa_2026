"""
Lab 09 - Dropdowns, alerts, iframes e multiplas abas com Selenium.

Cada parte do lab fica numa funcao propria. Nenhuma espera usa time.sleep:
toda sincronizacao e feita com WebDriverWait + expected_conditions, cada acao
importante e conferida com assert e registrada com logging.

Instalar: pip install selenium
Rodar:    python AULA09/web_avancado.py
          (defina HEADLESS=1 para rodar sem abrir a janela do navegador)
"""
import logging
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

RA = "6326200"
BASE = "https://the-internet.herokuapp.com"
ESPERA = 15

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("web_avancado")


def criar_driver():
    """Abre o Chrome; com HEADLESS=1 roda sem janela (util em servidor/CI)."""
    opcoes = webdriver.ChromeOptions()
    if os.environ.get("HEADLESS") == "1":
        opcoes.add_argument("--headless=new")
        opcoes.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=opcoes)


def esperar(driver):
    return WebDriverWait(driver, ESPERA)


# ---------------------------------------------------------------- Parte 1
def parte_1_selects(driver):
    """Lista as opcoes do dropdown e escolhe a 'Option 2' pelo indice."""
    driver.get(f"{BASE}/dropdown")
    elemento = esperar(driver).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "select#dropdown"))
    )
    select = Select(elemento)

    log.info("Parte 1 - opcoes do dropdown:")
    for indice, opcao in enumerate(select.options):
        log.info("  [%d] %s", indice, opcao.text)

    select.select_by_index(2)
    escolhida = select.first_selected_option.text
    assert escolhida == "Option 2", f"Esperava 'Option 2', veio '{escolhida}'"
    log.info("Parte 1 OK - selecionado pelo indice 2: %s", escolhida)


# ---------------------------------------------------------------- Parte 2
def clicar_botao_alert(driver, texto_botao):
    """Clica no botao localizado por XPath relativo (pelo texto, sem ID)."""
    botao = esperar(driver).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[text()='{texto_botao}']"))
    )
    botao.click()
    return esperar(driver).until(EC.alert_is_present())


def ler_resultado(driver):
    return esperar(driver).until(
        EC.visibility_of_element_located((By.XPATH, "//p[@id='result']"))
    ).text


def parte_2_alerts(driver):
    """Trata os tres tipos de alert JS: alert, confirm e prompt."""
    driver.get(f"{BASE}/javascript_alerts")

    alerta = clicar_botao_alert(driver, "Click for JS Alert")
    log.info("Parte 2 - JS Alert diz: %s", alerta.text)
    alerta.accept()
    assert "successfully clicked an alert" in ler_resultado(driver)
    log.info("Parte 2 - JS Alert aceito")

    confirmacao = clicar_botao_alert(driver, "Click for JS Confirm")
    log.info("Parte 2 - JS Confirm diz: %s", confirmacao.text)
    confirmacao.dismiss()
    resultado = ler_resultado(driver)
    assert resultado == "You clicked: Cancel", f"Resultado inesperado: {resultado}"
    log.info("Parte 2 - JS Confirm cancelado: %s", resultado)

    prompt = clicar_botao_alert(driver, "Click for JS Prompt")
    log.info("Parte 2 - JS Prompt diz: %s", prompt.text)
    prompt.send_keys(RA)
    prompt.accept()
    resultado = ler_resultado(driver)
    assert RA in resultado, f"RA nao apareceu no resultado: {resultado}"
    log.info("Parte 2 OK - prompt respondido: %s", resultado)


# ---------------------------------------------------------------- Parte 3
def escrever_no_editor(driver, corpo, mensagem):
    """Limpa o editor e digita a mensagem como um usuario faria.

    O body do TinyMCE perde o foco depois de um clear(), entao clicamos,
    selecionamos tudo (Ctrl+A), apagamos e digitamos. Se o editor estiver
    em modo somente leitura, escrevemos direto no DOM do iframe.
    """
    if corpo.get_attribute("contenteditable") == "true":
        corpo.click()
        corpo.send_keys(Keys.CONTROL, "a")
        corpo.send_keys(Keys.DELETE)
        corpo.send_keys(mensagem)
    if mensagem not in corpo.text:
        log.warning("Parte 3 - teclado nao escreveu no editor; usando o DOM")
        driver.execute_script(
            "arguments[0].innerHTML = '<p>' + arguments[1] + '</p>';",
            corpo, mensagem)


def parte_3_iframe(driver):
    """Escreve no editor que fica dentro do iframe e volta ao documento."""
    driver.get(f"{BASE}/iframe")
    # CSS sem o ID fixo "mce_0_ifr": cobre o TinyMCE 4 (.mce-edit-area),
    # o 5/6 (.tox-edit-area__iframe) e, por garantia, id terminando em _ifr.
    seletor_iframe = ("iframe.tox-edit-area__iframe, div.mce-edit-area iframe, "
                      "iframe[id$='_ifr']")
    esperar(driver).until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, seletor_iframe)
    ))
    corpo = esperar(driver).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce"))
    )
    mensagem = f"Mensagem escrita pelo robo do RA {RA}"
    escrever_no_editor(driver, corpo, mensagem)
    assert RA in corpo.text, "A mensagem com o RA nao ficou no editor"
    log.info("Parte 3 - escrito no iframe: %s", corpo.text)

    driver.switch_to.default_content()
    titulo = esperar(driver).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    ).text
    assert "Editor" in titulo, f"Nao voltou ao documento principal: {titulo}"
    log.info("Parte 3 OK - de volta ao DOM raiz, <h3>: %s", titulo)


# ---------------------------------------------------------------- Parte 4
def parte_4_janelas(driver):
    """Abre a nova aba, confere o conteudo, fecha e volta para a original."""
    driver.get(f"{BASE}/windows")
    original = driver.current_window_handle
    titulo_original = driver.title

    esperar(driver).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
    ).click()
    esperar(driver).until(EC.number_of_windows_to_be(2))

    nova = next(h for h in driver.window_handles if h != original)
    driver.switch_to.window(nova)
    texto = esperar(driver).until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    ).text
    assert texto == "New Window", f"Texto inesperado na nova aba: {texto}"
    log.info("Parte 4 - nova aba aberta com o texto: %s", texto)

    driver.close()
    driver.switch_to.window(original)
    assert len(driver.window_handles) == 1, "Sobrou aba aberta"
    assert driver.title == titulo_original, f"Titulo mudou: {driver.title}"
    log.info("Parte 4 OK - aba fechada, de volta em '%s'", driver.title)


# ---------------------------------------------------------------- Bonus
def fechar_abas_novas(driver, handle_original):
    """Percorre TODAS as abas alem da original, le cada uma e fecha.

    Serve para qualquer quantidade de janelas novas e sempre termina com o
    foco de volta na aba original.
    """
    conteudos = []
    for handle in list(driver.window_handles):
        if handle == handle_original:
            continue
        driver.switch_to.window(handle)
        texto = esperar(driver).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        ).text
        conteudos.append(texto)
        log.info("Bonus - aba %s: %s", handle[-6:], texto)
        driver.close()
    driver.switch_to.window(handle_original)
    assert driver.window_handles == [handle_original]
    return conteudos


def bonus_varias_janelas(driver, quantidade=3):
    """Clica 'Click Here' varias vezes e fecha todas as abas novas."""
    driver.get(f"{BASE}/windows")
    original = driver.current_window_handle
    for vez in range(1, quantidade + 1):
        esperar(driver).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
        ).click()
        esperar(driver).until(EC.number_of_windows_to_be(vez + 1))
        driver.switch_to.window(original)

    conteudos = fechar_abas_novas(driver, original)
    assert len(conteudos) == quantidade
    log.info("Bonus OK - %d abas lidas e fechadas", len(conteudos))


def main():
    driver = None
    try:
        driver = criar_driver()
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframe(driver)
        parte_4_janelas(driver)
        bonus_varias_janelas(driver)
        log.info("Todas as partes concluidas com sucesso.")
    except AssertionError as erro:
        log.error("Validacao falhou: %s", erro)
        raise
    except Exception:
        log.exception("Erro inesperado durante a automacao")
        raise
    finally:
        if driver is not None:
            driver.quit()
            log.info("Navegador fechado.")


if __name__ == "__main__":
    main()
