import logging
import sys
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# ==============================================================================
# CONFIGURAÇÃO DE LOGGING E CONSTANTES DE TEMPO
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ⚠️ SUBSTITUA PELO SEU RA REAL:
MEU_RA = "3917176"

# Tempos ampliados para conexões lentas ou lentidão no servidor Herokuapp:
TIMEOUT_ESPERA_EXPLICITA = 30  # Segundos máximos para o WebDriverWait esperar elementos
TIMEOUT_CARREGAMENTO_PAGINA = 60  # Segundos máximos para o driver.get() carregar a URL
PAUSA_VISUAL = 2.0  # Segundos de pausa APENAS para efeito visual didático (0 para desativar)


def pausa_didatica(segundos: float = PAUSA_VISUAL) -> None:
    """
    Pausa estritamente didática para visualização humana APÓS a sincronização
    explícita já ter ocorrido via WebDriverWait (conforme permitido no enunciado).
    """
    if segundos > 0:
        time.sleep(segundos)


def aguardar_documento_pronto(driver: webdriver.Firefox, wait: WebDriverWait) -> None:
    """Garante via espera explícita que o DOM terminou de carregar (readyState == complete)."""
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")


# ==============================================================================
# PARTE 1: SELECTS (COM VALIDAÇÃO)
# ==============================================================================
def parte_1_selects(driver: webdriver.Firefox) -> None:
    logging.info("=== INICIANDO PARTE 1: SELECTS ===")
    driver.get("https://the-internet.herokuapp.com/dropdown")
    wait = WebDriverWait(driver, TIMEOUT_ESPERA_EXPLICITA)
    aguardar_documento_pronto(driver, wait)

    # Aguarda o elemento <select> estar presente, visível e clicável
    elemento_dropdown = wait.until(
        EC.element_to_be_clickable((By.ID, "dropdown"))
    )
    select = Select(elemento_dropdown)

    # 1. Listar no terminal todas as opções disponíveis
    opcoes_disponiveis = [opcao.text for opcao in select.options]
    logging.info(f"Opções disponíveis no dropdown: {opcoes_disponiveis}")
    assert len(select.options) > 1, "O dropdown deveria conter mais de uma opção."
    pausa_didatica(1.0)

    # 2. Selecionar a 'Option 2' pelo ÍNDICE
    select.select_by_index(2)
    logging.info("Ação executada: seleção pelo índice 2.")
    pausa_didatica()

    # 3. Validar com assert que a opção selecionada é 'Option 2'
    texto_selecionado = select.first_selected_option.text
    assert texto_selecionado == "Option 2", (
        f"Falha na validação: esperado 'Option 2', mas obteve '{texto_selecionado}'."
    )
    logging.info(f"Validação concluída com sucesso! Opção ativa: '{texto_selecionado}'\n")


