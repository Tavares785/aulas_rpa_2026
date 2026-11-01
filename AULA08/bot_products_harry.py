
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.maximize_window()

driver.implicitly_wait(3)


def aceitar_cookies():
    xpath = (
        "//*[@id='onetrust-accept-btn-handler'] | "
        "//button[contains(., 'Accept') or contains(., 'Aceitar') "
        "or contains(., 'Allow') or contains(., 'Agree')]"
    )
    botoes = driver.find_elements(By.XPATH, xpath)
    if len(botoes) > 0:
        driver.execute_script("arguments[0].click();", botoes[0])
        time.sleep(2)


driver.get("https://www.harrypotter.com/pt/login")
time.sleep(5)
aceitar_cookies()

driver.get("https://harrypottershop.com/collections/gifts/Under-$10")
time.sleep(8)
aceitar_cookies()

for i in range(20):
    botoes = driver.find_elements(
        By.XPATH, "//a[contains(., 'Load More')] | //button[contains(., 'Load More')]"
    )
    if len(botoes) == 0:
        break
    driver.execute_script("arguments[0].scrollIntoView();", botoes[0])
    time.sleep(1)
    driver.execute_script("arguments[0].click();", botoes[0])
    time.sleep(4)

cards = driver.find_elements(
    By.XPATH,
    "//*[@id='MainContent']//li[.//a[contains(@href, '/products/')]]",
)
print("Cards encontrados:", len(cards))

lista_produtos = []
titulos_vistos = []

for card in cards:
    links = card.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")
    titulo = links[-1].get_attribute("textContent").strip()

   
    texto_card = card.get_attribute("textContent")
    achou = re.search(r"\$\d+(\.\d+)?", texto_card)
    if achou:
        preco = achou.group()
    else:
        preco = "N/D"

   
    if titulo != "" and titulo not in titulos_vistos:
        titulos_vistos.append(titulo)
        produto = {"titulo": titulo, "Preço": preco}
        lista_produtos.append(produto)


print("=== PRODUTOS ENCONTRADOS ===")
for produto in lista_produtos:
    print(produto["titulo"], "-", produto["Preço"])

print("Total de produtos coletados:", len(lista_produtos))

driver.quit()