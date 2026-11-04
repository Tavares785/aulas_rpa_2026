# Lab 08 - Web Scraping com Selenium
# Coleta o titulo e o preco dos produtos da loja Harry Potter (ate $10)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_LOJA = "https://harrypottershop.com/collections/gifts/Under-$10"

# 1. Abrir o navegador
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

# 2. Abrir o site oficial e depois ir para a loja
driver.get(URL_LOGIN)
driver.get(URL_LOJA)

# 3. Esperar a vitrine de produtos carregar
espera = WebDriverWait(driver, 15)
espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#product-grid > li")))

# 4. Coletar titulo e preco de cada produto
cards = driver.find_elements(By.CSS_SELECTOR, "#product-grid > li")

produtos = []
for card in cards:
    titulo = card.find_element(By.CSS_SELECTOR, ".card__heading a").get_attribute("textContent").strip()
    preco = card.find_element(By.CSS_SELECTOR, ".price-item--regular").get_attribute("textContent").strip()
    produtos.append({"titulo": titulo, "Preço": preco})

driver.quit()

# 5. Mostrar o resultado
for i, produto in enumerate(produtos, start=1):
    print(f"{i}. {produto['titulo']} - {produto['Preço']}")

print(f"\nTotal de produtos coletados: {len(produtos)}")
