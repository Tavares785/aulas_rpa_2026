import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do Logging para registrar cada passo da automação
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Seu RA (substitua pelo seu número de matrícula real da faculdade)
MEU_RA = "6326108"


# ----------------------------------------------------------------------
# Função Bônus: Gerenciamento Genérico de Múltiplas Janelas
# ----------------------------------------------------------------------
def alternar_e_fechar_janelas_novas(driver, handle_original):
    """
    Percorre todas as abas/janelas abertas que não sejam a original,
    lê o conteúdo do corpo da página, fecha a aba e retorna o foco à original.
    """
    todos_handles = driver.window_handles
    for handle in todos_handles:
        if handle != handle_original:
            driver.switch_to.window(handle)
            texto_aba = driver.find_element(By.TAG_NAME, "body").text
            logging.info(f"[BÔNUS] Aba extra encontrada. Conteúdo: '{texto_aba[:30]}...'")
            driver.close()
    
    # Retorna com segurança para a aba inicial
    driver.switch_to.window(handle_original)


# ----------------------------------------------------------------------
# Parte 1: Dropdowns / Selects
# ----------------------------------------------------------------------
def parte_1_selects(driver):
    logging.info("--- Iniciando Parte 1: Selects ---")
    driver.get("https://the-internet.herokuapp.com/dropdown")
    wait = WebDriverWait(driver, 10)

    # Localiza o elemento <select>
    select_element = wait.until(EC.presence_of_element_located((By.ID, "dropdown")))
    select = Select(select_element)

    # 1. Listar todas as opções disponíveis
    opcoes = select.options
    logging.info("Opções disponíveis no Dropdown:")
    for opcao in opcoes:
        logging.info(f" - {opcao.text}")

    # 2. Selecionar 'Option 2' pelo índice (índice 2, pois o primeiro é 0 e o desabilitado é 0)
    select.select_by_index(2)

    # 3. Validação com assert
    opcao_selecionada = select.first_selected_option.text
    assert opcao_selecionada == "Option 2", f"Esperado 'Option 2', mas obteve '{opcao_selecionada}'"
    logging.info("Validação Parte 1 OK: 'Option 2' foi corretamente selecionada.")


# ----------------------------------------------------------------------
# Parte 2: Alerts JavaScript (três tipos)
# ----------------------------------------------------------------------
def parte_2_alerts(driver):
    logging.info("--- Iniciando Parte 2: JS Alerts ---")
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    wait = WebDriverWait(driver, 10)

    # --- 1. JS Alert (Apenas aviso) ---
    btn_alert = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Click for JS Alert')]"))
    )
    btn_alert.click()

    alert = wait.until(EC.alert_is_present())
    logging.info(f"JS Alert capturado. Texto: '{alert.text}'")
    alert.accept()

    # --- 2. JS Confirm (Confirmação -> Dismiss) ---
    btn_confirm = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Click for JS Confirm')]"))
    )
    btn_confirm.click()

    alert = wait.until(EC.alert_is_present())
    logging.info(f"JS Confirm capturado. Texto: '{alert.text}'")
    alert.dismiss()

    # Validação do resultado do confirm
    resultado = wait.until(EC.presence_of_element_located((By.ID, "result"))).text
    assert resultado == "You clicked: Cancel", f"Resultado inesperado no Confirm: '{resultado}'"
    logging.info("Validação JS Confirm OK: Cancelado com sucesso.")

    # --- 3. JS Prompt (Entrada de texto) ---
    btn_prompt = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Click for JS Prompt')]"))
    )
    btn_prompt.click()

    alert = wait.until(EC.alert_is_present())
    logging.info(f"JS Prompt capturado. Enviando RA: {MEU_RA}")
    alert.send_keys(MEU_RA)
    alert.accept()

    # Validação do resultado do prompt
    resultado_prompt = wait.until(EC.presence_of_element_located((By.ID, "result"))).text
    assert MEU_RA in resultado_prompt, f"RA não encontrado no resultado. Obtido: '{resultado_prompt}'"
    logging.info("Validação JS Prompt OK: RA enviado e confirmado.")


