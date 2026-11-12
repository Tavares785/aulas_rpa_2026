import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Configuração do sistema de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

RA_EXEMPLO = "RA20261234"


def parte_1_selects(driver):
    """Parte 1: Manipulação de Selects com validação."""
    logging.info("--- Iniciando Parte 1: Selects ---")
    driver.get("https://the-internet.herokuapp.com/dropdown")
    
    wait = WebDriverWait(driver, 10)
    dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "dropdown")))
    select = Select(dropdown_element)
    
    logging.info("Listando todas as opções disponíveis no dropdown:")
    for opt in select.options:
        logging.info(f" -> Opção encontrada: '{opt.text}'")
        
    # Selecionar "Option 2" pelo índice (Índice 2, já que 0 é o placeholder padrão)
    select.select_by_index(2)
    logging.info("Selecionada a opção no índice 2.")
    
    # Validação com assert
    selected_option = select.first_selected_option
    logging.info(f"Opção atualmente selecionada: '{selected_option.text}'")
    assert selected_option.text == "Option 2", f"Erro: Esperado 'Option 2', mas obteve '{selected_option.text}'"
    logging.info("Parte 1 validada com sucesso!")


def parte_2_alerts(driver, ra):
    """Parte 2: Alertas JS (Alert, Confirm, Prompt) usando XPath relativo."""
    logging.info("--- Iniciando Parte 2: Alerts JS ---")
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    wait = WebDriverWait(driver, 10)
    
    # 1. JS Alert
    btn_alert = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']")))
    btn_alert.click()
    
    alert = wait.until(EC.alert_is_present())
    logging.info(f"Alerta JS capturado com texto: '{alert.text}'")
    alert.accept()
    
    # 2. JS Confirm (Cancelar)
    btn_confirm = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Confirm']")))
    btn_confirm.click()
    
    alert = wait.until(EC.alert_is_present())
    alert.dismiss()
    logging.info("JS Confirm cancelado (dismiss).")
    
    result_element = wait.until(EC.visibility_of_element_located((By.ID, "result")))
    result_text = result_element.text
    logging.info(f"Texto de resultado exibido: '{result_text}'")
    assert result_text == "You clicked: Cancel", f"Erro: Esperado 'You clicked: Cancel', obteve '{result_text}'"
    
    # 3. JS Prompt (Enviar RA)
    btn_prompt = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Prompt']")))
    btn_prompt.click()
    
    alert = wait.until(EC.alert_is_present())
    logging.info(f"Enviando RA '{ra}' para o Prompt JS.")
    alert.send_keys(ra)
    alert.accept()
    
    result_element = wait.until(EC.visibility_of_element_located((By.ID, "result")))
    result_text = result_element.text
    logging.info(f"Texto de resultado do Prompt exibido: '{result_text}'")
    assert ra in result_text, f"Erro: O RA '{ra}' não foi encontrado no texto '{result_text}'"
    logging.info("Parte 2 validada com sucesso!")


def parte_3_iframes(driver, ra):
    """Parte 3: Interação com Iframe utilizando CSS Selector."""
    logging.info("--- Iniciando Parte 3: Iframes ---")
    driver.get("https://the-internet.herokuapp.com/iframe")
    wait = WebDriverWait(driver, 10)
    
    # Localizando o iframe por CSS Selector (evitando o ID fixo mce_0_ifr)
    iframe_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[id*='mce_0_ifr']")))
    driver.switch_to.frame(iframe_element)
    logging.info("Foco trocado para o iframe do editor.")
    
    body = wait.until(EC.presence_of_element_located((By.ID, "tinymce")))
    body.clear()
    mensagem = f"Automação Web Avançada - RA: {ra}"
    body.send_keys(mensagem)
    logging.info(f"Texto inserido no editor: '{mensagem}'")
    
    # Retornar ao documento principal
    driver.switch_to.default_content()
    logging.info("Retornado ao documento principal (default_content).")
    
    # Validar cabeçalho h3 na raiz para confirmar saída do iframe
    h3_element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
    h3_text = h3_element.text
    logging.info(f"Cabeçalho H3 da página principal: '{h3_text}'")
    assert "An iFrame containing the TinyMCE WYSIWYG Editor" in h3_text, f"Erro: Cabeçalho inesperado '{h3_text}'"
    logging.info("Parte 3 validada com sucesso!")


