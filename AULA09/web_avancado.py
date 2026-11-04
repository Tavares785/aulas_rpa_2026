import logging
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Garante codificação UTF-8 no terminal do Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Configuração de logging para exibir no terminal com timestamp e nível
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Defina seu RA aqui
RA_ALUNO = "6326090"
TIMEOUT = 15


def parte_1_selects(driver: webdriver.Remote) -> None:
    """
    Parte 1: Manipulação de Dropdowns (Select) com validação.
    """
    logger.info("=== Iniciando Parte 1: Selects ===")
    driver.get("https://the-internet.herokuapp.com/dropdown")

    wait = WebDriverWait(driver, TIMEOUT)
    dropdown_element = wait.until(
        EC.visibility_of_element_located((By.ID, "dropdown"))
    )
    select = Select(dropdown_element)

    # 1. Listar no terminal todas as opções disponíveis do dropdown (select.options)
    opcoes = [opcao.text for opcao in select.options]
    logger.info(f"Opções disponíveis no dropdown ({len(opcoes)}): {opcoes}")
    for idx, opcao in enumerate(select.options):
        logger.info(f"  Índice {idx}: '{opcao.text}'")
    assert len(select.options) > 2, "O dropdown deveria conter pelo menos 3 opções."

    # 2. Selecionar a "Option 2" pelo índice (não pelo texto)
    # Índice 0: "Please select an option", Índice 1: "Option 1", Índice 2: "Option 2"
    select.select_by_index(2)
    logger.info("Selecionada a opção de índice 2.")

    # 3. Validar com assert que select.first_selected_option.text == "Option 2"
    opcao_selecionada = select.first_selected_option.text
    logger.info(f"Opção atualmente selecionada: '{opcao_selecionada}'")
    assert opcao_selecionada == "Option 2", (
        f"Esperado 'Option 2', mas obteve '{opcao_selecionada}'"
    )
    logger.info("Validação da Parte 1 concluída com sucesso!\n")


def parte_2_alerts(driver: webdriver.Remote, ra: str = RA_ALUNO) -> None:
    """
    Parte 2: Manipulação dos três tipos de Alerts JS usando XPath relativo.
    """
    logger.info("=== Iniciando Parte 2: Alerts JS ===")
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    wait = WebDriverWait(driver, TIMEOUT)

    # 1. JS Alert: disparar, capturar texto e confirmar com accept()
    btn_alert = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//ul/li/button[text()='Click for JS Alert']")
        )
    )
    btn_alert.click()

    alert = wait.until(EC.alert_is_present())
    texto_alert = alert.text
    logger.info(f"[JS Alert] Texto capturado: '{texto_alert}'")
    assert texto_alert == "I am a JS Alert", (
        f"Texto inesperado no JS Alert: '{texto_alert}'"
    )
    alert.accept()

    resultado_alert = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#result"))
    ).text
    logger.info(f"[JS Alert] Resultado na página: '{resultado_alert}'")
    assert resultado_alert == "You successfully clicked an alert", (
        f"Resultado inesperado após aceitar JS Alert: '{resultado_alert}'"
    )

    # 2. JS Confirm: disparar, cancelar com dismiss() e validar #result
    btn_confirm = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//ul/li/button[text()='Click for JS Confirm']")
        )
    )
    btn_confirm.click()

    confirm = wait.until(EC.alert_is_present())
    texto_confirm = confirm.text
    logger.info(f"[JS Confirm] Texto capturado: '{texto_confirm}'")
    confirm.dismiss()

    resultado_confirm = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#result"))
    ).text
    logger.info(f"[JS Confirm] Resultado na página: '{resultado_confirm}'")
    assert resultado_confirm == "You clicked: Cancel", (
        f"Esperado 'You clicked: Cancel', mas obteve '{resultado_confirm}'"
    )

    # 3. JS Prompt: disparar, enviar RA, confirmar com accept() e validar #result
    btn_prompt = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//ul/li/button[text()='Click for JS Prompt']")
        )
    )
    btn_prompt.click()

    prompt = wait.until(EC.alert_is_present())
    logger.info(f"[JS Prompt] Texto capturado: '{prompt.text}'. Enviando RA: {ra}")
    prompt.send_keys(ra)
    prompt.accept()

    resultado_prompt = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#result"))
    ).text
    logger.info(f"[JS Prompt] Resultado na página: '{resultado_prompt}'")
    assert ra in resultado_prompt, (
        f"Esperado que o RA '{ra}' estivesse em '{resultado_prompt}'"
    )
    logger.info("Validação da Parte 2 concluída com sucesso!\n")


