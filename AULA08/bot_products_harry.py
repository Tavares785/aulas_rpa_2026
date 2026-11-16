
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from getpass import getpass
import time

# Abrir o navegador
navegador = webdriver.Chrome()
navegador.maximize_window()

# Acessar o site Harry Potter
navegador.get("https://www.harrypotter.com/pt/login")

# Criar espera de até 20 segundos
espera = WebDriverWait(navegador, 20)

# Aceitar cookies
try:
    botao_cookies = espera.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "ot-button-order-2")
        )
    )

    botao_cookies.click()
    print("Cookies aceitos!")

except TimeoutException:
    print("Aviso de cookies não encontrado ou já fechado.")

# Solicitar e-mail e senha
email = input("Digite seu e-mail: ")
senha = getpass("Digite sua senha: ")

try:
    # Localizar campo de e-mail
    campo_login = espera.until(
        EC.element_to_be_clickable((By.ID, "emailAddress"))
    )

    campo_login.clear()
    campo_login.send_keys(email)

    print("E-mail preenchido!")

    # Localizar campo de senha
    campo_senha = espera.until(
        EC.element_to_be_clickable((By.ID, "password"))
    )

    campo_senha.clear()
    campo_senha.send_keys(senha)

    print("Senha preenchida!")

    # Localizar botão Entrar
    botao_entrar = espera.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-testid="loginButton"]')
        )
    )

    # Clicar no botão Entrar
    botao_entrar.click()

    print("Botão Entrar clicado!")

except TimeoutException:
    print("Não foi possível localizar algum elemento da página.")

# Aguardar para visualizar o resultado
time.sleep(10)

navegador.get("https://harrypottershop.com/collections/gifts/Under-$10")

aceitar = WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable(
        (By.ID, "onetrust-accept-btn-handler")
    )
)

aceitar.click()

fechar = WebDriverWait(navegador, 10).until(
    EC.element_to_be_clickable(
        (By.ID, "ModalClose-redirect-template")
    )
)

fechar.click()

navegador.execute_script("""
    window.scrollTo({
        top: 900,
        behavior: 'smooth'
    });
""")

# Dicionário para armazenar os produtos
produtos = {}

# Aguardar os produtos carregarem
WebDriverWait(navegador, 15).until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "li.grid__item")
    )
)

# Localizar os cards dos produtos
cards = navegador.find_elements(
    By.CSS_SELECTOR, "li.grid__item"
)

# Percorrer os produtos, um por vez
for card in cards:

    if len(produtos) == 5:
        break

    try:
        # Pegar o título e o link
        elemento = card.find_element(
            By.CSS_SELECTOR, ".card__heading a"
        )

        titulo = elemento.text.strip()
        href = elemento.get_attribute("href")

        # Pegar o preço do mesmo produto
        preco = card.find_element(
            By.CSS_SELECTOR, ".price"
        ).text.strip()

        # Salvar os dados no dicionário
        if titulo and preco and href:
            produtos[titulo] = {
                "Título": titulo,
                "Preço": preco,
                "Link": href
            }

    except Exception as erro:
        print("Erro ao coletar produto:", erro)

# ==================================
# EXIBIR OS PRODUTOS NA TELA
# ==================================

print("\n======= LISTA DE PRODUTOS =======")

for numero, (titulo, dados) in enumerate(
    produtos.items(), start=1
):

    print(f"\nProduto {numero}")
    print("Título:", dados["Título"])
    print("Preço:", dados["Preço"])
    print("Link:", dados["Link"])
    print("--------------------------------")

print("\nTotal de produtos coletados:", len(produtos))

# Aguardar para visualizar o resultado
time.sleep(10) 

# Fechar navegador
navegador.quit()
