import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        # 1. Login solicitado no enunciado
        print("Abrindo o site de login...")
        driver.get("https://www.harrypotter.com/pt/login")
        time.sleep(3)
        
        print("Navegando para a página de produtos...")
        driver.get("https://harrypottershop.com/collections/gifts/Under-$10")
        
        print("Aguardando carregamento inicial da loja...")
        time.sleep(5)
        
        print("Procurando o botão 'Go to the international site'...")
        botoes_internacional = [
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'international')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'international')]",
            "//*[contains(text(), 'Go to the international site')]",
            "//*[contains(text(), 'International')]"
        ]
        
        for xpath in botoes_internacional:
            try:
                elem_inter = driver.find_element(By.XPATH, xpath)
                if elem_inter.is_displayed():
                    elem_inter.click()
                    print("✅ Botão 'Go to the international site' clicado!")
                    time.sleep(3)
                    break
            except:
                continue

        print("Tentando aceitar cookies...")
        botoes_cookie = [
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
            "//button[contains(@id, 'accept')]",
            "//button[contains(@class, 'accept')]",
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]"
        ]
        
        for xpath in botoes_cookie:
            try:
                elem_cookie = driver.find_element(By.XPATH, xpath)
                if elem_cookie.is_displayed():
                    elem_cookie.click()
                    print("✅ Cookies aceitos!")
                    time.sleep(2)
                    break
            except:
                continue

        print("Procurando e clicando na seção 'Shop Hogwarts'...")
        wait = WebDriverWait(driver, 15)
        
        try:
            secao_hogwarts = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Shop Hogwarts') or contains(text(), 'Hogwarts')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", secao_hogwarts)
            time.sleep(2)
            
            # Clica no elemento para abrir a página da coleção
            secao_hogwarts.click()
            print("✅ Clicado em Shop Hogwarts com sucesso!")
        except Exception as e:
            print("Aviso: Clique direto falhou, acessando a URL da coleção diretamente...")
            driver.get("https://harrypottershop.co.uk/collections/hogwarts-christmas")
            
        print("Aguardando o carregamento da página de Natal de Hogwarts...")
        time.sleep(5)
        
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)

        print("Rastreando produtos e preços da coleção...")
        cards = driver.find_elements(
            By.XPATH, 
            "//li[contains(@class, 'grid__item')] | //div[contains(@class, 'card-wrapper')] | //div[contains(@class, 'product-card')] | //div[contains(@class, 'card')]"
        )
        
        if not cards:
            cards = driver.find_elements(By.XPATH, "//a[contains(@href, '/products/')]")

        lista_produtos = []
        
        for card in cards:
            texto_completo = card.text.strip().split('\n')
            
            if len(texto_completo) >= 1:
                titulo = texto_completo[0].strip()
                
                preco = "Preço não disponível"
                for linha in texto_completo:
                    if "$" in linha or "USD" in linha or "£" in linha or "R$" in linha or "€" in linha:
                        preco = linha.strip()
                        break
                
                if titulo and len(titulo) > 3 and "collection" not in titulo.lower() and "t&c" not in titulo.lower():
                    if not any(p['titulo'] == titulo for p in lista_produtos):
                        lista_produtos.append({
                            "titulo": titulo,
                            "Preço": preco
                        })


        print("\n" + "="*50)
        print(f" QUANTIDADE TOTAL DE PRODUTOS COLETADOS: {len(lista_produtos)}")
        print("="*50)
        
        for i, produto in enumerate(lista_produtos, 1):
            print(f"{i}. Título: {produto['titulo']} | Preço: {produto['Preço']}")
            
    except Exception as e:
        print(f"Ocorreu um erro durante a execução do bot: {e}")
        
    finally:
        driver.quit()
        print("\nNavegador fechado com sucesso.")

if __name__ == "__main__":  
    main()