def parte_3_iframes(driver: webdriver.Remote, ra: str = RA_ALUNO) -> None:
    """
    Parte 3: Troca de contexto para Iframe (editor rico TinyMCE) e retorno ao DOM raiz.
    """
    logger.info("=== Iniciando Parte 3: Iframes ===")
    driver.get("https://the-internet.herokuapp.com/iframe")
    wait = WebDriverWait(driver, TIMEOUT)

    # Localizar o iframe por CSS Selector (sem usar o ID fixo mce_0_ifr) e trocar o foco
    wait.until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe.tox-edit-area__iframe")
        )
    )
    logger.info("Foco alterado para dentro do iframe do editor.")

    corpo_editor = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "body#tinymce"))
    )

    # Caso o TinyMCE de demonstração do Herokuapp esteja bloqueado em modo read-only
    # (devido à expiração da chave gratuita do site de testes), desbloqueamos o modo design
    # para que os comandos nativos clear() e send_keys() do Selenium funcionem normalmente.
    driver.execute_script(
        """
        if (window.parent && window.parent.tinymce && window.parent.tinymce.activeEditor) {
            window.parent.tinymce.activeEditor.mode.set('design');
        }
        arguments[0].setAttribute('contenteditable', 'true');
        """,
        corpo_editor,
    )

    mensagem = f"Automação Web concluída pelo RA: {ra}"
    corpo_editor.clear()
    corpo_editor.click()
    corpo_editor.send_keys(mensagem)

    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "body#tinymce"), ra))
    texto_editor = corpo_editor.text
    logger.info(f"Texto inserido no iframe: '{texto_editor}'")
    assert ra in texto_editor, (
        f"O texto do editor deveria conter o RA '{ra}', mas contém '{texto_editor}'"
    )

    # Retornar ao documento principal (DOM raiz)
    driver.switch_to.default_content()
    logger.info("Foco retornado ao documento principal (default_content).")

    # Ler o cabeçalho <h3> da página para confirmar que saiu do iframe
    cabecalho_h3 = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.example h3"))
    ).text
    logger.info(f"Cabeçalho <h3> lido no DOM raiz: '{cabecalho_h3}'")
    assert "An iFrame containing the TinyMCE WYSIWYG Editor" in cabecalho_h3, (
        f"Cabeçalho <h3> inesperado: '{cabecalho_h3}'"
    )
    logger.info("Validação da Parte 3 concluída com sucesso!\n")


def processar_novas_janelas(
    driver: webdriver.Remote, handle_original: str, lista_handles: list[str]
) -> list[str]:
    """
    Função genérica (Bônus): Recebe a lista de handles, percorre todas as abas novas,
    lê e valida o conteúdo de cada uma e fecha-as, retornando sempre à aba original de forma segura.
    """
    conteudos_lidos: list[str] = []
    abas_novas = [h for h in lista_handles if h != handle_original]
    logger.info(
        f"Processando {len(abas_novas)} nova(s) janela(s)/aba(s): {abas_novas}"
    )

    try:
        for idx, handle in enumerate(abas_novas, start=1):
            driver.switch_to.window(handle)
            wait = WebDriverWait(driver, TIMEOUT)
            texto_aba = wait.until(
                EC.visibility_of_element_located((By.TAG_NAME, "h3"))
            ).text
            logger.info(
                f"  [Aba Nova #{idx} | Handle: {handle}] Conteúdo lido: '{texto_aba}'"
            )
            assert texto_aba == "New Window", (
                f"Esperado 'New Window', mas obteve '{texto_aba}'"
            )
            conteudos_lidos.append(texto_aba)

            driver.close()
            logger.info(f"  [Aba Nova #{idx} | Handle: {handle}] Fechada com sucesso.")
    finally:
        # Garante retorno seguro à aba original mesmo em caso de erro
        driver.switch_to.window(handle_original)
        logger.info(f"Foco retornado com segurança para a aba original: {handle_original}")

    return conteudos_lidos