# ==============================================================================
# PARTE 2: ALERTS JS (OS TRÊS TIPOS)
# ==============================================================================
def parte_2_alerts(driver: webdriver.Firefox, ra: str) -> None:
    logging.info("=== INICIANDO PARTE 2: ALERTS JS ===")
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    wait = WebDriverWait(driver, TIMEOUT_ESPERA_EXPLICITA)
    aguardar_documento_pronto(driver, wait)

    # --- 1. JS Alert ---
    btn_alert = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//ul/li/button[normalize-space()='Click for JS Alert']"))
    )
    btn_alert.click()

    alerta_1 = wait.until(EC.alert_is_present())
    texto_alerta_1 = alerta_1.text
    logging.info(f"[JS Alert] Texto capturado: '{texto_alerta_1}'")
    assert texto_alerta_1 == "I am a JS Alert", "Texto do JS Alert inesperado."
    pausa_didatica(1.5)
    alerta_1.accept()

    resultado_el = wait.until(EC.visibility_of_element_located((By.ID, "result")))
    assert resultado_el.text == "You successfully clicked an alert", "Falha ao confirmar JS Alert."
    logging.info(f"[JS Alert] Confirmado com accept(). Resultado na tela: '{resultado_el.text}'")
    pausa_didatica(1.0)

    # --- 2. JS Confirm ---
    btn_confirm = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//ul/li/button[normalize-space()='Click for JS Confirm']"))
    )
    btn_confirm.click()

    alerta_2 = wait.until(EC.alert_is_present())
    logging.info(f"[JS Confirm] Texto capturado: '{alerta_2.text}'. Cancelando com dismiss()...")
    pausa_didatica(1.5)
    alerta_2.dismiss()

    wait.until(EC.text_to_be_present_in_element((By.ID, "result"), "You clicked: Cancel"))
    texto_resultado_confirm = driver.find_element(By.ID, "result").text
    assert texto_resultado_confirm == "You clicked: Cancel", (
        f"Esperado 'You clicked: Cancel', obteve '{texto_resultado_confirm}'."
    )
    logging.info(f"[JS Confirm] Validação concluída! Resultado: '{texto_resultado_confirm}'")
    pausa_didatica(1.0)

    # --- 3. JS Prompt ---
    btn_prompt = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//ul/li/button[normalize-space()='Click for JS Prompt']"))
    )
    btn_prompt.click()

    alerta_3 = wait.until(EC.alert_is_present())
    logging.info(f"[JS Prompt] Enviando RA '{ra}' ao prompt e confirmando...")
    alerta_3.send_keys(ra)
    pausa_didatica(1.5)
    alerta_3.accept()

    wait.until(EC.text_to_be_present_in_element((By.ID, "result"), ra))
    texto_resultado_prompt = driver.find_element(By.ID, "result").text
    assert ra in texto_resultado_prompt, (
        f"O RA '{ra}' não foi encontrado no resultado '{texto_resultado_prompt}'."
    )
    logging.info(f"[JS Prompt] Validação concluída! Resultado: '{texto_resultado_prompt}'\n")
    pausa_didatica()


# ==============================================================================
# PARTE 3: IFRAMES (EDITOR RICO)
# ==============================================================================
def parte_3_iframes(driver: webdriver.Firefox, ra: str) -> None:
    logging.info("=== INICIANDO PARTE 3: IFRAMES ===")
    driver.get("https://the-internet.herokuapp.com/iframe")
    wait = WebDriverWait(driver, TIMEOUT_ESPERA_EXPLICITA)
    aguardar_documento_pronto(driver, wait)

    # Fecha o banner de aviso do TinyMCE caso apareça (tempo maior de 8s para carregar o script do editor)
    try:
        btn_fechar_aviso = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.tox-notification button.tox-notification__dismiss"))
        )
        btn_fechar_aviso.click()
        logging.info("Banner de aviso do TinyMCE fechado.")
    except TimeoutException:
        pass

    # 1. Trocar foco para o iframe usando CSS Selector (proibido usar #mce_0_ifr)
    seletor_css_iframe = "div.tox-edit-area > iframe.tox-edit-area__iframe"
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, seletor_css_iframe)))
    logging.info(f"Foco alterado para o iframe via CSS Selector: '{seletor_css_iframe}'")

    # 2. Localizar o corpo do editor dentro do iframe e aguardar que o texto inicial carregue
    corpo_editor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body#tinymce")))

    # Desbloqueia o editor caso a chave gratuita do TinyMCE no Herokuapp esteja em modo ReadOnly
    if corpo_editor.get_attribute("contenteditable") == "false":
        logging.warning("Editor TinyMCE estava bloqueado (contenteditable=false). Desbloqueando para edição...")
        driver.execute_script("arguments[0].setAttribute('contenteditable', 'true');", corpo_editor)

    mensagem = f"Automação RPA concluída com sucesso! RA: {ra}"
    corpo_editor.clear()
    corpo_editor.send_keys(mensagem)
    pausa_didatica()

    # Valida se o texto realmente foi inserido dentro do iframe
    texto_no_editor = corpo_editor.text
    assert ra in texto_no_editor, f"O texto no editor ('{texto_no_editor}') não contém o RA '{ra}'."
    logging.info(f"Texto inserido e validado dentro do iframe: '{texto_no_editor}'")

    # 3. Retornar ao documento principal (DOM raiz)
    driver.switch_to.default_content()
    logging.info("Contexto retornado para o DOM principal (default_content).")

    # 4. Ler o cabeçalho <h3> e validar com assert que saímos do iframe
    cabecalho_h3 = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
    texto_h3 = cabecalho_h3.text
    texto_esperado = "An iFrame containing the TinyMCE WYSIWYG Editor"
    assert texto_h3 == texto_esperado, (
        f"Falha ao validar saída do iframe. Esperado '{texto_esperado}', obteve '{texto_h3}'."
    )
    logging.info(f"Cabeçalho <h3> lido na raiz com sucesso: '{texto_h3}'\n")
    pausa_didatica()


