import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Usar os logs como pedido
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Isso aqui é só pra testar kapa kapa
RA_ALUNO = "6326127"


def parte_1_selects(driver):
    """Tratamento de dropdowns utilizando a classe Select."""
    logger.info("Iniciando Parte 1: Selects")
    driver.get("https://the-internet.herokuapp.com/dropdown")
    
    # espera o elemento ficar ativo
    wait = WebDriverWait(driver, 10)
    dropdown_element = wait.until(EC.visibility_of_element_located((By.ID, "dropdown")))
    
    dropdown = Select(dropdown_element)
    
    # Robo me manda os bagulho zé
    logger.info("Opções disponíveis no dropdown:")
    for option in dropdown.options:
        logger.info(f" - Valor: '{option.get_attribute('value')}' | Texto: '{option.text}'")
        
    # Pega a opção 2
    dropdown.select_by_index(2)
    
    # Certification
    texto_selecionado = dropdown.first_selected_option.text
    assert texto_selecionado == "Option 2", f"Esperado 'Option 2', mas obteve '{texto_selecionado}'"
    logger.info("Parte 1 concluída com sucesso! 'Option 2' foi selecionada e validada.")


def parte_2_alerts(driver):
    """Captura e interação com caixas de diálogo nativas (Alerts) usando XPath relativo."""
    logger.info("Iniciando Parte 2: Alerts JS")
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    wait = WebDriverWait(driver, 10)
    
    # Alerta do JS
    btn_alert = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']")))
    btn_alert.click()
    alert = wait.until(EC.alert_is_present())
    logger.info(f"Texto do JS Alert capturado: '{alert.text}'")
    alert.accept()
    
    # Js confirm
    btn_confirm = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Confirm']")))
    btn_confirm.click()
    alert = wait.until(EC.alert_is_present())
    alert.dismiss()  # Cancela o alerta
    
    # validation do js confirm
    result_text = wait.until(EC.visibility_of_element_located((By.ID, "result"))).text
    assert result_text == "You clicked: Cancel", f"Esperado 'You clicked: Cancel', obtido: '{result_text}'"
    
    # Prompt do js
    btn_prompt = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Prompt']")))
    btn_prompt.click()
    alert = wait.until(EC.alert_is_present())
    alert.send_keys(RA_ALUNO)
    alert.accept()
    
    # VALIDATION
    result_text = wait.until(EC.visibility_of_element_located((By.ID, "result"))).text
    assert RA_ALUNO in result_text, f"O RA '{RA_ALUNO}' não foi encontrado no resultado: '{result_text}'"
    logger.info("Parte 2 concluída com sucesso! Todos os alertas validados.")


def parte_3_iframes(driver):
    """Alternância de contexto para operação dentro de Iframes."""
    logger.info("Iniciando Parte 3: Iframes")
    driver.get("https://the-internet.herokuapp.com/iframe")
    wait = WebDriverWait(driver, 10)
    
    # Pegando o Iframe (demônio) via css selector
    iframe_selector = (By.CSS_SELECTOR, "iframe.tox-edit-area__iframe, iframe[title*='Rich Text Area']")
    wait.until(EC.frame_to_be_available_and_switch_to_it(iframe_selector))
    
    # Localiza dentro do Iframe
    editor_body = wait.until(EC.element_to_be_clickable((By.ID, "tinymce")))
    editor_body.clear()
    editor_body.send_keys(f"Automação executada com sucesso pelo RA: {RA_ALUNO}")
    logger.info("Texto inserido com sucesso dentro do Iframe.")
    
    # Retorna ao documento principal
    driver.switch_to.default_content()
    
    # Validation no DOM raiz
    header_text = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert "An iFrame containing" in header_text, f"Falha ao sair do iframe. H3 atual: '{header_text}'"
    logger.info("Parte 3 concluída com sucesso! Foco retornado ao DOM principal.")


def parte_4_windows(driver):
    """Controle de múltiplas abas/janelas através de window_handles."""
    logger.info("Iniciando Parte 4: Troca de Abas / Janelas")
    driver.get("https://the-internet.herokuapp.com/windows")
    wait = WebDriverWait(driver, 10)
    
    handle_original = driver.current_window_handle
    
    # Abrir nova aba
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
    
    # Espera até dar duas janelas
    wait.until(EC.number_of_windows_to_be(2))
    
    # Localiza e altera o foco para o novo handle
    todos_handles = driver.window_handles
    handle_novo = [h for h in todos_handles if h != handle_original][0]
    driver.switch_to.window(handle_novo)
    
    # VALIDATION DA NOVA ABA
    texto_nova_janela = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
    assert texto_nova_janela == "New Window", f"Texto esperado 'New Window', obtido: '{texto_nova_janela}'"
    logger.info("Nova janela acessada e validada com sucesso.")
    
    # Fecha a nova aba e volta a original
    driver.close()
    driver.switch_to.window(handle_original)
    
    # Vallidações finais
    assert len(driver.window_handles) == 1, "Mais de uma janela ainda permanece aberta."
    titulo_atual = driver.title
    assert "The Internet" in titulo_atual, f"Título inesperado após retorno: '{titulo_atual}'"
    logger.info("Parte 4 concluída com sucesso! Foco restabelecido na aba de origem.")


def bonus_gerenciador_multi_abas(driver, handle_original):
    """Bônus: Função genérica para tratar N janelas abertas simultaneamente de forma segura."""
    logger.info("Iniciando Bônus: Gerenciador de Múltiplas Abas")
    wait = WebDriverWait(driver, 10)
    
    # Pega tudo que n for principal
    janelas_secundarias = [h for h in driver.window_handles if h != handle_original]
    logger.info(f"Detectadas {len(janelas_secundarias)} janelas secundárias para processamento.")
    
    for indice, handle in enumerate(janelas_secundarias, start=1):
        driver.switch_to.window(handle)
        # EXTRAÇÃO
        conteudo = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text.replace('\n', ' ')
        logger.info(f"Janela Secundária #{indice} [Handle: {handle}]: Conteúdo preliminar -> '{conteudo[:40]}...'")
        
        # Fecha de boa sem engano
        driver.close()
        
    # Retorna com segurança à origem
    driver.switch_to.window(handle_original)
    assert len(driver.window_handles) == 1, "Erro: Nem todas as abas secundárias foram encerradas."
    logger.info("Bônus executado com sucesso! Todas as abas secundárias foram limpas.")


def main():
    """Inicializador do ciclo de vida do WebDriver."""
    # Configuração do chrome
    options = webdriver.ChromeOptions()
    # Caso queira rodar em background só descomentar
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    
    try:
        # Execução final
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_windows(driver)
        
        # Demonstração do fluxo
        logger.info("Simulando o Bônus")
        driver.get("https://the-internet.herokuapp.com/windows")
        handle_origem = driver.current_window_handle
        # Força a abertura de 2 novas abas via JavaScript para alimentar a função genérica
        driver.execute_script("window.open('https://the-internet.herokuapp.com/dropdown', '_blank');")
        driver.execute_script("window.open('https://the-internet.herokuapp.com/javascript_alerts', '_blank');")
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(3))
        
        # Executa a função genérica
        bonus_gerenciador_multi_abas(driver, handle_origem)
        
    except Exception as e:
        logger.error(f"Ocorreu uma falha crítica durante a execução do robô: {e}", exc_info=True)
        raise e
    finally:
        logger.info("Encerrando sessão do WebDriver no bloco finally.")
        driver.quit()


if __name__ == "__main__":
    main()
