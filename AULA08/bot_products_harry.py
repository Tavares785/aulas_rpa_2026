"""
Lab 08: Web Scraping e Interação com Elementos via Selenium.

Extração de produtos da loja Harry Potter (título e preço).
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def coletar_produtos():
    """Acessa a loja oficial do Harry Potter e extrai produtos."""
    url = "https://harrypottershop.com/collections/gifts/Under-$10"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    produtos = []

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card, .product"))
        )

        cards = driver.find_elements(By.CSS_SELECTOR, ".card, .product-card")

        for card in cards:
            try:
                elem_titulo = card.find_element(
                    By.CSS_SELECTOR, ".card__heading, .title, h3"
                )
                titulo = elem_titulo.text.strip()
            except Exception:
                titulo = "Sem título"

            try:
                elem_preco = card.find_element(
                    By.CSS_SELECTOR, ".price-item, .price"
                )
                preco = elem_preco.text.strip()
            except Exception:
                preco = "Sem preço"

            if titulo != "Sem título":
                produtos.append({"titulo": titulo, "preco": preco})

        print(f"Total de produtos coletados: {len(produtos)}")
        for item in produtos:
            print(f"Título: {item['titulo']} | Preço: {item['preco']}")

    finally:
        driver.quit()

    return produtos


if __name__ == "__main__":
    coletar_produtos()
