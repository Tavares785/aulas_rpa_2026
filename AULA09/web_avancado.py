
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==========================================
# CONFIGURACOES
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)

TEMPO_ESPERA = 15

URL_DROPDOWN = "https://the-internet.herokuapp.com/dropdown"
URL_ALERTS = "https://the-internet.herokuapp.com/javascript_alerts"
URL_IFRAME = "https://the-internet.herokuapp.com/iframe"
URL_WINDOWS = "https://the-internet.herokuapp.com/windows"


# ==========================================
# PARTE 1 - SELECTS
# ==========================================

def parte_1_selects(driver):

    logging.info("INICIANDO PARTE 1 - SELECTS")

    driver.get(URL_DROPDOWN)

    espera = WebDriverWait(driver, TEMPO_ESPERA)

    elemento = espera.until(
        EC.presence_of_element_located(
            (By.ID, "dropdown")
        )
    )

    selecao = Select(elemento)

    # Listar todas as opcoes
    logging.info("Opcoes disponiveis:")

    for opcao in selecao.options:
        logging.info(opcao.text)

    # Selecionar Option 2 pelo indice
    selecao.select_by_index(2)

    # Validar selecao
    selecionada = selecao.first_selected_option.text

    assert selecionada == "Option 2", (
        "Erro: Option 2 nao foi selecionada!"
    )

    logging.info(
        "Validacao concluida: %s selecionada.",
        selecionada
    )


# ==========================================
# PARTE 2 - ALERTS JAVASCRIPT
# ==========================================

def parte_2_alerts(driver, ra):

    logging.info("INICIANDO PARTE 2 - ALERTS")

    driver.get(URL_ALERTS)

    espera = WebDriverWait(driver, TEMPO_ESPERA)

    # Localizar a lista de botoes
    lista_botoes = driver.find_element(
        By.XPATH,
        "//ul"
    )

    # Localizar os botoes usando XPath relativo
    botao_alert = lista_botoes.find_element(
        By.XPATH,
        ".//button[normalize-space()='Click for JS Alert']"
    )

    botao_confirm = lista_botoes.find_element(
        By.XPATH,
        ".//button[normalize-space()='Click for JS Confirm']"
    )

    botao_prompt = lista_botoes.find_element(
        By.XPATH,
        ".//button[normalize-space()='Click for JS Prompt']"
    )

    # 1 - JS ALERT
    botao_alert.click()

    alerta = espera.until(
        EC.alert_is_present()
    )

    texto_alerta = alerta.text

    logging.info("Texto do JS Alert: %s", texto_alerta)

    assert texto_alerta != "", "Alerta sem texto!"

    alerta.accept()

    logging.info("JS Alert aceito com sucesso.")

    # 2 - JS CONFIRM
    botao_confirm.click()

    alerta = espera.until(
        EC.alert_is_present()
    )

    logging.info("Texto do JS Confirm: %s", alerta.text)

    alerta.dismiss()

    resultado = espera.until(
        EC.visibility_of_element_located(
            (By.ID, "result")
        )
    )

    texto_resultado = resultado.text

    assert "You clicked: Cancel" in texto_resultado, (
        "Erro: O JS Confirm nao foi cancelado!"
    )

    logging.info(
        "JS Confirm cancelado: %s",
        texto_resultado
    )

    # 3 - JS PROMPT
    botao_prompt.click()

    alerta = espera.until(
        EC.alert_is_present()
    )

    logging.info("Enviando RA: %s", ra)

    alerta.send_keys(ra)

    alerta.accept()

    resultado = espera.until(
        EC.visibility_of_element_located(
            (By.ID, "result")
        )
    )

    texto_resultado = resultado.text

    assert ra in texto_resultado, (
        "Erro: O RA nao apareceu no resultado!"
    )

    logging.info(
        "JS Prompt validado. RA informado: %s",
        ra
    )

    logging.info("PARTE 2 CONCLUIDA COM SUCESSO.")


# ==========================================
# PARTE 3 - IFRAMES
# ==========================================

def parte_3_iframes(driver, ra):

    logging.info("INICIANDO PARTE 3 - IFRAMES")

    driver.get(URL_IFRAME)

    espera = WebDriverWait(driver, TEMPO_ESPERA)

    try:

        # Localizar iframe pelo CSS Selector
        espera.until(
            EC.frame_to_be_available_and_switch_to_it(
                (
                    By.CSS_SELECTOR,
                    "iframe.tox-edit-area__iframe"
                )
            )
        )

        logging.info("Entrou no iframe.")

        # Localizar o editor
        editor = espera.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        # Limpar o texto existente
        editor.click()
        editor.send_keys(Keys.CONTROL, "a")
        editor.send_keys(Keys.BACKSPACE)

        # Escrever mensagem com RA
        mensagem = (
            f"Automacao RPA - Laboratorio 09 - RA: {ra}"
        )

        editor.send_keys(mensagem)

        assert ra in editor.text, (
            "Erro: RA nao foi escrito no editor!"
        )

        logging.info(
            "Mensagem escrita no iframe: %s",
            mensagem
        )

    finally:

        # Voltar ao documento principal
        driver.switch_to.default_content()

        logging.info("Retornou ao documento principal.")

    # Validar o cabecalho fora do iframe
    cabecalho = espera.until(
        EC.visibility_of_element_located(
            (By.TAG_NAME, "h3")
        )
    )

    texto_cabecalho = cabecalho.text

    assert (
        texto_cabecalho
        == "An iFrame containing the TinyMCE WYSIWYG Editor"
    ), "Erro: Nao retornou ao documento principal!"

    logging.info(
        "Iframe validado. Cabecalho: %s",
        texto_cabecalho
    )