# ==============================================================================
# PARTE 4: TROCA DE ABAS / JANELAS
# ==============================================================================
def parte_4_janelas(driver: webdriver.Firefox) -> None:
    logging.info("=== INICIANDO PARTE 4: TROCA DE ABAS / JANELAS ===")
    driver.get("https://the-internet.herokuapp.com/windows")
    wait = WebDriverWait(driver, TIMEOUT_ESPERA_EXPLICITA)
    aguardar_documento_pronto(driver, wait)

    # 1. Guardar o handle e o título da aba original
    handle_original = driver.current_window_handle
    titulo_original = driver.title
    logging.info(f"Aba original registrada -> Handle: {handle_original} | Título: '{titulo_original}'")

    # 2. Clicar no link "Click Here"
    link_nova_aba = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
    link_nova_aba.click()
    logging.info("Clique realizado em 'Click Here'.")

    # 3. Esperar até existirem 2 handles
    wait.until(EC.number_of_windows_to_be(2))
    todos_handles = driver.window_handles
    assert len(todos_handles) == 2, "Deveriam existir exatamente 2 abas abertas."

    # 4. Trocar o foco para a nova aba (o handle diferente do original)
    novo_handle = [h for h in todos_handles if h != handle_original][0]
    driver.switch_to.window(novo_handle)
    aguardar_documento_pronto(driver, wait)
    logging.info(f"Foco trocado para a nova aba -> Handle: {novo_handle}")

    # Validar com assert que o texto exibido na nova aba é "New Window"
    h3_nova_aba = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
    texto_nova_aba = h3_nova_aba.text
    assert texto_nova_aba == "New Window", (
        f"Esperado 'New Window' na nova aba, mas obteve '{texto_nova_aba}'."
    )
    logging.info(f"Validação na nova aba concluída! Texto encontrado: '{texto_nova_aba}'")
    pausa_didatica()

    # 5. Fechar a nova aba e retornar o foco para a aba original
    driver.close()
    logging.info("Nova aba fechada com driver.close().")
    driver.switch_to.window(handle_original)
    logging.info("Foco retornado para a aba original.")

    # 6. Validar que só resta 1 handle e que o título voltou ao original
    wait.until(EC.number_of_windows_to_be(1))
    assert len(driver.window_handles) == 1, "Deveria restar apenas 1 aba aberta."
    assert driver.title == titulo_original, (
        f"Título esperado '{titulo_original}', mas o atual é '{driver.title}'."
    )
    logging.info(
        f"Validação final da Parte 4 concluída! Handles ativos: {len(driver.window_handles)} | "
        f"Título atual: '{driver.title}'\n"
    )
    pausa_didatica()


