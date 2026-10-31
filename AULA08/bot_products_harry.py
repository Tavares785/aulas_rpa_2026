from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
produtos = list()
options = Options()
options.add_argument("--headless=new")  
options.add_argument("--window-size=1920,4000")        
drive = wd.Chrome(options=options)

drive.implicitly_wait(10)

drive.maximize_window()

link = 'https://www.harrypotter.com'

drive.get(link)

botao_aceita = drive.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')

botao_aceita.click()

botao_shop = drive.find_element(By.XPATH,'//*[@id="shop"]/div')

drive.execute_script("arguments[0].click();", botao_shop)
botao_continue = WebDriverWait(drive, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='button-v3' and .//span[text()='CONTINUE']]"))
)
botao_continue.click()

botao_aceita2 = drive.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]')

botao_aceita2.click()

menu_shop_gifts = drive.find_element(By.ID, "HeaderNewMenu-2")

# Força o clique no sumário ignorando a renderização gráfica
drive.execute_script("arguments[0].click();", menu_shop_gifts)


opcao_presente = WebDriverWait(drive, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'Under-%C2%A310')]"))
)

drive.execute_script("arguments[0].click();", opcao_presente)

while True:
    try:
        load_more = WebDriverWait(drive, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(normalize-space(), 'Load More')]"))

        )

        drive.execute_script("arguments[0].scrollIntoView();", load_more)
        time.sleep(1)

        load_more.click()
        time.sleep(3)
    except:
        break

bloco_produtos = drive.find_elements(By.XPATH,'//*[@id="product-grid"]/li')

for bloco in bloco_produtos:
    try:
        # Extrai o título usando a tag <a> e a classe específica
        titulo = bloco.find_element(By.XPATH, ".//p[contains(@class, 'card__heading')]").get_attribute('textContent')
        
        # Extrai o preço usando a estrutura mapeada anteriormente
        preco = bloco.find_element(By.XPATH, ".//span[contains(@class, 'price-item--regular')]").get_attribute('textContent')
        
        produtos.append({
            "titulo": titulo.strip(),
            "Preço": preco.strip()
        })
    except Exception as e:
        # Se um produto estiver sem preço ou título (ex: esgotado), o script ignora e passa para o próximo
        continue

df = pd.DataFrame(produtos)

print(df)
print()
print(f'Total de {len(produtos)} produtos coletados')