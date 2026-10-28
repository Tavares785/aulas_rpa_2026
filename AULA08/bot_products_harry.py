import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Credenciais de teste para o login
EMAIL_TESTE = "aluno.teste@harrypotter.com"
SENHA_TESTE = "Hogwarts@2026"


def coletar_produtos_harry_potter():
    # 1. Configurar e instanciar o Selenium WebDriver (webdriver.Edge)
    opcoes = webdriver.EdgeOptions()
    # "eager" faz o Selenium avançar assim que o DOM carrega, sem ficar travado em scripts externos
    opcoes.page_load_strategy = "eager"

    navegador = webdriver.Edge(options=opcoes)
    navegador.maximize_window()

    # Configurar espera implícita e WebDriverWait explícito
    navegador.implicitly_wait(5)
    espera = WebDriverWait(navegador, 15)

    produtos = []

    try:
        # 2. Abrir o navegador no site oficial de login e realizar a ação de logar
        url_login = "https://www.harrypotter.com/pt/login"
        print(f"Abrindo site oficial: {url_login}", flush=True)
        navegador.get(url_login)

        # Aceitar banner de cookies se aparecer na tela de login
        try:
            botao_cookies = WebDriverWait(navegador, 4).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))
            )
            botao_cookies.click()
            time.sleep(1)
        except Exception:
            pass

        # Mapear e preencher os campos de e-mail e senha e clicar em ENTRAR
        print(f"Preenchendo login com e-mail de teste: {EMAIL_TESTE}", flush=True)
        campo_email = espera.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#emailAddress")))
        campo_email.clear()
        campo_email.send_keys(EMAIL_TESTE)

        campo_senha = navegador.find_element(By.CSS_SELECTOR, "#password")
        campo_senha.clear()
        campo_senha.send_keys(SENHA_TESTE)

        botao_entrar = navegador.find_element(By.CSS_SELECTOR, "button[data-testid='loginButton']")
        botao_entrar.click()
        print("Botão ENTRAR clicado! Aguardando resposta...", flush=True)
        time.sleep(3)

        # 3. Navegar até a loja de presentes abaixo de $10
        url_loja = "https://harrypottershop.com/collections/gifts/Under-$10"
        print(f"Navegando para a loja: {url_loja}", flush=True)
        navegador.get(url_loja)

        # Aguardar até que os cards de produto estejam presentes no DOM
        cards_produtos = espera.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card-wrapper"))
        )

        # 4. Extrair Título e Preço de cada produto usando diferentes seletores
        print(f"Coletando dados de {len(cards_produtos)} produtos...", flush=True)
        navegador.implicitly_wait(0)  # Desativa espera implícita dentro do loop para ser instantâneo

        for card in cards_produtos:
            # Extrai o título usando CSS_SELECTOR
            elemento_titulo = card.find_element(By.CSS_SELECTOR, ".card__heading a")
            titulo = (elemento_titulo.text or elemento_titulo.get_attribute("textContent")).strip()

            # Extrai o preço usando XPATH (para promoção) e CSS_SELECTOR (para preço regular)
            if "price--on-sale" in card.get_attribute("innerHTML"):
                elemento_preco = card.find_element(
                    By.XPATH, ".//span[contains(@class, 'price-item--sale')]"
                )
            else:
                elemento_preco = card.find_element(
                    By.CSS_SELECTOR, ".price__regular .price-item--regular"
                )

            preco = (elemento_preco.text or elemento_preco.get_attribute("textContent")).strip()

            produtos.append({
                "titulo": titulo,
                "Preço": preco
            })

    finally:
        navegador.quit()

    # 5. Exibir no terminal todos os produtos encontrados e a quantidade total coletada
    print("\n" + "=" * 60)
    print("PRODUTOS ENCONTRADOS (UNDER $10)")
    print("=" * 60)
    for indice, item in enumerate(produtos, start=1):
        print(f"{indice:02d}. Título: {item['titulo']} | Preço: {item['Preço']}")

    print("=" * 60)
    print(f"Quantidade total coletada: {len(produtos)} produtos")
    print(f"\nEstrutura da lista de dicionários:\n{produtos}")


if __name__ == "__main__":
    coletar_produtos_harry_potter()

