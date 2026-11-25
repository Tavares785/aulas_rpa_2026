"""Coleta títulos e preços dos produtos Harry Potter abaixo de US$ 10."""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_PRODUTOS = "https://harrypottershop.com/collections/gifts/Under-$10"
SELETOR_PRODUTOS = "ul.product-grid > li.grid__item"


def coletar_produtos(driver: webdriver.Chrome) -> list[dict[str, str]]:
    """Coleta produtos da coleção, incluindo os carregados pelo botão."""
    driver.get(URL_PRODUTOS)
    WebDriverWait(driver, 30).until(
        lambda navegador: navegador.find_elements(
            By.CSS_SELECTOR, SELETOR_PRODUTOS
        )
    )
    botao_ficar_no_site = driver.find_elements(
        By.XPATH, "//button[normalize-space(.)='Stay in this site']"
    )
    if botao_ficar_no_site:
        botao_ficar_no_site[0].click()

    produtos = []
    urls_coletadas = set()

    while True:
        cards = driver.find_elements(By.CSS_SELECTOR, SELETOR_PRODUTOS)
        for card in cards:
            titulo_card = card.find_elements(By.CSS_SELECTOR, ".card__heading")
            if not titulo_card:
                continue

            links = titulo_card[0].find_elements(By.TAG_NAME, "a")
            if not links:
                continue
            link = links[0]
            url = link.get_attribute("href")
            if url in urls_coletadas:
                continue

            titulo = (link.get_attribute("textContent") or "").strip()
            precos = card.find_elements(By.CSS_SELECTOR, ".price-item--sale")
            if not precos:
                precos = card.find_elements(
                    By.CSS_SELECTOR, ".price-item--regular"
                )
            preco = (precos[0].get_attribute("textContent") or "").strip()

            if not titulo or not preco:
                raise ValueError(f"Título ou preço não encontrado para {url}")

            produtos.append({"titulo": titulo, "Preço": preco})
            urls_coletadas.add(url)

        botao_carregar_mais = driver.find_elements(
            By.CSS_SELECTOR, "#LoadMoreButton a[href*='?page=']"
        )
        if not botao_carregar_mais:
            break

        quantidade_anterior = len(cards)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#LoadMoreButton a[href*='?page=']")
            )
        ).click()
        WebDriverWait(driver, 30).until(
            lambda navegador: len(
                navegador.find_elements(By.CSS_SELECTOR, SELETOR_PRODUTOS)
            )
            > quantidade_anterior
        )

    return produtos


def main() -> None:
    driver = webdriver.Chrome()
    try:
        driver.get(URL_LOGIN)
        time.sleep(5)
        produtos = coletar_produtos(driver)
        if not produtos:
            print("Nenhum produto encontrado.")
            return

        print("Produtos encontrados:")
        for produto in produtos:
            print(f"- {produto['titulo']}: {produto['Preço']}")
        print(f"\nQuantidade total: {len(produtos)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
