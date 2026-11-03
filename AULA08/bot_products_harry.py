from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.maximize_window()

driver.get("https://www.harrypotter.com/pt/login")

time.sleep(3)

driver.get(
    "https://harrypottershop.com/collections/gifts/Under-$10"
)

time.sleep(8)

# Tenta aceitar cookies
try:
    botoes = driver.find_elements(By.TAG_NAME, "button")

    for botao in botoes:

        texto = botao.text.lower()

        if (
            "accept" in texto
            or "aceitar" in texto
            or "allow" in texto
        ):
            botao.click()
            time.sleep(2)
            break

except:
    pass

# Coleta os produtos sem repetir nomes
imagens = []

nomes_vistos = set()

for imagem in driver.find_elements(
    By.CSS_SELECTOR,
    "img[data-product-url]"
):

    nome = imagem.get_attribute("alt")

    if not nome:
        continue

    if nome in nomes_vistos:
        continue

    nomes_vistos.add(nome)
    imagens.append(imagem)

# Coleta os preços
precos = driver.find_elements(
    By.CSS_SELECTOR,
    ".card-information"
)

lista_produtos = []

quantidade = min(len(imagens), len(precos))

for i in range(quantidade):

    titulo = imagens[i].get_attribute("alt").strip()

    texto_preco = precos[i].text.strip()

    linhas = texto_preco.split("\n")

    preco = ""

    for linha in linhas:

        if "$" in linha:
            preco = linha
            break

    lista_produtos.append(
        {
            "titulo": titulo,
            "preco": preco
        }
    )

print("\nPRODUTOS ENCONTRADOS\n")

for produto in lista_produtos:

    print(f"Título: {produto['titulo']}")
    print(f"Preço: {produto['preco']}")
    print("-" * 40)

print(f"\nQuantidade total: {len(lista_produtos)}")

driver.quit()