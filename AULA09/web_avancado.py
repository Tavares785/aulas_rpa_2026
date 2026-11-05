import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

RA = "6326066"


def parte_1_selects(driver, wait):
    logging.info("Iniciando Parte 1: Selects")
    driver.get("https://the-internet.herokuapp.com/dropdown")
    
    dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "dropdown")))
    select = Select(dropdown_element)
    
    logging.info("Opções disponíveis:")
    for option in select.options:
        logging.info(f"- {option.text}")
        
    # Option 2 geralmente está no índice 2 (índice 0 é o placeholder)
    select.select_by_index(2)
    
    assert select.first_selected_option.text == "Option 2", "Opção 2 não foi selecionada corretamente."
    logging.info("Validação Parte 1 OK: Option 2 selecionada.")


def parte_2_alerts(driver, wait):
    logging.info("Iniciando Parte 2: Alerts JS")
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    
    # JS Alert
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'JS Alert')]"))).click()
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    logging.info(f"Texto do Alert: {alert.text}")
    alert.accept()
    
    # JS Confirm
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'JS Confirm')]"))).click()
    wait.until(EC.alert_is_present())
    driver.switch_to.alert.dismiss()
    
    resultado_confirm = wait.until(EC.presence_of_element_located((By.ID, "result"))).text
    assert resultado_confirm == "You clicked: Cancel", "Falha na validação do cancelamento do JS Confirm."
    logging.info("Validação JS Confirm OK: Cancelamento detectado.")
    
    # JS Prompt
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'JS Prompt')]"))).click()
    wait.until(EC.alert_is_present())
    prompt = driver.switch_to.alert
    prompt.send_keys(RA)
    prompt.accept()
    
    resultado_prompt = wait.until(EC.presence_of_element_located((By.ID, "result"))).text
    assert RA in resultado_prompt, f"Falha na validação do JS Prompt. RA {RA} não encontrado no resultado."
    logging.info("Validação JS Prompt OK: RA inserido e confirmado.")


def parte_3_iframes(driver, wait):
    logging.info("Iniciando Parte 3: Iframes")
    driver.get("https://the-internet.herokuapp.com/iframe")
    
    # Localizar iframe por CSS Selector genérico (ex: iframe cujo id contém 'ifr' ou pela tag)
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[id$='_ifr']")))
    driver.switch_to.frame(iframe)
    
    editor_body = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce")))
    editor_body.clear()
    editor_body.send_keys(f"Trabalho de Automação - RA: {RA}")
    logging.info("Texto inserido no iframe.")
    
    driver.switch_to.default_content()
    
    cabecalho = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3"))).text
    assert "An iFrame containing the TinyMCE WYSIWYG Editor" in cabecalho, "Falha ao retornar para o DOM principal."
    logging.info("Validação Parte 3 OK: Retorno ao DOM principal confirmado pelo <h3>.")


def parte_4_troca_janelas(driver, wait):
    logging.info("Iniciando Parte 4: Troca de Janelas")
    driver.get("https://the-internet.herokuapp.com/windows")
    
    handle_original = driver.current_window_handle
    
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))).click()
    wait.until(EC.number_of_windows_to_be(2))
    
    # Identificar a nova aba
    handles = driver.window_handles
    nova_aba = [handle for handle in handles if handle != handle_original][0]
    
    driver.switch_to.window(nova_aba)
    texto_nova_aba = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3"))).text
    assert texto_nova_aba == "New Window", "Falha na validação do conteúdo da nova aba."
    logging.info("Validação nova aba OK: Título 'New Window' encontrado.")
    
    driver.close()
    driver.switch_to.window(handle_original)
    
    assert len(driver.window_handles) == 1, "Falha: Mais de uma janela continua aberta."
    titulo_original = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3"))).text
    assert "Opening a new window" in titulo_original, "Falha ao retornar para a janela original."
    logging.info("Validação Parte 4 OK: Retorno seguro à aba original e nova aba fechada.")


def bonus_fechar_multiplas_janelas(driver, handle_original):
    logging.info("Iniciando Bônus: Fechar múltiplas janelas")
    handles = driver.window_handles
    
    for handle in handles:
        if handle != handle_original:
            driver.switch_to.window(handle)
            logging.info(f"Fechando janela auxiliar: {driver.title}")
            driver.close()
            
    driver.switch_to.window(handle_original)
    logging.info("Todas as janelas extras fechadas. Foco na original.")


if __name__ == "__main__":
    driver = webdriver.Chrome()  # Ajuste se estiver rodando o script no Ubuntu/Linux sem interface (add options)
    wait = WebDriverWait(driver, 10)
    
    try:
        parte_1_selects(driver, wait)
        parte_2_alerts(driver, wait)
        parte_3_iframes(driver, wait)
        parte_4_troca_janelas(driver, wait)
        
        # Chamada do bônus (simulada)
        # bonus_fechar_multiplas_janelas(driver, driver.current_window_handle)
        
    except AssertionError as e:
        logging.error(f"Erro de validação: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado na execução: {e}")
    finally:
        logging.info("Encerrando WebDriver.")
        driver.quit()