# ==============================================================================
# BÔNUS: FUNÇÃO GENÉRICA PARA MÚLTIPLAS JANELAS (2 OU MAIS)
# ==============================================================================
def processar_multiplas_abas_novas(
    driver: webdriver.Firefox,
    handle_original: str,
    lista_handles: list[str]
) -> list[str]:
    wait = WebDriverWait(driver, TIMEOUT_ESPERA_EXPLICITA)
    conteudos_lidos = []
    abas_novas = [h for h in lista_handles if h != handle_original]

    logging.info(f"[BÔNUS] Processando {len(abas_novas)} novas abas abertas...")

    for indice, handle in enumerate(abas_novas, start=1):
        driver.switch_to.window(handle)
        aguardar_documento_pronto(driver, wait)
        elemento_h3 = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
        texto = elemento_h3.text
        conteudos_lidos.append(texto)

        logging.info(
            f"[BÔNUS] Aba nova #{indice} (Handle: {handle}) -> Conteúdo lido: '{texto}'. Fechando..."
        )
        assert texto == "New Window", f"Conteúdo inesperado na aba #{indice}: '{texto}'"
        pausa_didatica(1.5)
        driver.close()

    # Retorna de forma segura à aba original
    driver.switch_to.window(handle_original)
    wait.until(EC.number_of_windows_to_be(1))
    logging.info(f"[BÔNUS] Retorno seguro à aba original ({handle_original}) concluído.")
    return conteudos_lidos


def parte_bonus_multiplas_janelas(driver: webdriver.Firefox, qtd_novas_abas: int = 3) -> None:
    logging.info(f"=== INICIANDO BÔNUS: MÚLTIPLAS JANELAS ({qtd_novas_abas} NOVAS ABAS) ===")
    driver.get("https://the-internet.herokuapp.com/windows")
    wait = WebDriverWait(driver, TIMEOUT_ESPERA_EXPLICITA)
    aguardar_documento_pronto(driver, wait)

    handle_original = driver.current_window_handle
    titulo_original = driver.title
    link_nova_aba = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))

    for i in range(1, qtd_novas_abas + 1):
        link_nova_aba.click()
        wait.until(EC.number_of_windows_to_be(1 + i))
        logging.info(f"[BÔNUS] Disparo #{i}: total de {len(driver.window_handles)} abas abertas.")
        pausa_didatica(1.0)

    todos_os_handles = driver.window_handles
    assert len(todos_os_handles) == 1 + qtd_novas_abas, "Quantidade incorreta de abas abertas."

    textos_capturados = processar_multiplas_abas_novas(driver, handle_original, todos_os_handles)

    assert len(textos_capturados) == qtd_novas_abas, "Nem todas as abas novas foram lidas."
    assert len(driver.window_handles) == 1, "Sobraram abas abertas após o processamento."
    assert driver.current_window_handle == handle_original, "O foco não está na aba original."
    assert driver.title == titulo_original, "O título da página original não confere."
    logging.info("[BÔNUS] Todas as validações de múltiplas janelas passaram com sucesso!\n")


# ==============================================================================
# BLOCO PRINCIPAL (TRY / EXCEPT / FINALLY)
# ==============================================================================
def main() -> None:
    options = Options()
    # Garante que o Firefox aguarde o carregamento completo de DOM, CSS e imagens no driver.get()
    options.page_load_strategy = "normal"

    driver = None
    try:
        logging.info("Inicializando o navegador Firefox...")
        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(TIMEOUT_CARREGAMENTO_PAGINA)
        driver.maximize_window()

        # Execução sequencial das partes
        parte_1_selects(driver)
        parte_2_alerts(driver, MEU_RA)
        parte_3_iframes(driver, MEU_RA)
        parte_4_janelas(driver)
        parte_bonus_multiplas_janelas(driver, qtd_novas_abas=3)

        logging.info("🎉 TODAS AS ETAPAS E VALIDAÇÕES FORAM CONCLUÍDAS COM SUCESSO!")

    except AssertionError as erro_validacao:
        logging.error(f"❌ Falha de validação (ASSERT): {erro_validacao}")
        raise
    except TimeoutException as erro_timeout:
        logging.error(f"⏳ Tempo esgotado aguardando elemento/condição (WebDriverWait): {erro_timeout}")
        raise
    except WebDriverException as erro_webdriver:
        logging.error(f"🌐 Erro no WebDriver/Firefox: {erro_webdriver}")
        raise
    except Exception as erro_geral:
        logging.error(f"⚠️ Erro inesperado: {erro_geral}")
        raise
    finally:
        if driver is not None:
            logging.info("Encerrando o navegador com driver.quit() no bloco finally...")
            driver.quit()
            logging.info("Sessão encerrada com segurança.")


if __name__ == "__main__":
    main()