# ==========================================
# PARTE 4 - TROCA DE ABAS E JANELAS
# ==========================================

def parte_4_janelas(driver):

    logging.info("INICIANDO PARTE 4 - JANELAS")

    driver.get(URL_WINDOWS)

    espera = WebDriverWait(driver, TEMPO_ESPERA)

    # Guardar aba original
    handle_original = driver.current_window_handle

    titulo_original = driver.title

    assert len(driver.window_handles) == 1

    logging.info("Aba original identificada.")

    try:

        # Clicar no link Click Here
        link = espera.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[normalize-space()='Click Here']"
                )
            )
        )

        link.click()

        # Esperar duas janelas
        espera.until(
            EC.number_of_windows_to_be(2)
        )

        logging.info("Nova aba aberta.")

        # Identificar e acessar a nova aba
        handles = driver.window_handles

        handle_novo = next(
            handle
            for handle in handles
            if handle != handle_original
        )

        driver.switch_to.window(handle_novo)

        # Validar texto da nova aba
        novo_texto = espera.until(
            EC.visibility_of_element_located(
                (By.TAG_NAME, "h3")
            )
        ).text

        assert novo_texto == "New Window", (
            "Erro: Texto da nova janela incorreto!"
        )

        logging.info(
            "Nova aba validada: %s",
            novo_texto
        )

        # Fechar nova aba
        driver.close()

        logging.info("Nova aba fechada.")

    finally:

        # Garantir retorno a aba original
        if handle_original in driver.window_handles:

            # Fechar eventual aba extra, caso ainda exista
            for handle in driver.window_handles:

                if handle != handle_original:

                    driver.switch_to.window(handle)
                    driver.close()

            driver.switch_to.window(handle_original)

    # Validar retorno
    assert len(driver.window_handles) == 1, (
        "Erro: Ainda existem outras abas abertas!"
    )

    assert driver.title == titulo_original, (
        "Erro: O titulo da aba original mudou!"
    )

    logging.info("Retornou a aba original.")

    logging.info(
        "PARTE 4 CONCLUIDA COM SUCESSO."
    )


# ==========================================
# BONUS - MULTIPLAS JANELAS
# ==========================================

def parte_5_multiplas_janelas(
    driver,
    handles_novos,
    handle_original
):

    logging.info("INICIANDO BONUS - MULTIPLAS JANELAS")

    try:

        for handle in handles_novos:

            if handle == handle_original:
                continue

            if handle not in driver.window_handles:
                continue

            try:

                # Entrar na nova janela
                driver.switch_to.window(handle)

                # Ler o conteudo
                titulo = driver.title

                conteudo = driver.find_element(
                    By.TAG_NAME,
                    "body"
                ).text

                logging.info("Titulo da janela: %s", titulo)

                logging.info(
                    "Conteudo da janela: %s",
                    conteudo
                )

                assert conteudo.strip() != "", (
                    "Janela sem conteudo!"
                )

            finally:

                # Fechar a janela visitada
                if handle in driver.window_handles:

                    driver.close()

                    logging.info(
                        "Janela fechada: %s",
                        handle
                    )

    finally:

        # Retornar a aba original
        if handle_original in driver.window_handles:

            driver.switch_to.window(handle_original)

    assert driver.current_window_handle == handle_original

    logging.info(
        "BONUS CONCLUIDO. Aba original restaurada."
    )


# ==========================================
# EXECUCAO PRINCIPAL
# ==========================================

def main():

    driver = None

    # Solicitar RA ao usuario
    ra = input("Digite seu RA: ").strip()

    if not ra:
        logging.error("RA nao informado. Encerrando.")
        return

    try:

        logging.info("Iniciando automacao Selenium.")

        # Abrir Chrome
        driver = webdriver.Chrome()

        driver.maximize_window()

        # Executar as quatro partes obrigatorias
        parte_1_selects(driver)

        parte_2_alerts(driver, ra)

        parte_3_iframes(driver, ra)

        parte_4_janelas(driver)

        logging.info(
            "TODAS AS PARTES OBRIGATORIAS FORAM CONCLUIDAS!"
        )

    except Exception:

        logging.exception(
            "ERRO DURANTE A EXECUCAO DO LABORATORIO."
        )

        raise

    finally:

        # Fechar navegador mesmo se ocorrer erro
        if driver is not None:

            driver.quit()

            logging.info("Navegador encerrado.")

    logging.info("FIM DO LABORATORIO 09.")


# ==========================================
# INICIO DO PROGRAMA
# ==========================================

if __name__ == "__main__":
    main()
