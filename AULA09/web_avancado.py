import logging
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. Configuração de registo estruturado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

RA_ALUNO = "6326020"
TEMPO_LIMITE = 10


def parte_1_selects(driver: webdriver.Chrome):
    logging.info("--- A iniciar Parte 1: Manipulação de Selects ---")
    driver.get("https://the-internet.herokuapp.com/dropdown")

    espera = WebDriverWait(driver, TEMPO_LIMITE)
    elemento_dropdown = espera.until(
        EC.presence_of_element_located((By.ID, "dropdown"))
    )

    menu = Select(elemento_dropdown)
    opcoes = [opcao.text for opcao in menu.options]
    logging.info(f"Opções encontradas: {opcoes}")

    # Selecionar "Option 2" pelo índice 2
    menu.select_by_index(2)

    opcao_ativa = menu.first_selected_option.text
    logging.info(f"Opção atualmente selecionada: '{opcao_ativa}'")
    assert opcao_ativa == "Option 2", f"Esperado 'Option 2', mas obteve '{opcao_ativa}'"
    logging.info("Parte 1 concluída e validada com sucesso!")


def parte_2_alerts(driver: webdriver.Chrome):
    logging.info("--- A iniciar Parte 2: Alertas JS ---")
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    espera = WebDriverWait(driver, TEMPO_LIMITE)

    # 1. Alerta JS Simples
    btn_alert = espera.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Click for JS Alert']"))
    )
    btn_alert.click()

    espera.until(EC.alert_is_present())
    alerta = driver.switch_to.alert
    logging.info(f"Texto capturado do JS Alert: '{alerta.text}'")
    alerta.accept()

    # 2. JS Confirm
    btn_confirm = espera.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Click for JS Confirm']"))
    )
    btn_confirm.click()

    espera.until(EC.alert_is_present())
    alerta = driver.switch_to.alert
    logging.info("A cancelar o JS Confirm com dismiss()...")
    alerta.dismiss()

    elemento_resultado = espera.until(EC.visibility_of_element_located((By.ID, "result")))
    logging.info(f"Texto do resultado: '{elemento_resultado.text}'")
    assert elemento_resultado.text == "You clicked: Cancel", f"Esperado 'You clicked: Cancel', mas obteve '{elemento_resultado.text}'"

    # 3. JS Prompt
    btn_prompt = espera.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Click for JS Prompt']"))
    )
    btn_prompt.click()

    espera.until(EC.alert_is_present())
    alerta = driver.switch_to.alert
    logging.info(f"A enviar RA ({RA_ALUNO}) para o JS Prompt...")
    alerta.send_keys(RA_ALUNO)
    alerta.accept()

    espera.until(EC.text_to_be_present_in_element((By.ID, "result"), RA_ALUNO))
    texto_final = driver.find_element(By.ID, "result").text
    logging.info(f"Resultado final do Prompt: '{texto_final}'")
    assert RA_ALUNO in texto_final, f"RA '{RA_ALUNO}' não encontrado no resultado: '{texto_final}'"
    logging.info("Parte 2 concluída e validada com sucesso!")


def parte_3_iframes(driver: webdriver.Chrome):
    logging.info("--- A iniciar Parte 3: Iframes ---")
    driver.get("https://the-internet.herokuapp.com/iframe")
    espera = WebDriverWait(driver, TEMPO_LIMITE)

    try:
        botao_fechar = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.tox-notification button[aria-label='Close']"))
        )
        botao_fechar.click()
    except Exception:
        pass

    # Localizar o iframe via seletor CSS genérico
    elemento_iframe = espera.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.tox-edit-area__iframe"))
    )
    driver.switch_to.frame(elemento_iframe)

    corpo_editor = espera.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce"))
    )
    corpo_editor.clear()
    mensagem = f"Trabalho RPA - Aluno RA {RA_ALUNO}"
    corpo_editor.send_keys(mensagem)
    logging.info(f"Mensagem inserida no iframe: '{mensagem}'")

    driver.switch_to.default_content()

    cabecalho_h3 = espera.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )
    logging.info(f"Texto do cabeçalho h3 fora do iframe: '{cabecalho_h3.text}'")
    assert "An iFrame containing the TinyMCE WYSIWYG Editor" in cabecalho_h3.text, "Erro: não regressou à raiz do DOM."
    logging.info("Parte 3 concluída e validada com sucesso!")


def gerenciar_abas_secundarias(driver: webdriver.Chrome, handle_original: str):
    """Função genérica (Bónus): itera por janelas abertas, valida o conteúdo, fecha-as e regressa à origem."""
    todos_handles = driver.window_handles
    abas_secundarias = [h for h in todos_handles if h != handle_original]

    for handle in abas_secundarias:
        driver.switch_to.window(handle)
        espera = WebDriverWait(driver, TEMPO_LIMITE)
        conteudo = espera.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
        logging.info(f"[Aba Secundária {handle}] Conteúdo h3: '{conteudo}'")
        assert conteudo == "New Window", f"Esperado 'New Window', mas obteve '{conteudo}'"
        driver.close()

    # Retorno seguro ao separador principal
    driver.switch_to.window(handle_original)


def parte_4_windows(driver: webdriver.Chrome):
    logging.info("--- A iniciar Parte 4: Troca de Abas / Janelas (com Bónus) ---")
    driver.get("https://the-internet.herokuapp.com/windows")
    espera = WebDriverWait(driver, TEMPO_LIMITE)

    handle_original = driver.current_window_handle
    logging.info(f"Handle original guardado: {handle_original}")

    link_click_here = espera.until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Click Here']"))
    )
    link_click_here.click()

    # Aguardar até haver 2 janelas registadas
    espera.until(EC.number_of_windows_to_be(2))
    logging.info("Detetadas 2 janelas abertas.")

    # Fecho genérico com o bónus implementado
    gerenciar_abas_secundarias(driver, handle_original)

    # Validações finais no separador principal
    assert len(driver.window_handles) == 1, f"Deveria restar apenas 1 handle, mas existem {len(driver.window_handles)}"

    titulo_h3 = driver.find_element(By.TAG_NAME, "h3").text
    assert titulo_h3 == "Opening a new window", f"Título inesperado: '{titulo_h3}'"
    logging.info("Parte 4 concluída e validada com sucesso!")


def main():
    opcoes_navegador = webdriver.ChromeOptions()
    opcoes_navegador.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opcoes_navegador,
    )

    try:
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_windows(driver)
        logging.info("🎉 Todas as 4 partes foram executadas e validadas com sucesso!")
    except Exception as erro:
        logging.error(f"Ocorreu uma falha na execução: {erro}", exc_info=True)
        raise
    finally:
        logging.info("A fechar o navegador no bloco finally...")
        driver.quit()


if __name__ == "__main__":
    main()