# ----------------------------------------------------------------------
# Parte 3: IFrames (Troca de Contexto)
# ----------------------------------------------------------------------
def parte_3_iframes(driver):
    logging.info("--- Iniciando Parte 3: IFrames ---")
    driver.get("https://the-internet.herokuapp.com/iframe")
    wait = WebDriverWait(driver, 10)

    # 1. Localiza o iframe via CSS Selector (sem usar o ID mce_0_ifr)
    iframe = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.tox-edit-area__iframe, iframe[title*='Rich Text Area']"))
    )

    # 2. Troca o contexto de execução para dentro do iframe
    driver.switch_to.frame(iframe)

    # 3. Limpa e escreva a mensagem com o RA no corpo do editor
    corpo_editor = wait.until(EC.presence_of_element_located((By.ID, "tinymce")))
    corpo_editor.clear()
    corpo_editor.send_keys(f"Trabalho de RPA executado pelo RA: {MEU_RA}")
    logging.info("Texto inserido com sucesso dentro do iframe.")

    # 4. Retorna ao documento principal (DOM raiz)
    driver.switch_to.default_content()

    # 5. Validação fora do iframe lendo o cabeçalho <h3> da página
    h3_texto = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3"))).text
    assert "An iFrame containing" in h3_texto, f"Não foi possível confirmar o retorno ao DOM principal. Encontrado: '{h3_texto}'"
    logging.info("Validação Parte 3 OK: Retorno ao DOM raiz confirmado via <h3>.")


# ----------------------------------------------------------------------
# Parte 4 (com Bônus): Troca de Janelas / Abas
# ----------------------------------------------------------------------
def parte_4_windows(driver):
    logging.info("--- Iniciando Parte 4: Múltiplas Janelas ---")
    driver.get("https://the-internet.herokuapp.com/windows")
    wait = WebDriverWait(driver, 10)

    # 1. Guarda o handle original
    handle_original = driver.current_window_handle

    # 2. Clica no link que abre nova aba
    link_nova_janela = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
    )
    link_nova_janela.click()

    # 3. Espera até que existam 2 janelas/abas
    wait.until(EC.number_of_windows_to_be(2))

    # 4. Identifica a nova aba e troca o foco
    handles = driver.window_handles
    novo_handle = [h for h in handles if h != handle_original][0]
    driver.switch_to.window(novo_handle)

    # 5. Valida o conteúdo da nova aba
    h3_nova_aba = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3"))).text
    assert h3_nova_aba == "New Window", f"Texto esperado 'New Window', obteve '{h3_nova_aba}'"
    logging.info("Validação da nova aba OK: 'New Window' exibido.")

    # Execução da Função Bônus (fechamento seguro de abas extras e retorno)
    alternar_e_fechar_janelas_novas(driver, handle_original)

    # 6. Validações finais na aba original
    assert len(driver.window_handles) == 1, "Ainda existe mais de uma aba aberta!"
    assert driver.current_window_handle == handle_original, "Foco não voltou para o handle original."
    
    titulo_pagina = driver.title
    assert "The Internet" in titulo_pagina, f"Título da página incorreto: '{titulo_pagina}'"
    logging.info("Validação Parte 4 OK: Retorno seguro à aba original confirmado.")


# ----------------------------------------------------------------------
# Fluxo Principal de Execução com Try/Except/Finally
# ----------------------------------------------------------------------
if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        parte_1_selects(driver)
        parte_2_alerts(driver)
        parte_3_iframes(driver)
        parte_4_windows(driver)
        logging.info("=== TODAS AS PARTES DO LAB 09 FORAM EXECUTADAS COM SUCESSO! ===")

    except Exception as e:
        logging.error(f"Ocorreu uma falha durante a execução da automação: {e}", exc_info=True)

    finally:
        # Garante que a instância do navegador seja encerrada
        driver.quit()
        logging.info("Navegador encerrado no bloco finally.")