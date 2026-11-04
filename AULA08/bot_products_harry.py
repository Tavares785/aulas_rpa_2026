from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

drive = webdriver.Chrome()
drive.maximize_window()
drive.implicitly_wait(10)

# passo 3: abre o login
drive.get("https://www.harrypotter.com/pt/login")
sleep(3)

# fecha o banner de cookies (se não aparecer, segue normal)
botoes = drive.find_elements(By.XPATH, "//button[contains(., 'Aceitar') or contains(., 'ACEITAR') or contains(., 'Accept') or contains(., 'Concordo')]")
if len(botoes) > 0:
    drive.execute_script("arguments[0].click();", botoes[0])
    sleep(2)

# login (conta de exemplo do professor)
drive.find_element(By.ID, "emailAddress").send_keys("guleesin@gmail.com")
drive.find_element(By.ID, "password").send_keys("Harry@2026")
botao_login = drive.find_element(By.XPATH, '//*[@data-testid="loginButton"]')
drive.execute_script("arguments[0].click();", botao_login)
sleep(10)

# passo 5: vai pra loja
drive.get("https://harrypottershop.com/collections/gifts/Under-$10")
sleep(5)

# o banner pode aparecer na loja também
botoes = drive.find_elements(By.XPATH, "//button[contains(., 'Accept') or contains(., 'Aceitar') or contains(., 'ACCEPT')]")
if len(botoes) > 0:
    drive.execute_script("arguments[0].click();", botoes[0])
    sleep(2)

# cada <li> com link de produto é um card
cards = drive.find_elements(By.XPATH, "//li[.//a[contains(@href, '/products/')]]")

produtos = []

for card in cards:
    links = card.find_elements(By.XPATH, ".//a[contains(@href, '/products/')]")
    titulo = links[-1].get_attribute("textContent").strip()

    palavras = card.get_attribute("textContent").split()
    preco = ""
    for palavra in palavras:
        if palavra.startswith("$") and preco == "":
            preco = palavra

    produtos.append({"titulo": titulo, "Preço": preco})

# passo 7: mostra tudo e o total
for produto in produtos:
    print(produto["titulo"], "-", produto["Preço"])

print("Total coletado:", len(produtos))

drive.quit()