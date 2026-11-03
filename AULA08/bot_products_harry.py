
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")


driver = webdriver.Chrome(options=options)


produtos = []

try:
    
    driver.get("https://www.harrypotter.com/pt/login")

    wait = WebDriverWait(driver, 20)

   
    try:
        botao_cookies = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(translate(., 'ACEITAR', 'aceitar'), 'aceitar')]"
            ))
        )

        botao_cookies.click()
        print("Cookies aceitos!")

    except Exception:
        print("Cookies não encontrados ou já resolvidos.")

    
    driver.get(
        "https://harrypottershop.com/collections/gifts/Under-$10"
    )

    
    wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "h4.card__heading"
        ))
    )

    
    titulos = driver.find_elements(
        By.CSS_SELECTOR,
        "h4.card__heading"
    )

    precos = driver.find_elements(
        By.CSS_SELECTOR,
        "div.card__price"
    )

    print("Títulos encontrados:", len(titulos))
    print("Preços encontrados:", len(precos))

    
    for titulo_elemento, preco_elemento in zip(titulos, precos):

        titulo = titulo_elemento.get_attribute("textContent").strip()
        preco = preco_elemento.get_attribute("textContent").strip()

        if titulo and preco:

            produto = {
                "titulo": titulo,
                "Preço": preco
            }

            produtos.append(produto)

    
    print("\n===== PRODUTOS ENCONTRADOS =====\n")

    for produto in produtos:
        print("Título:", produto["titulo"])
        print("Preço:", produto["Preço"])
        print("-" * 40)

    
    print("\nQuantidade total coletada:", len(produtos))

finally:
    
    driver.quit()
