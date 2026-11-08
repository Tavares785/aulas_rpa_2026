#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_avancado.py - Desafio de Automação Web Avançada com Selenium WebDriver.

Regras e Boas Práticas Atendidas:
1. Sincronização exclusiva via WebDriverWait com expected_conditions
   (proibido time.sleep).
2. Encapsulamento de cada etapa em sua própria função modular.
3. Validação com assert e rastreamento completo via módulo logging.
4. Bloco try/except/finally garantindo driver.quit() no encerramento.
5. Localização de botões JS Alerts exclusivamente por XPath relativo
   (sem IDs prontos).
6. Localização do iframe do editor exclusivamente por CSS Selector
   (sem ID fixo).
7. Gerenciamento seguro de abas/janelas com espera explícita por número
   de handles.
8. Bônus implementado: função genérica para leitura e fechamento de
   múltiplas abas secundárias.
"""

import argparse
import logging
import sys
from typing import List

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# ---------------------------------------------------------------------------
# Configuração de Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("WebAvancado")


# ---------------------------------------------------------------------------
# Inicialização do WebDriver
# ---------------------------------------------------------------------------
def criar_driver(headless: bool = True) -> WebDriver:
    """
    Configura e inicializa uma instância do Chrome WebDriver.

    Args:
        headless: Se True, executa o navegador em modo headless
                  (sem interface gráfica).

    Returns:
        WebDriver: Instância configurada do Chrome.
    """
    logger.info("Inicializando Chrome WebDriver (headless=%s)...", headless)
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    logger.info("Navegador inicializado com sucesso.")
    return driver


# ---------------------------------------------------------------------------
# Parte 1: Selects — com validação
# ---------------------------------------------------------------------------
def parte_1_selects(driver: WebDriver, timeout: int = 10) -> None:
    """
    Acessa a página de dropdown, lista as opções disponíveis no dropdown,
    seleciona a 'Option 2' pelo seu índice numérico e valida a seleção
    com assert.

    Args:
        driver: Instância do WebDriver em execução.
        timeout: Tempo máximo de espera explícita em segundos.
    """
    url = "https://the-internet.herokuapp.com/dropdown"
    logger.info("=== [Parte 1] Iniciando teste de Dropdown / Selects ===")
    logger.info("Navegando para: %s", url)
    driver.get(url)

    wait = WebDriverWait(driver, timeout)

    # 1. Aguarda o elemento select estar presente e visível
    dropdown_element = wait.until(
        EC.visibility_of_element_located((By.ID, "dropdown"))
    )
    select = Select(dropdown_element)

    # 2. Lista todas as opções disponíveis no terminal e log
    options = select.options
    logger.info("Total de opções encontradas no dropdown: %d", len(options))
    for idx, opt in enumerate(options):
        logger.info(
            "Opção [%d] -> Texto: '%s' | Valor: '%s' | Habilitada: %s",
            idx,
            opt.text,
            opt.get_attribute("value"),
            opt.is_enabled()
        )

    # 3. Seleciona a "Option 2" pelo índice (índice 2 na lista de opções)
    # Índice 0: "Please select an option" (desabilitado)
    # Índice 1: "Option 1"
    # Índice 2: "Option 2"
    indice_alvo = 2
    logger.info("Selecionando opção pelo índice numérico: %d...", indice_alvo)
    select.select_by_index(indice_alvo)

    # 4. Validação com assert
    opcao_selecionada = select.first_selected_option.text
    logger.info("Opção atualmente selecionada: '%s'", opcao_selecionada)
    assert opcao_selecionada == "Option 2", (
        f"Falha na validação do Select: esperado 'Option 2', "
        f"mas obtido '{opcao_selecionada}'"
    )
    logger.info(
        "[Parte 1] Validação concluída com sucesso! Opção 2 confirmada."
    )


# ---------------------------------------------------------------------------
# Parte 2: Alerts JS — os três tipos
# ---------------------------------------------------------------------------
def parte_2_alerts(
    driver: WebDriver,
    ra: str = "RA12345678",
    timeout: int = 10
) -> None:
    """
    Acessa a página de alertas JavaScript e testa os 3 tipos:
    1. JS Alert: dispara, captura o texto e aceita com accept().
    2. JS Confirm: dispara, cancela com dismiss() e valida no #result.
    3. JS Prompt: dispara, envia o RA via send_keys(), aceita e valida.

    Regra: Botões localizados EXCLUSIVAMENTE por XPath relativo, sem IDs.

    Args:
        driver: Instância do WebDriver.
        ra: Registro Acadêmico a ser digitado no prompt.
        timeout: Tempo máximo de espera explícita em segundos.
    """
    url = "https://the-internet.herokuapp.com/javascript_alerts"
    logger.info("=== [Parte 2] Iniciando teste de Alertas JavaScript ===")
    logger.info("Navegando para: %s", url)
    driver.get(url)

    wait = WebDriverWait(driver, timeout)

    # -----------------------------------------------------------------------
    # 2.1 JS Alert
    # -----------------------------------------------------------------------
    logger.info("2.1 - Testando JS Alert...")
    # XPath relativo buscando pelo texto visível do botão
    xpath_btn_alert = "//ul/li/button[contains(text(), 'Click for JS Alert')]"
    btn_alert = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpath_btn_alert))
    )
    btn_alert.click()
    logger.info("Botão 'Click for JS Alert' clicado.")

    # Espera explícita pelo surgimento do alert
    alert = wait.until(EC.alert_is_present())
    texto_alert = alert.text
    logger.info("Texto capturado do JS Alert: '%s'", texto_alert)
    assert "JS Alert" in texto_alert, (
        f"Texto inesperado no JS Alert: '{texto_alert}'"
    )

    alert.accept()
    logger.info("JS Alert confirmado via accept().")

    # Valida resultado na página
    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "result"), "You successfully clicked an alert"
        )
    )
    resultado_alert = driver.find_element(By.ID, "result").text
    assert resultado_alert == "You successfully clicked an alert", (
        f"Falha no resultado do JS Alert: '{resultado_alert}'"
    )
    logger.info("Resultado do JS Alert validado: '%s'", resultado_alert)

    # -----------------------------------------------------------------------
    # 2.2 JS Confirm
    # -----------------------------------------------------------------------
    logger.info("2.2 - Testando JS Confirm...")
    # XPath relativo buscando o botão de confirmação
    xpath_btn_confirm = (
        "//ul/li/button[contains(text(), 'Click for JS Confirm')]"
    )
    btn_confirm = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpath_btn_confirm))
    )
    btn_confirm.click()
    logger.info("Botão 'Click for JS Confirm' clicado.")

    confirm = wait.until(EC.alert_is_present())
    texto_confirm = confirm.text
    logger.info("Texto capturado do JS Confirm: '%s'", texto_confirm)

    # Cancela o confirm com dismiss()
    confirm.dismiss()
    logger.info("JS Confirm cancelado via dismiss().")

    # Valida com assert que o texto no #result indica "You clicked: Cancel"
    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "result"), "You clicked: Cancel"
        )
    )
    resultado_confirm = driver.find_element(By.ID, "result").text
    logger.info("Resultado lido em #result: '%s'", resultado_confirm)
    assert resultado_confirm == "You clicked: Cancel", (
        f"Falha no JS Confirm: esperado 'You clicked: Cancel', "
        f"obtido '{resultado_confirm}'"
    )
    logger.info("Validação do JS Confirm concluída com sucesso.")

    # -----------------------------------------------------------------------
    # 2.3 JS Prompt
    # -----------------------------------------------------------------------
    logger.info("2.3 - Testando JS Prompt com RA: '%s'...", ra)
    # XPath relativo buscando o botão de prompt
    xpath_btn_prompt = (
        "//ul/li/button[contains(text(), 'Click for JS Prompt')]"
    )
    btn_prompt = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpath_btn_prompt))
    )
    btn_prompt.click()
    logger.info("Botão 'Click for JS Prompt' clicado.")

    prompt = wait.until(EC.alert_is_present())
    texto_prompt = prompt.text
    logger.info("Texto capturado do JS Prompt: '%s'", texto_prompt)

    # Envia o RA e confirma
    prompt.send_keys(ra)
    logger.info("Texto '%s' enviado ao prompt.", ra)
    prompt.accept()
    logger.info("JS Prompt aceito via accept().")

    # Valida com assert que o #result contém o RA digitado
    wait.until(EC.text_to_be_present_in_element((By.ID, "result"), ra))
    resultado_prompt = driver.find_element(By.ID, "result").text
    logger.info("Resultado lido em #result: '%s'", resultado_prompt)
    assert ra in resultado_prompt, (
        f"Falha no JS Prompt: RA '{ra}' não encontrado "
        f"no resultado '{resultado_prompt}'"
    )
    logger.info(
        "[Parte 2] Todos os 3 tipos de alertas JS validados com sucesso!"
    )


# ---------------------------------------------------------------------------
# Parte 3: Iframes — editor rico
# ---------------------------------------------------------------------------
def parte_3_iframes(
    driver: WebDriver,
    ra: str = "RA12345678",
    timeout: int = 10
) -> None:
    """
    Acessa a página com editor rico TinyMCE dentro de um iframe.
    - Localiza o iframe por CSS Selector (sem usar ID fixo mce_0_ifr).
    - Troca o foco para o iframe.
    - Limpa o conteúdo padrão e escreve uma mensagem contendo o RA.
    - Retorna ao documento principal (default_content()).
    - Valida a saída do iframe lendo o cabeçalho <h3> do DOM raiz com assert.

    Args:
        driver: Instância do WebDriver.
        ra: Registro Acadêmico a ser incluído no editor.
        timeout: Tempo máximo de espera explícita em segundos.
    """
    url = "https://the-internet.herokuapp.com/iframe"
    logger.info("=== [Parte 3] Iniciando teste de Iframes (TinyMCE) ===")
    logger.info("Navegando para: %s", url)
    driver.get(url)

    wait = WebDriverWait(driver, timeout)

    # 1. Localiza o iframe por CSS Selector relativo à classe e ao título
    css_iframe = "iframe.tox-edit-area__iframe, iframe[title='Rich Text Area']"
    logger.info("Aguardando iframe via CSS Selector: '%s'...", css_iframe)
    iframe_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_iframe))
    )

    # 2. Troca o foco para o iframe do editor
    driver.switch_to.frame(iframe_element)
    logger.info("Foco alternado com sucesso para o interior do iframe.")

    # 3. Aguarda o editor estar totalmente carregado e interativo
    corpo_editor = wait.until(
        EC.presence_of_element_located((By.ID, "tinymce"))
    )
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#tinymce p"))
    )

    texto_original = corpo_editor.text
    logger.info("Conteúdo inicial do editor: '%s'", texto_original)

    # 4. Limpa o conteúdo e escreve a nova mensagem contendo o RA
    corpo_editor.click()
    corpo_editor.send_keys(Keys.CONTROL + "a")
    corpo_editor.send_keys(Keys.BACKSPACE)

    nova_mensagem = f"Trabalho de Automação Web Avançada - Aluno: {ra}"
    logger.info("Digitando nova mensagem no editor: '%s'...", nova_mensagem)
    corpo_editor.send_keys(nova_mensagem)

    # Valida que o texto foi escrito dentro do editor
    assert ra in corpo_editor.text, (
        f"Falha ao validar texto no iframe: RA '{ra}' não encontrado "
        f"em '{corpo_editor.text}'"
    )
    logger.info(
        "Texto validado dentro do editor com sucesso: '%s'", corpo_editor.text
    )

    # 5. Retorna ao documento principal (DOM raiz)
    driver.switch_to.default_content()
    logger.info("Retornado ao documento principal via default_content().")

    # 6. De volta no DOM raiz, lê o <h3> para confirmar a saída do iframe
    h3_element = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )
    texto_h3 = h3_element.text
    logger.info("Cabeçalho <h3> lido no DOM raiz: '%s'", texto_h3)

    texto_esperado_h3 = "An iFrame containing the TinyMCE WYSIWYG Editor"
    assert texto_h3 == texto_esperado_h3, (
        f"Falha na validação do retorno do iframe: esperado "
        f"'{texto_esperado_h3}', obtido '{texto_h3}'"
    )
    logger.info(
        "[Parte 3] Foco no DOM raiz confirmado com sucesso pelo <h3>!"
    )


# ---------------------------------------------------------------------------
# Parte 4: Troca de Abas / Janelas (com Bônus genérico)
# ---------------------------------------------------------------------------
def parte_4_windows(driver: WebDriver, timeout: int = 10) -> None:
    """
    Acessa a página de janelas / abas:
    - Armazena o handle da aba original (driver.current_window_handle).
    - Clica no link 'Click Here' que abre uma nova aba.
    - Utiliza WebDriverWait para aguardar exatamente 2 handles.
    - Alterna o foco para a nova aba e valida via assert o texto 'New Window'.
    - Fecha a nova aba (driver.close()) e retorna à aba original.
    - Valida que resta apenas 1 handle e o título é o da página de janelas.

    Args:
        driver: Instância do WebDriver.
        timeout: Tempo máximo de espera explícita em segundos.
    """
    url = "https://the-internet.herokuapp.com/windows"
    logger.info("=== [Parte 4] Iniciando teste de Troca de Abas / Janelas ===")
    logger.info("Navegando para: %s", url)
    driver.get(url)

    wait = WebDriverWait(driver, timeout)

    # 1. Guarda o handle e o título da aba original
    handle_original = driver.current_window_handle
    titulo_original = driver.title
    logger.info(
        "Aba original identificada -> Handle: %s | Título: '%s'",
        handle_original,
        titulo_original
    )

    # 2. Localiza e clica no link "Click Here"
    link_nova_aba = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
    )
    link_nova_aba.click()
    logger.info("Link 'Click Here' clicado. Aguardando nova janela...")

    # 3. Aguarda explicitamente até existirem 2 handles
    wait.until(EC.number_of_windows_to_be(2))
    todos_handles = driver.window_handles
    logger.info(
        "Total de handles detectados: %d -> %s",
        len(todos_handles),
        todos_handles
    )
    assert len(todos_handles) == 2, (
        f"Esperado exatamente 2 handles, mas obteve {len(todos_handles)}"
    )

    # 4. Encontra o handle diferente do original e troca o foco
    handle_nova_aba = [h for h in todos_handles if h != handle_original][0]
    logger.info("Trocando foco para a nova aba: %s...", handle_nova_aba)
    driver.switch_to.window(handle_nova_aba)

    # Valida com assert que o texto exibido na nova aba é "New Window"
    elemento_h3_nova_aba = wait.until(
        EC.visibility_of_element_located((By.TAG_NAME, "h3"))
    )
    texto_nova_aba = elemento_h3_nova_aba.text
    logger.info("Texto exibido na nova aba: '%s'", texto_nova_aba)
    assert texto_nova_aba == "New Window", (
        f"Falha na nova janela: esperado 'New Window', "
        f"obtido '{texto_nova_aba}'"
    )

    # 5. Fecha a nova aba e retorna o foco para a aba original
    logger.info("Fechando a aba secundária atual...")
    driver.close()

    logger.info("Voltando foco para aba original: %s...", handle_original)
    driver.switch_to.window(handle_original)

    # 6. Valida que resta apenas 1 handle e o título é o da página original
    wait.until(EC.number_of_windows_to_be(1))
    handles_restantes = driver.window_handles
    assert len(handles_restantes) == 1, (
        f"Esperado 1 handle após fechar aba secundária, "
        f"encontrados: {len(handles_restantes)}"
    )
    assert driver.current_window_handle == handle_original, (
        "O foco não está na aba original."
    )
    assert driver.title == titulo_original, (
        f"Título atual '{driver.title}' difere do original '{titulo_original}'"
    )
    logger.info(
        "[Parte 4] Troca, validação e fechamento de aba com sucesso!"
    )


# ---------------------------------------------------------------------------
# Bônus: Função Genérica para Múltiplas Abas/Janelas
# ---------------------------------------------------------------------------
def fechar_abas_secundarias_e_retornar(
    driver: WebDriver,
    handle_original: str
) -> List[str]:
    """
    Função Genérica (Bônus):
    Recebe a instância do WebDriver e o handle da aba original.
    Percorre todas as abas novas abertas, lê o conteúdo textual relevante,
    fecha-as e garante o retorno seguro do foco à aba original.

    Args:
        driver: Instância do WebDriver.
        handle_original: Handle da aba original que não deve ser fechada.

    Returns:
        List[str]: Lista com texto lido em cada aba antes do fechamento.
    """
    logger.info("Executando fechamento genérico de janelas secundárias...")
    conteudos_lidos = []
    handles_atuais = list(driver.window_handles)

    for h in handles_atuais:
        if h != handle_original:
            logger.info("Alternando foco para a aba secundária: %s", h)
            driver.switch_to.window(h)

            # Lê o conteúdo relevante da aba
            try:
                elem_h3 = driver.find_element(By.TAG_NAME, "h3")
                conteudo = elem_h3.text
            except Exception:
                conteudo = driver.title

            logger.info("Conteúdo capturado da aba [%s]: '%s'", h, conteudo)
            conteudos_lidos.append(conteudo)

            # Fecha a aba secundária
            driver.close()
            logger.info("Aba secundária [%s] fechada.", h)

    # Retorna o foco de forma segura para a aba original
    driver.switch_to.window(handle_original)
    logger.info(
        "Foco restaurado com sucesso na aba original: %s", handle_original
    )
    return conteudos_lidos


def parte_bonus_multiplas_janelas(
    driver: WebDriver,
    timeout: int = 10
) -> None:
    """
    Demonstração prática do Bônus:
    Cenário em que múltiplos cliques ou scripts abrem duas ou mais novas abas.
    Utiliza a função genérica `fechar_abas_secundarias_e_retornar` para
    processar as novas abas, ler seus conteúdos e fechá-las com segurança.

    Args:
        driver: Instância do WebDriver.
        timeout: Tempo máximo de espera explícita.
    """
    url = "https://the-internet.herokuapp.com/windows"
    logger.info("=== [Bônus] Teste com Múltiplas Novas Janelas ===")
    driver.get(url)

    wait = WebDriverWait(driver, timeout)
    handle_original = driver.current_window_handle

    # Simula abertura de 3 novas janelas
    logger.info("Disparando abertura de 3 novas abas simultâneas...")
    url_nova = "https://the-internet.herokuapp.com/windows/new"
    driver.execute_script(f"window.open('{url_nova}', '_blank');")
    driver.execute_script(f"window.open('{url_nova}', '_blank');")
    driver.execute_script(f"window.open('{url_nova}', '_blank');")

    # Aguarda explicitamente até existirem 4 janelas abertas
    wait.until(EC.number_of_windows_to_be(4))
    assert len(driver.window_handles) == 4, "Deveriam existir 4 abas abertas."
    logger.info("4 abas abertas confirmadas.")

    # Executa a função genérica bônus
    conteudos = fechar_abas_secundarias_e_retornar(driver, handle_original)

    # Validações finais
    wait.until(EC.number_of_windows_to_be(1))
    assert len(driver.window_handles) == 1, (
        "Apenas a aba original deveria permanecer aberta."
    )
    assert driver.current_window_handle == handle_original, (
        "O foco deve estar na aba original."
    )
    assert len(conteudos) == 3, (
        f"Esperado leitura de 3 abas secundárias, lidas: {len(conteudos)}"
    )
    for c in conteudos:
        assert c == "New Window", f"Conteúdo inesperado na aba: '{c}'"

    logger.info(
        "[Bônus] Função genérica de gerenciamento de múltiplas janelas "
        "aprovada com louvor!"
    )


# ---------------------------------------------------------------------------
# Execução Principal com try / except / finally
# ---------------------------------------------------------------------------
def main() -> int:
    """
    Ponto de entrada do script com tratamento de exceções e argumentos CLI.
    Garante o encerramento seguro do driver no bloco finally.
    """
    parser = argparse.ArgumentParser(
        description="Script de Automação Web Avançada com Selenium WebDriver."
    )
    parser.add_argument(
        "--ra",
        type=str,
        default="RA12345678",
        help="Registro Acadêmico (RA) a ser utilizado nos testes"
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Executa com navegador visível (por padrão roda headless)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Tempo limite (em segundos) para esperas explícitas"
    )
    args = parser.parse_args()

    driver = None
    try:
        logger.info("Iniciando bateria completa de automação web avançada...")
        logger.info(
            "Parâmetros: RA=%s | Headless=%s | Timeout=%ds",
            args.ra,
            not args.no_headless,
            args.timeout
        )

        # Inicializa o navegador
        driver = criar_driver(headless=not args.no_headless)

        # Execução das 4 partes obrigatórias
        parte_1_selects(driver, timeout=args.timeout)
        parte_2_alerts(driver, ra=args.ra, timeout=args.timeout)
        parte_3_iframes(driver, ra=args.ra, timeout=args.timeout)
        parte_4_windows(driver, timeout=args.timeout)

        # Execução da parte Bônus
        parte_bonus_multiplas_janelas(driver, timeout=args.timeout)

        logger.info("=" * 64)
        logger.info(
            "TODAS AS ETAPAS E O BÔNUS FORAM EXECUTADOS COM SUCESSO!"
        )
        logger.info("=" * 64)
        return 0

    except (TimeoutException, AssertionError, WebDriverException) as erro:
        logger.error(
            "ERRO durante a execução da automação: %s", erro, exc_info=True
        )
        return 1
    except Exception as erro_inesperado:
        logger.critical(
            "ERRO inesperado durante a execução: %s",
            erro_inesperado,
            exc_info=True
        )
        return 2
    finally:
        # Regra obrigatória: Garantir driver.quit() no bloco finally
        if driver is not None:
            logger.info("Encerramento seguro do driver no bloco finally...")
            try:
                driver.quit()
                logger.info("Driver encerrado com sucesso.")
            except Exception as e:
                logger.warning("Falha ao fechar o driver: %s", e)


if __name__ == "__main__":
    sys.exit(main())
