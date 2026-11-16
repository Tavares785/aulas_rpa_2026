import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do sistema de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

RA_ALUNO = "123456"  # Substitua pelo seu RA real

def criar_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Remova o comentário se quiser rodar em background
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def parte_1_selects(driver):
    logging.info("--- Iniciando Parte 1: Selects ---")
    driver.get("https://the-internet.herokuapp.com/dropdown")
    
    # Aguarda o elemento select estar visível
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dropdown"))
    )
    
    select = Select(select_element)
    
    # Lista todas as opções disponíveis no terminal
    logging.info("Opções disponíveis no dropdown:")
    for option in select.options:
        logging.info(f" - {option.text}")
        
    # Seleciona a "Option 2" pelo índice (índice 2 corresponde à "Option 2")
    select.select_by_index(2)
    
    # Valida com assert
    selected_text = select.first_selected_option.text
    logging.info(f"Opção selecionada atualmente: {selected_text}")
    assert selected_text == "Option 2", f"Esperado 'Option 2', mas obteve '{selected_text}'"
    logging.info("Parte 1 concluída com sucesso!")

def parte_2_alerts(driver):
    logging.info("--- Iniciando Parte 2: Alerts JS ---")
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    
    # 1. JS Alert (Localizando botão por XPath relativo)
    btn_alert = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']"))
    )
    btn_alert.click()
    
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    logging.info(f"Texto capturado no JS Alert: {alert.text}")
    alert.accept()
    
    result_text = driver.find_element(By.ID, "result").text
    assert "You successfully clicked an alert" in result_text
    
    # 2. JS Confirm
    btn_confirm = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Confirm']"))
    )
    btn_confirm.click()
    
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert.dismiss() # Cancela o alerta
    
    result_text = driver.find_element(By.ID, "result").text
    logging.info(h := f"Resultado após cancelar: {result_text}")
    assert result_text == "You clicked: Cancel", f"Esperado 'You clicked: Cancel', obteve '{result_text}'"
    
    # 3. JS Prompt
    btn_prompt = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Prompt']"))
    )
    btn_prompt.click()
    
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert.send_keys(RA_ALUNO)
    alert.accept()
    
    result_text = driver.find_element(By.ID, "result").text
    logging.info(f"Resultado após prompt: {result_text}")
    assert RA_ALUNO in result_text, f"O RA {RA_ALUNO} não foi encontrado no texto de resultado."
    logging.info("Parte 2 concluída com sucesso!")

def parte_3_iframes(driver):
    logging.info("--- Iniciando Parte 3: Iframes ---")
    driver.get("https://the-internet.herokuapp.com/iframe")
    
    # Localiza o iframe por CSS Selector (evitando o ID fixo mce_0_ifr)
    iframe_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSSSelector, "div.tox-edit-area > iframe, #content iframe"))
    )
    
    # Troca o contexto para o iframe
    driver.switch_to.frame(iframe_element)
    
    # Limpa e escreve a mensagem contendo o RA dentro do editor
    editor_body = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tinymce"))
    )
    editor_body.clear()
    mensagem = f"Automação realizada com sucesso. RA: {RA_ALUNO}"
    editor_body.send_keys(mensagem)
    logging.info(f"Texto inserido no iframe: {mensagem}")
    
    # Retorna ao documento principal (DOM raiz)
    driver.switch_to.default_content()
    
    # Valida que retornou ao documento principal lendo o cabeçalho <h3>
    h3_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_H3, "h3") if hasattr(By, 'TAG_H3') else (By.TAG_NAME, "h3"))
    ).text
    
    logging.info(f"Cabeçalho H3 encontrado no DOM raiz: {h3_text}")
    assert "An iFrame containing the TinyMCE WYSIWYG Editor" in h3_text
    logging.info("Parte 3 concluída com sucesso!")

def parte_4_janelas(driver):
    logging.info("--- Iniciando Parte 4: Troca de Abas / Janelas ---")
    driver.get("https://the-internet.herokuapp.com/windows")
    
    handle_original = driver.current_window_handle
    logging.info(f"Handle da aba original: {handle_original}")
    
    # Clica no link que abre uma nova aba
    link_click_here = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
    )
    link_click_here.click()
    
    # Espera até existirem exatamente 2 abas/janelas
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    
    # Identifica o handle da nova aba
    handles = driver.window_handles
    handle_nova = [h for h in handles if h != handle_original][0]
    
    # Troca o foco para a nova aba
    driver.switch_to.window(handle_nova)
    
    # Valida que o texto exibido é "New Window"
    novo_titulo_texto = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h3"))
    ).text
    logging.info(f"Texto na nova aba: {novo_titulo_texto}")
    assert novo_titulo_texto == "New Window", f"Esperado 'New Window', obtido '{novo_titulo_texto}'"
    
    # Fecha a nova aba e retorna à original
    driver.close()
    driver.switch_to.window(handle_original)
    
    # Valida que voltou a ter apenas 1 handle e que o título da página está correto
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(1))
    assert len(driver.window_handles) == 1
    
    titulo_pagina = driver.title
    logging.info(f"Título da página original recuperado: {titulo_pagina}")
    assert "The Internet" in titulo_pagina
    logging.info("Parte 4 concluída com sucesso!")

if __name__ == "__main__":
    driver = criar_driver()
    try:
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_janelas(driver)
        logging.info("🎉 Todos os testes do Lab 09 foram executados com sucesso!")
    except Exception as e:
        logging.error(f"Erro durante a execução dos testes: {e}")
        raise
    finally:
        driver.quit()
        logging.info("Driver encerrado com segurança.")