import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

try:
  driver.get("https://www.harrypotter.com/pt/login")
  time.sleep(3)

  driver.get("https://harrypottershop.com/collections/gifts/Under-$10")
  time.sleep(4)

  produtos_elementos = driver.find_elements(
      By.CSS_SELECTOR, ".card-information, .product-item, .card"
  )

  lista_produtos = []

  for item in produtos_elementos:
    try:
      titulo_element = item.find_element(
          By.CSS_SELECTOR, ".card__heading, h3, .product-item__title"
      )
      titulo = titulo_element.text.strip()
    except:
      titulo = "Título não encontrado"

    try:
      preco_element = item.find_element(
          By.CSS_SELECTOR, ".price, .money, .price-item"
      )
      preco = preco_element.text.strip()
    except:
      preco = "Preço não encontrado"

    if titulo != "Título não encontrado" or preco != "Preço não encontrado":
      lista_produtos.append({"titulo": titulo, "Preço": preco})

  print("\n" + "=" * 40)
  print(f"📊 Quantidade total coletada: {len(lista_produtos)} produtos")
  print("=" * 40)

  for i, produto in enumerate(lista_produtos, 1):
    print(f"{i}. Título: {produto['titulo']} | Preço: {produto['Preço']}")

finally:
  driver.quit()