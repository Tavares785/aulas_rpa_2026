"""Lab 08 - Web Scraping com Selenium.

O bot abre o site oficial de Harry Potter, navega ate a colecao de
presentes abaixo de US$ 10 da Harry Potter Shop, extrai titulo e preco de
cada produto e exibe o resultado no terminal.
"""

import time

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_COLECAO = "https://harrypottershop.com/collections/gifts/Under-$10"
TEMPO_ESPERA = 15

# Seletores candidatos (o primeiro que encontrar produtos e usado).
SELETORES_CARD = [
    "li.grid__item",
    "div.product-card",
    "div.product-item",
    "div.grid-product",
    "[data-product-id]",
    "div.card-wrapper",
]
SELETORES_TITULO = [
    ".card__heading a",
    ".product-card__title",
    ".product-item__title",
    ".grid-product__title",
    "h3 a",
    "h2 a",
    "a[href*='/products/']",
]
SELETORES_PRECO = [
    ".price-item--sale",
    ".price-item--regular",
    ".price__regular",
    ".product-price",
    ".price",
    "[class*='price']",
]


def criar_driver():
    """Instancia o Chrome com espera implicita configurada."""
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opcoes)
    driver.implicitly_wait(5)
    return driver


def texto_do_primeiro(elemento, seletores):
    """Retorna o texto do primeiro seletor que achar conteudo no elemento."""
    for seletor in seletores:
        try:
            for item in elemento.find_elements(By.CSS_SELECTOR, seletor):
                texto = (item.get_attribute("textContent") or "").strip()
                if texto:
                    return " ".join(texto.split())
        except NoSuchElementException:
            continue
    return ""


def localizar_cards(driver):
    """Devolve a lista de cards de produto da pagina."""
    for seletor in SELETORES_CARD:
        try:
            cards = driver.find_elements(By.CSS_SELECTOR, seletor)
            cards = [c for c in cards if c.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")]
        except StaleElementReferenceException:
            return []
        if cards:
            return cards
    return []


def rolar_pagina(driver):
    """Rola ate o fim para carregar produtos montados via JavaScript."""
    altura = driver.execute_script("return document.body.scrollHeight")
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        nova_altura = driver.execute_script("return document.body.scrollHeight")
        if nova_altura == altura:
            break
        altura = nova_altura


def extrair_produtos(driver):
    """Le titulo e preco de cada card atualmente na pagina."""
    produtos = []
    vistos = set()
    for card in localizar_cards(driver):
        titulo = texto_do_primeiro(card, SELETORES_TITULO)
        preco = texto_do_primeiro(card, SELETORES_PRECO)
        if not titulo or titulo in vistos:
            continue
        vistos.add(titulo)
        produtos.append({"titulo": titulo, "Preço": preco or "indisponivel"})
    return produtos


def coletar_produtos(driver):
    """Espera a pagina carregar e extrai os produtos (com novas tentativas)."""
    espera = WebDriverWait(
        driver, TEMPO_ESPERA, ignored_exceptions=(StaleElementReferenceException,)
    )
    espera.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    try:
        espera.until(lambda d: len(localizar_cards(d)) > 0)
    except TimeoutException:
        return []

    rolar_pagina(driver)

    # O site pode remontar os cards apos a rolagem; tenta de novo se isso ocorrer.
    for _ in range(5):
        try:
            time.sleep(2)
            return extrair_produtos(driver)
        except StaleElementReferenceException:
            continue
    return []


def exibir_produtos(produtos):
    """Mostra os produtos e o total no terminal."""
    print("\n=== Produtos encontrados ===")
    for i, produto in enumerate(produtos, start=1):
        print(f"{i:02d}. {produto['titulo']} - {produto['Preço']}")
    print(f"\nTotal de produtos coletados: {len(produtos)}")


def main():
    driver = criar_driver()
    try:
        driver.get(URL_LOGIN)
        WebDriverWait(driver, TEMPO_ESPERA).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print(f"Pagina aberta: {driver.title}")

        driver.get(URL_COLECAO)
        produtos = coletar_produtos(driver)
        exibir_produtos(produtos)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
