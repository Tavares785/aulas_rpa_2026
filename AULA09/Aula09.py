"""
web_avancado.py
Selenium avançado: Selects, Alertas JS, Iframes e Troca de Abas/Janelas.

Regras seguidas:
- Sem time.sleep(): toda sincronização usa WebDriverWait + expected_conditions.
- Uma função por parte.
- Cada ação relevante validada com assert e registrada com logging.
- try/except/finally com driver.quit() no finally.
"""

import logging
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


RA = "6326297"  
BASE_URL = "https://the-internet.herokuapp.com"
TIMEOUT = 10

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("web_avancado")


def esperar(driver: WebDriver) -> WebDriverWait:
    """Atalho para criar o WebDriverWait padrão."""
    return WebDriverWait(driver, TIMEOUT)



def parte_1_selects(driver: WebDriver) -> None:
    log.info("=== PARTE 1: Selects ===")
    driver.get(f"{BASE_URL}/dropdown")

    elemento = esperar(driver).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select#dropdown"))
    )
    select = Select(elemento)

    log.info("Opções disponíveis no menu suspenso:")
    for i, opcao in enumerate(select.options):
        log.info("  [%d] %r", i, opcao.text)

    
    select.select_by_index(2)
    log.info("Selecionada a opção de índice 2")

    selecionada = select.first_selected_option.text
    assert selecionada == "Option 2", f"Esperado 'Option 2', obtido {selecionada!r}"
    log.info("OK: opção selecionada validada -> %s", selecionada)



def _ler_resultado(driver: WebDriver) -> str:
    return esperar(driver).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#result"))
    ).text


def parte_2_alerts(driver: WebDriver) -> None:
    log.info("=== PARTE 2: Alertas JS ===")
    driver.get(f"{BASE_URL}/javascript_alerts")

    
    xp_alert = "//button[contains(text(), 'JS Alert')]"
    xp_confirm = "//button[contains(text(), 'JS Confirm')]"
    xp_prompt = "//button[contains(text(), 'JS Prompt')]"

    
    esperar(driver).until(EC.element_to_be_clickable((By.XPATH, xp_alert))).click()
    alerta = esperar(driver).until(EC.alert_is_present())
    texto = alerta.text
    log.info("Texto do JS Alert: %r", texto)
    assert texto == "I am a JS Alert", f"Texto inesperado no alert: {texto!r}"
    alerta.accept()
    resultado = _ler_resultado(driver)
    assert "successfully clicked an alert" in resultado, resultado
    log.info("OK: JS Alert aceito -> %s", resultado)

    
    esperar(driver).until(EC.element_to_be_clickable((By.XPATH, xp_confirm))).click()
    confirmacao = esperar(driver).until(EC.alert_is_present())
    log.info("Texto do JS Confirm: %r", confirmacao.text)
    confirmacao.dismiss()
    resultado = _ler_resultado(driver)
    
    assert ("Cancel" in resultado) or ("Cancelar" in resultado), resultado
    log.info("OK: JS Confirm cancelado -> %s", resultado)

    
    esperar(driver).until(EC.element_to_be_clickable((By.XPATH, xp_prompt))).click()
    prompt = esperar(driver).until(EC.alert_is_present())
    log.info("Texto do JS Prompt: %r", prompt.text)
    prompt.send_keys(RA)
    prompt.accept()
    resultado = _ler_resultado(driver)
    assert RA in resultado, f"RA {RA!r} não encontrado em {resultado!r}"
    log.info("OK: JS Prompt aceito com RA -> %s", resultado)



def parte_3_iframes(driver: WebDriver) -> None:
    log.info("=== PARTE 3: Iframes ===")
    driver.get(f"{BASE_URL}/iframe")

    
    seletor_iframe = "div.tox-edit-area > iframe"
    esperar(driver).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, seletor_iframe))
    )
    log.info("Foco trocado para o iframe do editor")

    corpo = esperar(driver).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "body#tinymce"))
    )
    corpo.clear()
    mensagem = f"Ola do robo Selenium! RA: {RA}"
    corpo.send_keys(mensagem)
    escrito = corpo.text
    assert RA in escrito, f"RA não encontrado no editor: {escrito!r}"
    log.info("OK: mensagem escrita no editor -> %r", escrito)

    
    driver.switch_to.default_content()
    log.info("Foco devolvido ao documento principal")

    cabecalho = esperar(driver).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3"))
    ).text
    assert "iFrame" in cabecalho, f"<h3> inesperado: {cabecalho!r}"
    log.info("OK: de volta à raiz do DOM, <h3> = %r", cabecalho)



