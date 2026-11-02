import csv  # Módulo: grava e lê arquivos CSV.
import logging  # Módulo: registra eventos, avisos e erros.
import os  # Módulo: lê variáveis de ambiente.
import sys  # Módulo: permite direcionar logs ao terminal.
from pathlib import Path  # Classe: representa caminhos de arquivos.

from dotenv import load_dotenv  # Função: carrega o arquivo .env.
from selenium import webdriver  # Módulo: controla o navegador.
from selenium.common.exceptions import (
    NoSuchElementException,  # Exceção: elemento não encontrado.
    TimeoutException,  # Exceção: tempo de espera excedido.
    WebDriverException,  # Classe-base: erros do Selenium WebDriver.
)
from selenium.webdriver.common.by import By  # Classe: estratégias de localização.
from selenium.webdriver.support import expected_conditions as EC  # Condições de espera.
from selenium.webdriver.support.ui import WebDriverWait  # Classe: espera explícita.


# ============================================================
# 1. CAMINHOS E CONFIGURAÇÕES
# ============================================================

# Exemplo (ilustrativo):
# __file__ = "D:/faculdade/aulas_rpa_2026/AULA08/bot_products_harry.py"
# Path(__file__).resolve() → caminho completo do arquivo .py.
# .parent → "D:/faculdade/aulas_rpa_2026/AULA08" (pasta do script).
PASTA_SCRIPT = Path(__file__).resolve().parent
# Operador / de Path: junta pasta + nome do arquivo.
# Ex.: ".../AULA08" / ".env" → ".../AULA08/.env".
CAMINHO_ENV = PASTA_SCRIPT / ".env"
# Ex.: ".../AULA08" / "produtos_harry.csv" → caminho do CSV.
CAMINHO_CSV = PASTA_SCRIPT / "produtos_harry.csv"
# Ex.: ".../AULA08" / "execucao_bot.log" → caminho do log.
CAMINHO_LOG = PASTA_SCRIPT / "execucao_bot.log"

URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_LOJA = "https://harrypottershop.com/collections/gifts/Under-$10"
# Seletor: procura <li class="grid__item"> filhos diretos de <ul id="product-grid">.
# Ex.: 18 cartões HTML → lista de 18 elementos WebElement.
SELETOR_PRODUTOS = "#product-grid > li.grid__item"
# Seletor: encontra o <a> clicável dentro de <div id="LoadMoreButton">.
# Ex.: <div id="LoadMoreButton"><a>Load More</a></div> → o <a>.
SELETOR_LOAD_MORE = "#LoadMoreButton a"
MAX_CLIQUES = 100  # Limite de segurança contra repetição inesperada.


# ============================================================
# 2. CONFIGURAÇÃO DOS LOGS
# ============================================================

# getLogger(): obtém o registrador usado pelas etapas do programa.
# Ex.: logger.info("Login iniciado") → mensagem com nível INFO no terminal/log.
logger = logging.getLogger("bot_harry")
logger.setLevel(logging.DEBUG)  # O logger aceita DEBUG e níveis mais altos.
logger.propagate = False  # Evita duplicação no logger principal do Python.

# Formatter(): organiza os campos de cada linha do log.
# Ex.: INFO + "Chrome iniciado" → "2026-11-02 10:30:00 | INFO | Chrome iniciado".
formato = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# StreamHandler(): envia registros ao terminal (stdout).
saida_terminal = logging.StreamHandler(sys.stdout)
saida_terminal.setLevel(logging.INFO)  # INFO, WARNING, ERROR e CRITICAL.
saida_terminal.setFormatter(formato)
logger.addHandler(saida_terminal)

# FileHandler(): salva registros em um arquivo persistente.
# mode="a": adiciona registros sem apagar execuções anteriores.
saida_arquivo = logging.FileHandler(
    CAMINHO_LOG, mode="a", encoding="utf-8"
)
saida_arquivo.setLevel(logging.DEBUG)  # Inclui detalhes dos produtos.
saida_arquivo.setFormatter(formato)
logger.addHandler(saida_arquivo)


# ============================================================
# 3. INICIALIZAÇÃO E CREDENCIAIS
# ============================================================

driver = None  # Permite verificar no finally se o Chrome foi criado.
logger.info("Iniciando a automação Harry Potter.")

