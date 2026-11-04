
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    driver.get("https://harrypottershop.com/collections/gifts/Under-$10")

    print("Página oficial do Harry Potter aberta!")

    wait.until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")) > 0
    )

    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")

    produtos = []
    encontrados = set()

    for link in links:
        titulo = link.find_elements(By.CSS_SELECTOR, ".card__heading")
        preco = link.find_elements(By.CSS_SELECTOR, ".card__price")

        nome = titulo[0].get_attribute("textContent").strip() if titulo else ""
        valor = preco[0].get_attribute("textContent").strip() if preco else ""

        if nome and nome not in encontrados:
            encontrados.add(nome)
            produtos.append({
                "titulo": nome,
                "preco": valor
            })

    print("\nPRODUTOS ENCONTRADOS:\n")

    for produto in produtos:
        print("Produto:", produto["titulo"])
        print("Preço:", produto["preco"])
        print("-" * 30)

    print("\nTotal de produtos:", len(produtos))

finally:
    driver.quit()