def parte_4_windows(driver):
    """Parte 4: Troca de Abas / Janelas."""
    logging.info("--- Iniciando Parte 4: Troca de Abas / Janelas ---")
    driver.get("https://the-internet.herokuapp.com/windows")
    wait = WebDriverWait(driver, 10)
    
    handle_original = driver.current_window_handle
    logging.info(f"Handle original guardado: {handle_original}")
    
    link_click_here = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
    link_click_here.click()
    logging.info("Link 'Click Here' clicado para abrir nova aba.")
    
    # Esperar existirem exatamente 2 janelas/abas
    wait.until(EC.number_of_windows_to_be(2))
    
    # Descobrir o handle da nova aba
    all_handles = driver.window_handles
    handle_nova = [h for h in all_handles if h != handle_original][0]
    
    # Trocar foco para a nova aba
    driver.switch_to.window(handle_nova)
    logging.info("Foco alterado para a nova aba.")
    
    # Validar texto na nova página
    h3_nova = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
    logging.info(f"Texto H3 na nova aba: '{h3_nova.text}'")
    assert h3_nova.text == "New Window", f"Erro: Esperado 'New Window', obtido '{h3_nova.text}'"
    
    # Fechar a nova aba e retornar para a original
    driver.close()
    logging.info("Nova aba fechada.")
    driver.switch_to.window(handle_original)
    logging.info("Foco retornado à aba original.")
    
    # Validações finais
    assert len(driver.window_handles) == 1, f"Erro: Esperado 1 handle remanescente, encontrados {len(driver.window_handles)}"
    assert "The Internet" in driver.title, f"Erro: Título da página original incorreto: '{driver.title}'"
    logging.info("Parte 4 validada com sucesso!")


def bonus_gerenciar_multiplas_janelas(driver):
    logging.info("--- Iniciando Bônus: Gerenciamento Genérico de Múltiplas Janelas ---")
    driver.get("https://the-internet.herokuapp.com/windows")
    wait = WebDriverWait(driver, 10)
    
    handle_original = driver.current_window_handle
    
    # Acionando a abertura de uma nova aba
    link_click_here = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
    link_click_here.click()
    wait.until(EC.number_of_windows_to_be(2))
    
    def fechar_todas_exceto_original(drv, original_h):
        for handle in drv.window_handles:
            if handle != original_h:
                drv.switch_to.window(handle)
                logging.info(f"Processando aba extra (URL: {drv.current_url}, Título: {drv.title}). Fechando...")
                drv.close()
        drv.switch_to.window(original_h)
        assert len(drv.window_handles) == 1, "Erro: Mais de uma aba permaneceu aberta."
        logging.info("Todas as abas extras foram fechadas com segurança e o foco retornou à origem.")

    fechar_todas_exceto_original(driver, handle_original)
    logging.info("Bônus executado com sucesso!")


def main():
    driver = None
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")  # Descomente se preferir executar em modo headless
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        
        # Executando as partes do desafio em ordem
        parte_1_selects(driver)
        parte_2_alerts(driver, ra=RA_EXEMPLO)
        parte_3_iframes(driver, ra=RA_EXEMPLO)
        parte_4_windows(driver)
        bonus_gerenciar_multiplas_janelas(driver)
        
        logging.info("=== TODAS AS ETAPAS FORAM CONCLUÍDAS COM SUCESSO! ===")
        
    except Exception as e:
        logging.error(f"Erro crítico durante a execução do script: {e}", exc_info=True)
        raise
    finally:
        if driver:
            driver.quit()
            logging.info("Instância do WebDriver encerrada com sucesso no bloco finally.")


if __name__ == "__main__":
    main()