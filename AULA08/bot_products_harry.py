"""
bot_products_harry.py

Instalação:
    pip install selenium
"""

import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_PRODUTOS = "https://harrypottershop.com/collections/gifts/Under-$10"

PADRAO_PRECO = re.compile(r"[$R€£]\s?\d+[.,]?\d*")


def criar_driver():
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--start-maximized")
    return webdriver.Chrome(options=opcoes)


def fechar_popups(driver):
    """Tenta fechar banners de cookies/popups comuns."""
    textos = ["accept", "aceitar", "agree", "got it", "close", "fechar"]
    for botao in driver.find_elements(By.TAG_NAME, "button"):
        try:
            if botao.is_displayed() and botao.text.strip().lower() in textos:
                botao.click()
                time.sleep(1)
        except Exception:
            continue


def rolar_pagina(driver, vezes=8):
    """Rola aos poucos para carregar produtos com lazy loading."""
    for _ in range(vezes):
        driver.execute_script("window.scrollBy(0, 900);")
        time.sleep(1)


def achar_card(link):
    """Sobe na árvore do HTML até achar o bloco que contém o preço."""
    elemento = link
    for _ in range(5):
        elemento = elemento.find_element(By.XPATH, "..")
        if PADRAO_PRECO.search(elemento.text):
            return elemento
    return None


def coletar_produtos(driver):
    produtos = []
    vistos = set()

    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")
    for link in links:
        href = link.get_attribute("href")
        if not href or href in vistos:
            continue

        card = achar_card(link)
        if card is None:
            continue

        linhas = [l.strip() for l in card.text.split("\n") if l.strip()]
        precos = [l for l in linhas if PADRAO_PRECO.search(l)]
        titulos = [l for l in linhas if not PADRAO_PRECO.search(l) and len(l) > 3]

        if titulos and precos:
            vistos.add(href)
            produtos.append({"titulo": titulos[0], "Preço": precos[0]})

    return produtos


def main():
    driver = criar_driver()
    try:
        # 3. Abre o site oficial
        driver.get(URL_LOGIN)
        time.sleep(3)

        # 4. Navega até a coleção
        driver.get(URL_PRODUTOS)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/products/']"))
        )
        fechar_popups(driver)
        rolar_pagina(driver)

        # 5. Extrai título e preço
        produtos = coletar_produtos(driver)

        # Debug: salva o HTML se não achou nada
        if not produtos:
            with open("debug_pagina.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Nenhum produto encontrado. HTML salvo em debug_pagina.html")
            print("URL atual:", driver.current_url)

        # 6. Exibe resultado
        print("\n=== PRODUTOS ENCONTRADOS ===")
        for i, p in enumerate(produtos, start=1):
            print(f"{i}. {p['titulo']} - {p['Preço']}")
        print(f"\nTotal coletado: {len(produtos)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
