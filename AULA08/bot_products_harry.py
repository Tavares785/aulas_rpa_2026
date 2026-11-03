import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def lidar_com_banner_cookies_onetrust(driver):
    
    print("Aguardando o carregamento do banner de privacidade e cookies do login...")
    try:
        wait = WebDriverWait(driver, 15)
        seletor_aceitar = (
            "//button[@id='onetrust-accept-btn-handler']"
            " | //button[contains(text(), 'Aceitar')]"
            " | //button[contains(text(), 'Accept')]"
        )
        btn_aceitar = wait.until(EC.element_to_be_clickable((By.XPATH, seletor_aceitar)))
        btn_aceitar.click()
        print("[Cookies Login] Banner de cookies aceito!")
        time.sleep(2)
    except Exception:
        print("[Cookies Login] Banner não detectado ou já fechado.")

def limpar_modais_e_cookies_loja(driver):
    
    print("Iniciando monitor assíncrono para neutralizar pop-ups na loja...")
    script_limpeza = """
    
    """
    try:
        driver.execute_script(script_limpeza)
        time.sleep(5)  
    except Exception as e:
        print(f"Aviso ao executar script de limpeza da loja: {e}")

def iniciar_bot():
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)
    produtos_coletados =

    try:
        
        url_login = "https://www.harrypotter.com/pt/login"
        print(f"Abrindo a página de login: {url_login}")
        driver.get(url_login)
        
        # Resolve o banner de privacidade do login inicial
        time.sleep(5)
        lidar_com_banner_cookies_onetrust(driver)

       
        print("Preenchendo as credenciais...")
        driver.implicitly_wait(30)
        
        email = driver.find_element(By.ID, "emailAddress")
        email.send_keys("guleesin@gmail.com")
        
        driver.find_element(By.ID, "password").send_keys("Harry@2026")
        
        
        lidar_com_banner_cookies_onetrust(driver)
        time.sleep(2)
        
        print("Clicando no botão de login...")
        driver.find_element(By.XPATH, '//*[@data-testid="loginButton"]').click()
        print("Login efetuado nativamente.")
        
        
        time.sleep(10)

        
        url_loja = "https://harrypottershop.com/collections/gifts/Under-$10"
        print(f"Redirecionando para a URL da coleção: {url_loja}")
        driver.get(url_loja)
        
        
        print("Aguardando carregamento da página da loja e surgimento dos pop-ups...")
        time.sleep(10)
        
        
        limpar_modais_e_cookies_loja(driver)

        
        print("Aguardando renderização final dos produtos no HTML...")
        wait = WebDriverWait(driver, 25)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'product') or contains(text(), 'Regular price')]")))

      
        produtos_cards = driver.find_elements(By.XPATH, "//li[contains(., 'Regular price')] | //div[contains(@class, 'product-card')]")
        print(f"Elementos válidos detectados: {len(produtos_cards)}. Iniciando a extração dos campos...")

         
        for card in produtos_cards:
            try:
                texto_linhas = card.text.split('\n')
                if not texto_linhas:
                    continue
                    
                titulo_text = texto_linhas[0].strip()
                
                
                if "wishlist" in titulo_text.lower() or not titulo_text:
                    try:
                        titulo_text = card.find_element(By.CSS_SELECTOR, "h3, a[href*='/products/']").text.strip()
                    except Exception:
                        continue

                # Extração limpa do preço fatiando a string no caractere '$'
                preco = ""
                for linha in texto_linhas:
                    if "$" in linha:
                        partes = linha.split('$')
                        if len(partes) > 1:
                            valor_limpo = partes[1].split()
                            preco = f"${valor_limpo[0]}"
                            break

                
                if titulo_text and preco and "wishlist" not in titulo_text.lower():
                    if not any(p['titulo'] == titulo_text for p in produtos_coletados):
                        produtos_coletados.append({
                            "titulo": titulo_text,
                            "Preço": preco
                        })
            except Exception:
                continue

        
        print("\n=== LISTA DE PRODUTOS COLETADOS (UNDER $10) ===")
        for idx, prod in enumerate(produtos_coletados, 1):
            print(f"{idx}. Produto: {prod['titulo']} | Preço: {prod['Preço']}")
            
        print("================================================")
        print(f"Quantidade total coletada com sucesso: {len(produtos_coletados)} produtos.\n")

    except Exception as e:
        print(f"\nOcorreu um erro crítico durante a execução do bot: {e}")
        
    finally:
       
        try:
            driver.execute_script("if(window.popupCleanerId) clearInterval(window.popupCleanerId);")
        except Exception:
            pass
        # Fechamento correto da instância do navegador
        print("Finalizando sessão do WebDriver Chrome...")
        driver.quit()

if __name__ == "__main__":
    iniciar_bot()
