"""
Bot de automação web com Selenium para extração de produtos Harry Potter.

Enunciado do Lab 08:
1. Instale a biblioteca selenium
2. Crie o script bot_products_harry.py
3. O bot deve abrir o navegador Chrome no site oficial:
   https://www.harrypotter.com/pt/login
5. Navegue até https://harrypottershop.com/collections/gifts/Under-$10
6. Para cada produto, extraia o Titulo e a Preço e guarde em uma lista de
   dicionários, ex.: {"titulo": ..., "Preço": ...}
7. Ao final, exiba no terminal todos os produtos encontrados (Titulo + Preço)
   e a quantidade total coletada.
"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_PRODUTOS = "https://harrypottershop.com/collections/gifts/Under-$10"

SELETORES_CARD = [
    "li.grid__item",
    ".product-card",
    ".product-item",
    ".card-wrapper",
    "[data-product-card]",
    "div[class*='product-card']",
    "div[class*='product-item']",
    "div[class*='grid-product']",
    ".product-tile",
    ".card",
]

SELETORES_TITULO = [
    ".card__heading",
    ".product-item__title",
    ".product-card__title",
    ".product-title",
    ".title",
    "h2",
    "h3",
    "h4",
    "a[href*='/products/']",
]

SELETORES_PRECO = [
    ".price",
    ".price__regular",
    ".price-item--regular",
    ".price-item--sale",
    ".product-item__price",
    ".product-card__price",
    ".price-item",
    ".money",
    "[class*='price']",
]

MOEDAS = ("$", "£", "€", "R$")


def criar_navegador() -> webdriver.Chrome:
    """Inicializa e configura uma instância do Chrome WebDriver."""
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--lang=pt-BR")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver


def fechar_modais_e_cookies(driver: webdriver.Chrome) -> None:
    """Fecha avisos de cookies ou popups se existirem na tela."""
    seletores = [
        "//button[@id='onetrust-accept-btn-handler']",
        "//button[contains(., 'Accept') or contains(., 'Aceitar')]",
        "//button[contains(., 'Close') or contains(., 'Fechar')]",
        "//button[contains(@class, 'modal__close')]",
        "//button[@aria-label='Close' or @aria-label='Fechar']",
    ]
    for xpath in seletores:
        try:
            for botao in driver.find_elements(By.XPATH, xpath):
                if botao.is_displayed():
                    botao.click()
                    sleep(0.5)
        except Exception:
            continue


def rolar_pagina(driver: webdriver.Chrome) -> None:
    """Rola suavemente a página para carregar conteúdo dinâmico."""
    try:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight / 3);"
        )
        sleep(1)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight / 1.5);"
        )
        sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        sleep(1)
    except Exception:
        pass


def extrair_titulo_card(card) -> str:
    """Extrai o título do produto a partir de um elemento card."""
    for t_sel in SELETORES_TITULO:
        try:
            elemento = card.find_element(By.CSS_SELECTOR, t_sel)
            texto = elemento.text.strip()
            if texto and len(texto) > 1:
                return texto.split("\n")[0].strip()
        except Exception:
            continue
    return ""


def extrair_preco_card(card) -> str:
    """Extrai o preço do produto a partir de um elemento card."""
    for p_sel in SELETORES_PRECO:
        try:
            elemento = card.find_element(By.CSS_SELECTOR, p_sel)
            texto = elemento.text.strip()
            if not texto:
                continue
            linhas = [lin.strip() for lin in texto.split("\n") if lin.strip()]
            for linha in linhas:
                if any(simb in linha for simb in MOEDAS):
                    return linha
            if linhas:
                return linhas[0]
        except Exception:
            continue
    return "Preço indisponível"


def obter_cards_produtos(driver: webdriver.Chrome) -> list:
    """Busca os cards de produto testando os seletores mais comuns."""
    for seletor in SELETORES_CARD:
        encontrados = driver.find_elements(By.CSS_SELECTOR, seletor)
        if encontrados:
            return encontrados
    return []


def extrair_produtos_de_cards(cards: list) -> list[dict[str, str]]:
    """Percorre a lista de cards e extrai título e preço."""
    produtos: list[dict[str, str]] = []
    titulos_registrados = set()

    for card in cards:
        titulo = extrair_titulo_card(card)
        if not titulo or titulo in titulos_registrados:
            continue

        preco = extrair_preco_card(card)
        titulos_registrados.add(titulo)
        produtos.append({"titulo": titulo, "Preço": preco})

    return produtos


def extrair_produtos_fallback(
    driver: webdriver.Chrome,
    titulos_registrados: set
) -> list[dict[str, str]]:
    """Localiza produtos por links diretos caso os cards não sejam achados."""
    produtos: list[dict[str, str]] = []
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")

    for link in links:
        nome = link.text.strip()
        if not nome or len(nome) < 3 or nome in titulos_registrados:
            continue

        preco = "Preço indisponível"
        try:
            xpath_ancestor = (
                "./ancestor::*[contains(@class, 'product') or position()=1]"
            )
            pai = link.find_element(By.XPATH, xpath_ancestor)
            precos = pai.find_elements(
                By.CSS_SELECTOR, "[class*='price'], .money"
            )
            for p_el in precos:
                p_txt = p_el.text.strip()
                if p_txt and any(simb in p_txt for simb in MOEDAS):
                    preco = p_txt
                    break
        except Exception:
            pass

        titulos_registrados.add(nome)
        produtos.append({"titulo": nome, "Preço": preco})

    return produtos


def coletar_produtos(driver: webdriver.Chrome) -> list[dict[str, str]]:
    """Localiza e extrai os produtos (título e preço) na página.

    Retorna uma lista de dicionários no formato:
        [{"titulo": ..., "Preço": ...}, ...]
    """
    _ = WebDriverWait(driver, 15)
    rolar_pagina(driver)

    cards = obter_cards_produtos(driver)
    produtos = extrair_produtos_de_cards(cards)

    if not produtos:
        produtos = extrair_produtos_fallback(driver, set())

    return produtos


def exibir_produtos(produtos: list[dict[str, str]]) -> None:
    """Exibe no terminal os produtos coletados e a quantidade total."""
    print("\n" + "=" * 65)
    print("PRODUTOS ENCONTRADOS - HARRY POTTER SHOP (Under $10)")
    print("=" * 65)

    if not produtos:
        print("Nenhum produto foi encontrado.")
    else:
        for idx, item in enumerate(produtos, start=1):
            print(f"[{idx:02d}] Título: {item['titulo']}")
            print(f"     Preço:  {item['Preço']}")
            print("-" * 65)

    print(f"\nQuantidade total de produtos coletados: {len(produtos)}")
    print("=" * 65 + "\n")


def main() -> None:
    """Fluxo principal do bot de scraping."""
    driver = criar_navegador()
    try:
        # 3. Abrir o navegador Chrome no site oficial de login
        print(f"1. Acessando site oficial de login: {URL_LOGIN}")
        driver.get(URL_LOGIN)
        fechar_modais_e_cookies(driver)
        sleep(2)

        # 5. Navegar até a coleção de presentes até $10
        print(f"2. Navegando até a loja: {URL_PRODUTOS}")
        driver.get(URL_PRODUTOS)
        fechar_modais_e_cookies(driver)
        sleep(3)

        # 6. Extrair os produtos (Título e Preço)
        print("3. Coletando produtos da página...")
        produtos = coletar_produtos(driver)

        # 7. Exibir todos os produtos e a contagem total no terminal
        exibir_produtos(produtos)

    finally:
        print("Encerrando navegador...")
        driver.quit()


if __name__ == "__main__":
    main()
