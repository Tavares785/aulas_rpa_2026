from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_PRODUTOS = "https://harrypottershop.com/collections/gifts/Under-$10"


def iniciar_navegador():
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opcoes)
    driver.implicitly_wait(5)  # espera implícita para cada busca de elemento
    return driver


def coletar_produtos(driver):
    produtos = []

    # Espera explícita: aguarda os cards de produto aparecerem (JS)
    espera = WebDriverWait(driver, 15)
    espera.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "#MainContent li.grid__item")))

    cards = driver.find_elements(By.CSS_SELECTOR, "#MainContent li.grid__item")

    for card in cards:
        try:
            # Título: pega o primeiro card__heading com texto visível
            titulos = card.find_elements(By.CSS_SELECTOR, ".card__heading a")
            titulos_visiveis = [t.text.strip() for t in titulos if t.text.strip()]
            titulo = titulos_visiveis[0] if titulos_visiveis else ""

            # Preço: pega o último price-item visível (preço final/promocional)
            precos = card.find_elements(By.CSS_SELECTOR, ".price-item")
            precos_visiveis = [p.text.strip() for p in precos if p.text.strip()]
            preco = precos_visiveis[-1] if precos_visiveis else ""

            if titulo and preco:
                produtos.append({"titulo": titulo, "Preço": preco})
        except Exception:
            continue  # card com problema: pula para o próximo

    return produtos


def main():
    driver = iniciar_navegador()
    try:
        # Passo 3: abrir o site oficial
        driver.get(URL_LOGIN)
        print("Página de login aberta:", driver.title)

        # Passo 5: ir para a página de produtos
        driver.get(URL_PRODUTOS)

        # Exemplo de By.TAG_NAME: título principal da página
        print("Página:", driver.find_element(By.TAG_NAME, "h1").text)

        # Exemplo de By.XPATH: texto com a contagem de produtos
        contador = driver.find_element(By.XPATH, "//*[contains(text(), 'products')]").text
        print("Contador da página:", contador)

        # Passo 6: extrair os produtos
        produtos = coletar_produtos(driver)

        # Passo 7: exibir os resultados
        print("\n=== PRODUTOS ENCONTRADOS ===")
        for i, produto in enumerate(produtos, start=1):
            print(f"{i:02d}. {produto['titulo']} - {produto['Preço']}")
        print(f"\nTotal coletado: {len(produtos)} produtos")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()