def parte_4_janelas(driver: WebDriver) -> None:
    log.info("=== PARTE 4: Troca de Abas/Janelas ===")
    driver.get(f"{BASE_URL}/windows")

    handle_original = driver.current_window_handle
    titulo_original = driver.title
    log.info("Handle original: %s | título: %r", handle_original, titulo_original)

    esperar(driver).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Click Here']"))
    ).click()

    esperar(driver).until(EC.number_of_windows_to_be(2))
    log.info("Duas janelas detectadas")

    novos = [h for h in driver.window_handles if h != handle_original]
    assert len(novos) == 1, f"Esperava 1 aba nova, achei {len(novos)}"
    driver.switch_to.window(novos[0])

    texto = esperar(driver).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.example h3"))
    ).text
    assert texto == "New Window", f"Texto inesperado na nova aba: {texto!r}"
    log.info("OK: nova aba exibe %r", texto)

    driver.close()
    driver.switch_to.window(handle_original)
    log.info("Aba nova fechada; foco devolvido à original")

    assert len(driver.window_handles) == 1, "Deveria restar apenas 1 aba"
    assert driver.title == titulo_original, (
        f"Título esperado {titulo_original!r}, obtido {driver.title!r}"
    )
    h3 = esperar(driver).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.example h3"))
    ).text
    assert h3 == "Opening a new window", f"<h3> inesperado: {h3!r}"
    log.info("OK: 1 aba restante, título e conteúdo da página de janelas confirmados")



def processar_novas_abas(driver: WebDriver, handle_original: str) -> Dict[str, str]:
    """
    Percorre todas as abas diferentes da original, lê o <h3> de cada uma
    e a fecha. Sempre retorna o foco à aba original (mesmo em caso de erro).
    Retorna {handle: texto_lido}.
    """
    conteudos: Dict[str, str] = {}
    novas: List[str] = [h for h in driver.window_handles if h != handle_original]
    log.info("Processando %d aba(s) nova(s)", len(novas))

    try:
        for handle in novas:
            driver.switch_to.window(handle)
            texto = esperar(driver).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h3"))
            ).text
            conteudos[handle] = texto
            log.info("Aba %s -> %r", handle, texto)
            driver.close()
    finally:
        driver.switch_to.window(handle_original)
        log.info("Foco restaurado na aba original")
    return conteudos


def parte_5_bonus(driver: WebDriver) -> None:
    log.info("=== BÔNUS: múltiplas janelas ===")
    driver.get(f"{BASE_URL}/windows")
    handle_original = driver.current_window_handle

    link_xpath = "//a[text()='Click Here']"
    quantidade = 3  
    for _ in range(quantidade):
        esperar(driver).until(EC.element_to_be_clickable((By.XPATH, link_xpath))).click()

    esperar(driver).until(EC.number_of_windows_to_be(quantidade + 1))
    conteudos = processar_novas_abas(driver, handle_original)

    assert len(conteudos) == quantidade, f"Lidas {len(conteudos)} abas, esperado {quantidade}"
    assert all(t == "New Window" for t in conteudos.values()), conteudos
    assert len(driver.window_handles) == 1, "Deveria restar apenas a aba original"
    assert driver.current_window_handle == handle_original
    log.info("OK: bônus concluído, %d abas lidas e fechadas", quantidade)



def main() -> None:
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_janelas(driver)
        parte_5_bonus(driver)
        log.info("Todas as partes concluídas com sucesso")
    except AssertionError:
        log.exception("Falha de validação (assert)")
        raise
    except Exception:
        log.exception("Erro inesperado durante a automação")
        raise
    finally:
        driver.quit()
        log.info("Driver encerrado")


if __name__ == "__main__":
    main()