def parte_4_windows(driver: webdriver.Remote) -> None:
    """
    Parte 4: Controle de múltiplas abas/janelas com window_handles e switch_to.window,
    incluindo o desafio Bônus para múltiplas janelas.
    """
    logger.info("=== Iniciando Parte 4: Troca de Abas / Janelas ===")
    driver.get("https://the-internet.herokuapp.com/windows")
    wait = WebDriverWait(driver, TIMEOUT)

    # 1. Guardar o handle da aba original
    handle_original = driver.current_window_handle
    titulo_original = driver.title
    logger.info(
        f"Handle da aba original: {handle_original} | Título: '{titulo_original}'"
    )

    # 2. Clicar no link "Click Here", que abre uma nova aba
    link_nova_aba = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
    )
    link_nova_aba.click()
    logger.info("Clicou em 'Click Here' para abrir nova aba.")

    # 3. Usando WebDriverWait, esperar até existirem 2 handles
    wait.until(EC.number_of_windows_to_be(2))
    logger.info(f"Total de abas abertas: {len(driver.window_handles)}")
    assert len(driver.window_handles) == 2, "Deveriam existir exatamente 2 abas abertas."

    # 4 e 5. Trocar foco para a nova aba, validar texto "New Window", fechar e voltar à original
    conteudos = processar_novas_janelas(
        driver, handle_original, driver.window_handles
    )
    assert conteudos == ["New Window"], "O conteúdo da nova aba deveria ser 'New Window'."

    # 6. Validar com assert que, ao final, só existe 1 handle e que o título voltou ao original
    wait.until(EC.number_of_windows_to_be(1))
    assert len(driver.window_handles) == 1, (
        f"Esperado apenas 1 handle aberto, mas existem {len(driver.window_handles)}"
    )
    assert driver.current_window_handle == handle_original, (
        "O foco atual não está no handle original."
    )
    assert driver.title == titulo_original, (
        f"Título esperado '{titulo_original}', mas obteve '{driver.title}'"
    )
    cabecalho_original = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    ).text
    assert cabecalho_original == "Opening a new window", (
        f"Cabeçalho esperado 'Opening a new window', mas obteve '{cabecalho_original}'"
    )
    logger.info("Validação da Parte 4 (fluxo padrão) concluída com sucesso!")

    # --- Execução do Cenário Bônus (2 ou mais novas janelas abertas simultaneamente) ---
    logger.info("--- Iniciando Cenário Bônus: Múltiplas Janelas Simultâneas ---")
    qtd_novas_janelas = 3
    for i in range(qtd_novas_janelas):
        link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
        link.click()
        wait.until(EC.number_of_windows_to_be(i + 2))

    total_esperado = 1 + qtd_novas_janelas
    logger.info(
        f"Cenário Bônus: {len(driver.window_handles)} janelas abertas no total."
    )
    assert len(driver.window_handles) == total_esperado

    conteudos_bonus = processar_novas_janelas(
        driver, handle_original, driver.window_handles
    )
    assert len(conteudos_bonus) == qtd_novas_janelas
    assert all(c == "New Window" for c in conteudos_bonus)
    assert len(driver.window_handles) == 1
    assert driver.title == titulo_original
    logger.info("Validação do Cenário Bônus concluída com sucesso!\n")


def main() -> None:
    driver = None
    try:
        logger.info("Inicializando o WebDriver Microsoft Edge...")
        options = webdriver.EdgeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Edge(options=options)

        parte_1_selects(driver)
        parte_2_alerts(driver, ra=RA_ALUNO)
        parte_3_iframes(driver, ra=RA_ALUNO)
        parte_4_windows(driver)

        logger.info("🎉 Todos os desafios do Lab 09 foram executados e validados com sucesso!")
    except AssertionError as err:
        logger.error(f"Falha de validação (AssertionError): {err}")
        raise
    except Exception as exc:
        logger.error(f"Erro inesperado durante a execução: {exc}")
        raise
    finally:
        if driver is not None:
            logger.info("Encerrando o WebDriver (driver.quit())...")
            driver.quit()


if __name__ == "__main__":
    main()

