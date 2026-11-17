"""
AULA 08 - Automacao Web com Selenium
Web Scraping de Produtos Harry Potter

Aluno: Kaua David Dantas Mendonca
RA: 6326260
"""

import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_PRODUTOS = "https://harrypottershop.com/collections/gifts/Under-$10"


def criar_navegador(headless: bool = False) -> webdriver.Chrome:
    """Configura e instancia o Chrome WebDriver."""
    options = Options()
    if headless or os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=pt-BR")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    # Configuracao de espera implicita
    driver.implicitly_wait(10)
    return driver


def aceitar_cookies(driver: webdriver.Chrome) -> None:
    """Tenta fechar ou aceitar avisos de cookies caso existam na tela."""
    termos = ("Accept", "Aceitar", "ACEITAR", "Aceito", "Agree")
    for termo in termos:
        try:
            botao = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//button[contains(., '{termo}')]")
                )
            )
            botao.click()
            time.sleep(1)
            return
        except Exception:
            continue


def coletar_produtos(driver: webdriver.Chrome) -> list[dict[str, str]]:
    """Abre o portal oficial, navega ate a loja e extrai os produtos.

    Retorna uma lista de dicionarios contendo Titulo e Preco de cada item:
        [{"titulo": "...", "Preço": "..."}, ...]
    """
    # 1. Abre a pagina oficial informada no enunciado
    print(f"Acessando portal inicial: {URL_LOGIN}")
    driver.get(URL_LOGIN)
    aceitar_cookies(driver)
    time.sleep(2)

    # 2. Navega ate a secao da loja Harry Potter Shop
    print(f"Navegando ate a loja: {URL_PRODUTOS}")
    driver.get(URL_PRODUTOS)
    aceitar_cookies(driver)

    # Espera explicita ate os cards de produtos serem carregados
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".product-card-wrapper, .card-wrapper, [class*='product-card']")
        )
    )

    # Rola a pagina para garantir carregamento dinamico
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Localiza os cards de produtos
    cards = driver.find_elements(
        By.CSS_SELECTOR, ".product-card-wrapper"
    )
    if not cards:
        cards = driver.find_elements(By.CSS_SELECTOR, ".card-wrapper")

    produtos: list[dict[str, str]] = []

    for card in cards:
        # Extrai o titulo do produto
        titulo = ""
        try:
            elem_titulo = card.find_element(
                By.CSS_SELECTOR, ".card__heading, [class*='card__heading'], h3"
            )
            titulo = (
                elem_titulo.text
                or elem_titulo.get_attribute("textContent")
                or elem_titulo.get_attribute("innerText")
                or ""
            ).strip()
        except Exception:
            continue

        if not titulo:
            continue

        # Extrai o preco do produto
        preco = ""
        try:
            elem_preco = card.find_element(
                By.CSS_SELECTOR,
                ".price-item--regular, .price-item, .price__regular, .price"
            )
            raw_preco = (
                elem_preco.text
                or elem_preco.get_attribute("textContent")
                or elem_preco.get_attribute("innerText")
                or ""
            ).strip()
            match = re.search(r"\$\s*\d+(?:\.\d{2})?", raw_preco)
            preco = match.group(0) if match else raw_preco
        except Exception:
            preco = "N/D"

        produtos.append({
            "titulo": titulo,
            "Preço": preco
        })

    return produtos


def exibir_produtos(produtos: list[dict[str, str]]) -> None:
    """Exibe os produtos coletados e a quantidade total no terminal."""
    print("\n" + "=" * 60)
    print("PRODUTOS ENCONTRADOS - HARRY POTTER SHOP")
    print("=" * 60)

    for i, produto in enumerate(produtos, start=1):
        print(f"[{i:02d}] Titulo: {produto['titulo']}")
        print(f"     Preço : {produto['Preço']}")
        print("-" * 60)

    print(f"\nTotal de produtos coletados: {len(produtos)}\n")


def main() -> None:
    """Funcao principal de execucao do bot."""
    driver = criar_navegador(headless=False)
    try:
        produtos = coletar_produtos(driver)
        exibir_produtos(produtos)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
