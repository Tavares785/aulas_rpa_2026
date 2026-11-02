from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



opcoes = Options()
opcoes.add_argument("--start-maximized")
driver = webdriver.Chrome(options=opcoes)
driver.get("https://www.harrypotter.com/pt/login")
driver.implicitly_wait(3)


# Aceitar os cookies
try:
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    driver.implicitly_wait(3)
except Exception:
    pass

#Encontra o campo de digita o email
email = "tiwega8434@hiringview.com"
driver.find_element(By.ID, "emailAddress").send_keys(email)

# Encontra o campo e digita a senha
senha = "Senha123"
driver.find_element(By.ID, "password").send_keys(senha)

# Encontra o botao de entrar
driver.find_element(By.CLASS_NAME, "Button-module-scss-module__HB5Z3q__content").click()

# Acessando o shop
driver.get("https://harrypottershop.com/collections/gifts/Under-$10")

driver.find_element(By.CLASS_NAME, 'ot-button-order-2').click()
driver.find_element(By.ID, 'ModalClose-redirect-template-2').click()
driver.implicitly_wait(0.5)

# Lista de produtos
lista_li = driver.find_elements(By.CSS_SELECTOR, '#product-grid > li')

produtos = []
for item in lista_li:
    titulo = item.find_element(By.CSS_SELECTOR, ".card__heading a").text
    
    preco = item.find_element(By.CSS_SELECTOR, ".price__regular .price-item").get_attribute("textContent").strip()
    produtos.append({"titulo": titulo, "Preço": preco})


for produto in produtos:
    print(f"{produto['titulo']} - {produto['Preço']}")
print(f"Total de produtos: {len(produtos)}")



