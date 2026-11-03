import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

driver.implicitly_wait(10)

lista_produtos = []

try:
    print("Acessando a página de login inicial...")
    driver.get("https://www.harrypotter.com/pt/login")
    time.sleep(3) 
    
    print("Navegando até a loja (Gifts Under $10)...")
    driver.get("https://harrypottershop.com/collections/gifts/Under-$10")
    
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.grid__item, .product-card")))
    
    produtos_elementos = driver.find_elements(By.CSS_SELECTOR, "li.grid__item, .product-card")
    
    for produto in produtos_elementos:
        try:
            titulo_text = produto.find_element(By.CSS_SELECTOR, "a.full-unstyled-link, .product-card__title, h3").text.strip()
            preco_text = produto.find_element(By.CSS_SELECTOR, "span.price-item, .money").text.strip()
            
            if titulo_text and preco_text:
                dicionario_produto = {
                    "titulo": titulo_text,
                    "Preço": preco_text
                }
                lista_produtos.append(dicionario_produto)
        except Exception:
            continue

    print("\n" + "="*40)
    print("        PRODUTOS ENCONTRADOS")
    print("="*40)
    for prod in lista_produtos:
        print(f"Título: {prod['titulo']} | Preço: {prod['Preço']}")
        
    print("="*40)
    print(f"Quantidade total coletada: {len(lista_produtos)} produtos.")
    print("="*40)

finally:
    print("\nFechando o navegador...")
    driver.quit()
