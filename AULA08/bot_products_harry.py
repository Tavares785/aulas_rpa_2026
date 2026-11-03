"""Coleta produtos da loja Harry Potter e mostra título e preço."""

from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_SHOP = "https://harrypottershop.com/collections/gifts/Under-$10"


def criar_navegador() -> webdriver.Chrome:
    """Cria uma instância do Chrome em modo headless para execução mais rápida."""
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--lang=pt-BR")
    return webdriver.Chrome(options=options)


def buscar_texto(elemento: Any, seletores: list[str]) -> str:
    """Retorna o texto de um primeiro seletor que exista dentro do elemento."""
    for seletor in seletores:
        try:
            alvo = elemento.find_element(By.CSS_SELECTOR, seletor)
        except NoSuchElementException:
            continue
        texto = (alvo.text or alvo.get_attribute("textContent") or "").strip()
        if texto:
            return texto
    return ""


def coletar_produtos(driver: webdriver.Chrome) -> list[dict[str, str]]:
    """Coleta título e preço de todos os produtos da coleção, percorrendo as páginas."""
    driver.set_page_load_timeout(30)
    driver.get(URL_SHOP)

    seletores_cards = [
        "article.product-card",
        ".product-card",
        "[class*='product-card']",
        "li.product",
        ".card-product",
    ]
    wait = WebDriverWait(driver, 12)
    seletor_cards = ", ".join(seletores_cards)

    produtos: list[dict[str, str]] = []
    produtos_coletados: set[str] = set()
    paginas_visitadas: set[str] = set()

    while driver.current_url not in paginas_visitadas:
        paginas_visitadas.add(driver.current_url)
        try:
            wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, seletor_cards))
            )
        except TimeoutException as erro:
            raise TimeoutException(
                f"Não foi possível carregar os produtos da página {driver.current_url}"
            ) from erro

        cards = []
        for seletor in seletores_cards:
            cards = driver.find_elements(By.CSS_SELECTOR, seletor)
            if cards:
                break

        for card in cards:
            titulo = buscar_texto(
                card,
                [
                    ".card__heading",
                    "h3",
                    ".product-card__title",
                    "a[href*='/products/']",
                    "[data-product-title]",
                ],
            )
            if not titulo:
                continue

            href = card.get_attribute("href")
            if not href:
                try:
                    href = card.find_element(
                        By.CSS_SELECTOR, "a[href*='/products/']"
                    ).get_attribute("href")
                except NoSuchElementException:
                    href = None
            chave = urlparse(urljoin(driver.current_url, href)).path if href else titulo
            if chave in produtos_coletados:
                continue

            preco = buscar_texto(
                card,
                [
                    ".price-item--sale",
                    ".price-item--regular",
                    ".price-item",
                    ".money",
                    ".price",
                    ".card__price",
                    ".product-card__price",
                    "[class*='price']",
                ],
            )
            produtos_coletados.add(chave)
            produtos.append({"titulo": titulo, "Preço": preco or "Preço indisponível"})

        pagina_atual = int(parse_qs(urlparse(driver.current_url).query).get("page", ["1"])[0])
        proxima_pagina = None
        for link in driver.find_elements(By.CSS_SELECTOR, "a[href*='page=']"):
            href = link.get_attribute("href")
            if not href:
                continue
            url_pagina = urljoin(driver.current_url, href)
            parsed_url = urlparse(url_pagina)
            pagina_link = parse_qs(parsed_url.query).get("page", ["1"])[0]
            if parsed_url.path == urlparse(URL_SHOP).path and pagina_link.isdigit():
                if int(pagina_link) > pagina_atual:
                    if proxima_pagina is None or int(pagina_link) < proxima_pagina[0]:
                        proxima_pagina = (int(pagina_link), url_pagina)

        if proxima_pagina is None:
            break
        driver.get(proxima_pagina[1])

    return produtos


def main() -> None:
    driver = criar_navegador()
    try:
        produtos = coletar_produtos(driver)
        if not produtos:
            print("Nenhum produto encontrado.")
            return

        for produto in produtos:
            print(f"{produto['titulo']} - {produto['Preço']}")

        print(f"\nProdutos encontrados: {len(produtos)}")
        print(f"Total coletado: {len(produtos)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as erro:
        print(f"Erro ao coletar produtos: {erro}")
