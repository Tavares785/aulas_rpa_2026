# Lab 08: Web Scraping e Interação com Elementos via Selenium


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)

# ==========================================
# 1. CONFIGURAR E ABRIR O NAVEGADOR
# ==========================================

navegador = webdriver.Chrome()
navegador.maximize_window()

# ==========================================
# 2. ACESSAR O SITE OFICIAL
# ==========================================

navegador.get("https://www.harrypotter.com/pt/login")

print("Acessando o site oficial...")

# ==========================================
# 3. ACESSAR A LOJA
# ==========================================

navegador.get(
    "https://harrypottershop.com/collections/gifts/Under-$10"
)

print("Acessando a loja Harry Potter Shop...")

# ==========================================
# 4. AGUARDAR OS PRODUTOS CARREGAREM
# ==========================================

espera = WebDriverWait(navegador, 25)

try:
    espera.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "li.grid__item")
        )
    )

    # ==========================================
    # 5. CRIAR LISTA DE PRODUTOS
    # ==========================================

    produtos = []

    # Localizar os cartões dos produtos
    cards = navegador.find_elements(
        By.CSS_SELECTOR, "li.grid__item"
    )

    print("\nColetando produtos...\n")

    # ==========================================
    # 6. PERCORRER CADA PRODUTO
    # ==========================================

    for card in cards:

        try:
            # Extrair título
            titulo = card.find_element(
                By.CSS_SELECTOR, ".card__heading a"
            ).text.strip()

            # Extrair preço
            preco = card.find_element(
                By.CSS_SELECTOR, ".price-item"
            ).text.strip()

            # Guardar os dados
            if titulo and preco:
                produtos.append({
                    "titulo": titulo,
                    "preco": preco
                })

        except NoSuchElementException:
            continue

    # ==========================================
    # 7. EXIBIR RESULTADOS
    # ==========================================

    print("=" * 45)
    print("        PRODUTOS HARRY POTTER")
    print("=" * 45)

    for produto in produtos:

        print("Título:", produto["titulo"])
        print("Preço:", produto["preco"])
        print("-" * 45)

    # ==========================================
    # 8. EXIBIR QUANTIDADE TOTAL
    # ==========================================

    print("\nTotal de produtos encontrados:", len(produtos))

    if len(produtos) == 0:
        print("Nenhum produto foi coletado.")
        print("Verifique os seletores HTML utilizados.")

except TimeoutException:
    print("Tempo esgotado: os produtos não carregaram.")

finally:
    # ==========================================
    # 9. FECHAR O NAVEGADOR
    # ==========================================

    navegador.quit()
