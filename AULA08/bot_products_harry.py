from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

# 1) Abre o Chrome (o Selenium 4.6+ baixa o driver sozinho)
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)  # espera ate 10s os elementos aparecerem na tela

# 2) Abre o site oficial na pagina de login
driver.get("https://www.harrypotter.com/pt/login")
sleep(3)

# 3) Vai para a loja: presentes com menos de 10 dolares
driver.get("https://harrypottershop.com/collections/gifts/Under-$10")

# 4) Clica em "Load More" ate aparecerem todos os produtos
for i in range(10):
    botoes = driver.find_elements(By.CSS_SELECTOR, "#LoadMoreButton a")
    if len(botoes) == 0 or not botoes[0].is_displayed():
        break  # sem botao = todos os produtos ja estao na tela
    driver.execute_script("arguments[0].click();", botoes[0])
    sleep(3)

# 5) Pega cada produto e guarda o titulo e o preco numa lista de dicionarios
produtos = []
cards = driver.find_elements(By.XPATH, '//*[@id="product-grid"]/li')

for card in cards:
    titulo = card.find_element(By.CSS_SELECTOR, ".card__heading a")
    preco = card.find_element(
        By.CSS_SELECTOR, ".price__regular .price-item--regular"
    )

    # textContent pega o texto mesmo escondido (o .text nao pega)
    produtos.append({
        "titulo": titulo.get_attribute("textContent").strip(),
        "Preço": preco.get_attribute("textContent").strip(),
    })

# 6) Mostra todos os produtos e o total no terminal
for produto in produtos:
    print(produto["titulo"], "-", produto["Preço"])

print("Total de produtos coletados:", len(produtos))

driver.quit()