try:
    # load_dotenv(): lê o .env e disponibiliza suas variáveis ao processo.
    # Ex.: linha EMAIL=teste@exemplo.com no .env → os.getenv("EMAIL")
    # retorna "teste@exemplo.com". NÃO registrar senhas ou valores reais.
    load_dotenv(dotenv_path=CAMINHO_ENV)
    EMAIL = os.getenv("EMAIL")  # Antes: chave "EMAIL" → depois: valor ou None.
    SENHA = os.getenv("SENHA")  # Antes: chave "SENHA" → depois: valor ou None.

    # Cenário desfavorável: arquivo .env ausente ou incompleto.
    if not EMAIL or not SENHA:
        raise ValueError("EMAIL ou SENHA não configurados no arquivo .env.")

    # Não registrar EMAIL, SENHA nem outros segredos nos logs.
    logger.info("Configurações de autenticação carregadas.")

    # webdriver.Chrome(): cria a sessão do navegador automatizado.
    # Ex.: navegador fechado → nova janela Chrome controlada pelo Selenium.
    driver = webdriver.Chrome()
    # WebDriverWait(): cria espera explícita de até 15 s; não pausa sempre 15 s.
    # Ex.: elemento aparece após 2 s → espera termina em ~2 s.
    espera = WebDriverWait(driver, 15)
    logger.info("Navegador Chrome iniciado.")

    # ========================================================
    # 4. ACESSO AO LOGIN E COOKIES
    # ========================================================

    # .get(): navega para URL_LOGIN.
    # Ex.: página em branco → "https://www.harrypotter.com/pt/login".
    driver.get(URL_LOGIN)
    logger.info("Página de login acessada.")

    try:
        botao_cookies = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.ID, "onetrust-accept-btn-handler")
            )
        )
        # .click(): aciona o elemento <button> já localizado.
        # Ex.: aviso de cookies aberto → clique enviado ao botão Aceitar.
        botao_cookies.click()
        logger.info("Cookies da página de login aceitos.")
    except TimeoutException:
        # Situação normal possível: cookies já aceitos anteriormente.
        logger.warning("Aviso de cookies do login não apareceu em 5 s.")

    # ========================================================
    # 5. PREENCHIMENTO E ACIONAMENTO DO LOGIN
    # ========================================================

    campo_email = espera.until(
        EC.visibility_of_element_located((By.ID, "emailAddress"))
    )
    # .send_keys(): digita o texto armazenado em EMAIL no campo HTML.
    # Ex.: campo vazio → campo preenchido; o valor não aparece nos logs.
    campo_email.send_keys(EMAIL)
    logger.debug("Campo de e-mail preenchido (valor não registrado).")

    campo_senha = espera.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    # .send_keys(): digita SENHA sem expor o valor no código/log.
    # Ex.: campo vazio → campo preenchido com caracteres mascarados.
    campo_senha.send_keys(SENHA)
    logger.debug("Campo de senha preenchido (valor não registrado).")

    botao_login = espera.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-testid="loginButton"]')
        )
    )
    # .current_url: obtém a URL antes do clique; não altera o navegador.
    # Ex.: ".../pt/login" → variável url_antes_login.
    url_antes_login = driver.current_url
    # .click(): envia o clique; isso NÃO garante autenticação bem-sucedida.
    # Ex.: botão "Log In" habilitado → tentativa de login iniciada.
    botao_login.click()
    logger.info("Botão de login acionado (autenticação ainda não confirmada).")

    try:
        # EC.url_changes(): condição de mudança de URL.
        # Ex.: ".../pt/login" → ".../pt/account": condição verdadeira.
        # A mudança de URL NÃO é prova suficiente de login autorizado.
        WebDriverWait(driver, 10).until(EC.url_changes(url_antes_login))
        logger.info("Mudança de URL detectada após o login.")
    except TimeoutException:
        # Cenário desfavorável: login inválido ou página sem redirecionamento.
        # A ausência de mudança NÃO comprova falha de autenticação.
        logger.warning("Não houve mudança de URL em até 10 s após o login.")

    # ========================================================
    # 6. ACESSO À LOJA, COOKIES E MODAL
    # ========================================================

    # .get(): navega para a coleção de presentes por menos de US$ 10.
    # Ex.: página de login → página da lista de produtos.
    driver.get(URL_LOJA)
    logger.info("Loja acessada: %s", driver.current_url)
    logger.debug("Título HTML: %s", driver.title)

    try:
        botao_cookies_loja = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.ID, "onetrust-accept-btn-handler")
            )
        )
        botao_cookies_loja.click()
        logger.info("Cookies da loja aceitos.")
    except TimeoutException:
        logger.warning("Aviso de cookies da loja não apareceu em 5 s.")

    try:
        botao_permanecer = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.ID, "ModalClose-redirect-template-2")
            )
        )
        botao_permanecer.click()
        logger.info("Modal fechado: Stay in this site.")
    except TimeoutException:
        logger.warning("Modal de redirecionamento não apareceu em 5 s.")

    # Aguarda pelo menos um cartão antes de iniciar a contagem.
    espera.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, SELETOR_PRODUTOS))
    )

    # ========================================================
    # 7. LOAD MORE: CARREGAMENTO DOS PRODUTOS
    # ========================================================

    cliques = 0  # Ex.: 0 → 1 após o primeiro clique no Load More.

    # while True: verifica e tenta carregar outra leva de produtos.
    # Ex.: 18 itens → clique → 30 itens → verifica se resta botão.
    while True:
        # .find_elements(): procura TODOS os cartões no HTML; devolve lista.
        # Ex.: 18 cartões HTML → [WebElement, ...] com 18 elementos.
        produtos_antes = driver.find_elements(By.CSS_SELECTOR, SELETOR_PRODUTOS)
        # len(): transforma a lista em sua quantidade de itens.
        # Ex.: [18 WebElements] → 18.
        quantidade_antes = len(produtos_antes)

        # .find_elements(): procura o link; sem resultado, retorna [].
        # Ex.: botão presente → [WebElement]; botão ausente → [].
        botoes = driver.find_elements(By.CSS_SELECTOR, SELETOR_LOAD_MORE)
        # not botoes: [] → True; [WebElement] → False.
        if not botoes:
            logger.info(
                "Load More não encontrado; encerrando a busca com %d produtos.",
                quantidade_antes,
            )
            break

        # Cenário extremo: evitar repetição indefinida após mudanças no site.
        if cliques >= MAX_CLIQUES:
            logger.error("Limite de segurança de %d cliques atingido.", MAX_CLIQUES)
            break

        try:
            botao_load_more = espera.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SELETOR_LOAD_MORE))
            )
            # .click(): solicita ao site mais cartões de produto.
            # Ex.: 18 produtos exibidos → clique enviado; pode ainda haver 18.
            botao_load_more.click()
            # += 1: atualiza o contador; ex.: cliques = 0 → 1.
            cliques += 1
            logger.debug("Clique número %d no Load More realizado.", cliques)

            # .until(lambda ...): espera uma contagem MAIOR que a anterior.
            # Ex.: antes=18; durante=18 → False; depois=30 → True.
            # Essa espera confirma novos itens, não apenas o clique.
            espera.until(
                lambda navegador: len(
                    navegador.find_elements(By.CSS_SELECTOR, SELETOR_PRODUTOS)
                ) > quantidade_antes
            )
        except TimeoutException:
            # Pior cenário: a loja não carregou itens ou o link não ficou clicável.
            logger.warning(
                "Clique/carregamento não confirmado em 15 s; "
                "interrompendo para evitar repetição sem progresso."
            )
            break

        # .find_elements() + len(): conta os cartões após a espera.
        # Ex.: antes=18 → depois=30; foram adicionados 12.
        quantidade_depois = len(
            driver.find_elements(By.CSS_SELECTOR, SELETOR_PRODUTOS)
        )
        logger.info("Produtos carregados: %d → %d.", quantidade_antes, quantidade_depois)

    # ========================================================
    # 8. EXTRAÇÃO DE NOME, PREÇO E LINK
    # ========================================================

    # .find_elements(): obtém TODOS os cartões após o Load More.
    # Ex.: 30 produtos na página → lista com 30 elementos WebElement.
    cartoes = driver.find_elements(By.CSS_SELECTOR, SELETOR_PRODUTOS)
    logger.info("Iniciando extração de %d cartões.", len(cartoes))
    # Lista: começa vazia; receberá um dicionário por produto válido.
    # Ex.: [] → [{"nome": "...", "preco": "...", "link": "..."}, ...].
    dados_produtos = []

    # enumerate(): produz pares (número, cartão), começando pelo 1.
    # Ex.: primeiro WebElement → (1, WebElement); segundo → (2, WebElement).
    for numero, cartao in enumerate(cartoes, start=1):
        try:
            # .find_element(): procura o link do título DENTRO do cartão atual.
            # Ex.: primeiro cartão → <a> Peppermint Toads Chocolate </a>.
            elemento_nome = cartao.find_element(By.CSS_SELECTOR, ".card__heading a")
            # .text: lê o texto visível; .strip(): tira espaços nas pontas.
            # Ex.: "  Peppermint Toads Chocolate  " → "Peppermint Toads Chocolate".
            nome = elemento_nome.text.strip()
            # .get_attribute("href"): lê o endereço do elemento <a>.
            # Ex.: href="/products/peppermint-toads-chocolate"
            # → "https://harrypottershop.com/products/peppermint-toads-chocolate".
            link = elemento_nome.get_attribute("href")

            # .find_elements(): procura preço promocional dentro do cartão.
            # Ex.: sem promoção → []; com promoção → [WebElement].
            # Preferimos o valor atual em vez do preço antigo riscado.
            precos_promocionais = cartao.find_elements(
                By.CSS_SELECTOR,
                ".price--on-sale .price__sale .price-item--sale",
            )
            if precos_promocionais:
                # [0]: primeiro preço em promoção; .text.strip(): limpa espaços.
                # Ex.: "  $7.00  " → "$7.00" (valor ilustrativo).
                preco = precos_promocionais[0].text.strip()
                logger.debug("Produto %d está em promoção.", numero)
            else:
                elemento_preco = cartao.find_element(
                    By.CSS_SELECTOR, ".price__regular .price-item--regular"
                )
                # .text.strip(): converte o texto visível no preço sem espaços.
                # Ex.: "  $9.00\n " → "$9.00".
                preco = elemento_preco.text.strip()

            # Cenário desfavorável: cartão incompleto no HTML.
            if not nome or not preco or not link:
                logger.warning("Cartão %d com dados vazios; ignorado.", numero)
                continue

            # Dicionário: associa cada campo ao valor extraído.
            # Ex.: nome="Peppermint Toads Chocolate", preco="$9.00" →
            # {"nome": "Peppermint Toads Chocolate", "preco": "$9.00", "link": "..."}.
            produto = {"nome": nome, "preco": preco, "link": link}
            # .append(): acrescenta um produto à lista de resultados.
            # Ex.: 0 dicionários → 1; ... → 30 (se todos forem válidos).
            dados_produtos.append(produto)
            logger.debug("Produto %d extraído: %s | %s | %s", numero, nome, preco, link)

        except NoSuchElementException:
            # Não impede que os demais cartões sejam processados.
            logger.warning("Cartão %d sem nome ou preço identificável; ignorado.", numero)

    logger.info(
        "Extração concluída: %d produto(s) válido(s) de %d cartão(ões).",
        len(dados_produtos), len(cartoes)
    )

    if not dados_produtos:
        # Cenário crítico: nenhum dado útil foi coletado; não criar CSV vazio.
        raise ValueError("Nenhum produto válido foi extraído; CSV não será criado.")

    # ========================================================
    # 9. EXPORTAÇÃO PARA CSV
    # ========================================================

    # .open(mode="w"): cria ou SOBRESCREVE o arquivo na pasta AULA08.
    # Ex.: CSV anterior com 20 linhas → novo CSV baseado na coleta atual.
    # with: fecha o arquivo automaticamente após a escrita.
    # newline="": evita linhas em branco extras no Windows.
    # utf-8-sig: facilita reconhecer caracteres acentuados no Excel.
    with CAMINHO_CSV.open(mode="w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(
            arquivo, fieldnames=["nome", "preco", "link"], delimiter=";"
        )
        # .writeheader(): primeira linha → "nome;preco;link".
        escritor.writeheader()
        # .writerows(): converte os dicionários em linhas do CSV.
        # Ex.: {"nome":"Bottled Butterbeer", "preco":"$7.00", ...}
        # → "Bottled Butterbeer;$7.00;https://...".
        escritor.writerows(dados_produtos)

    logger.info("CSV gerado com %d produtos: %s", len(dados_produtos), CAMINHO_CSV)
    logger.info("Arquivo de logs: %s", CAMINHO_LOG)

    # input(): pausa a execução esperando Enter no terminal.
    # Ex.: Chrome permanece aberto → usuário pressiona Enter → finally.
    input("Pressione Enter para encerrar...")

# ============================================================
# 10. TRATAMENTO DOS CENÁRIOS DESFAVORÁVEIS
# ============================================================

except TimeoutException:
    # exception(): registra mensagem + traceback (linha da falha).
    logger.exception("Tempo de espera excedido em uma etapa obrigatória.")
except WebDriverException:
    logger.exception("Falha no WebDriver ou na comunicação com o Chrome.")
except (OSError, csv.Error):
    logger.exception("Falha ao criar ou escrever o arquivo CSV/log.")
except ValueError:
    logger.exception("Configuração ou dados inválidos.")
except KeyboardInterrupt:
    logger.warning("Automação interrompida manualmente (Ctrl+C).")
except Exception:
    # Última proteção: erros de programação não previstos.
    logger.exception("Erro inesperado durante a automação.")
finally:
    if driver is not None:
        try:
            logger.info("Encerrando navegador...")
            # .quit(): encerra a sessão e a janela controlada pelo WebDriver.
            # Ex.: navegador aberto → sessão finalizada após Enter.
            driver.quit()
            logger.info("Navegador encerrado.")
        except WebDriverException:
            logger.exception("Não foi possível encerrar a sessão normalmente.")
    logger.info("Fim da execução.")
