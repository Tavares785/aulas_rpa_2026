import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def rodar_bot():
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    produtos_coletados = []

    try:
        driver.get("https://harrypotter.com")
        time.sleep(3)
        
        driver.get("https://harrypottershop.com")
        
        wait = WebDriverWait(driver, 15)
        cards_produtos = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.grid__item"))
        )
        
        for card in cards_produtos:
            try:
                titulo_elemento = card.find_element(By.CSS_SELECTOR, ".card__heading, h3")
                titulo = titulo_elemento.text.strip()
                
                preco_elemento = card.find_element(By.CSS_SELECTOR, ".price__regular, .price-item--regular")
                preco = preco_elemento.text.strip()
                
                if "Regular price" in preco:
                    preco = preco.replace("Regular price", "").strip()
                if "\n" in preco:
                    preco = preco.split("\n")[-1].strip()

                if titulo and preco:
                    produtos_coletados.append({
                        "titulo": titulo,
                        "Preço": preco
                    })
            except Exception:
                continue

        print("\n" + "="*50)
        print("PRODUTOS ENCONTRADOS (UNDER $10):")
        print("="*50)
        for produto in produtos_coletados:
            print(f"Título: {produto['titulo']} | Preço: {produto['Preço']}")
            
        print("="*50)
        print(f"Quantidade total coletada: {len(produtos_coletados)} produtos.")
        print("="*50)

    except Exception as e:
        print(f"Erro: {e}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    rodar_bot()
