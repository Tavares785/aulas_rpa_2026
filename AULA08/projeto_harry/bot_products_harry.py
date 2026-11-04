import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Inicia o navegador Firefox (o Selenium baixa o geckodriver sozinho)
print("Iniciando o navegador Firefox...")
driver = webdriver.Firefox()

# Configura uma espera implícita padrão de 10 segundos
driver.implicitly_wait(10)

try:
    # 2. Abre o primeiro site exigido no enunciado
    print("Acessando a página de login do Harry Potter...")
    driver.get("https://www.harrypotter.com/pt/login")
    time.sleep(10)  # Pausa rápida para visualizar a página aberta

    # 3. Navega até a loja na seção de presentes abaixo de $10
    print("Navegando para a loja Harry Potter Shop (Under $10)...")
    driver.get("https://harrypottershop.com/collections/gifts/Under-$10")
    time.sleep(10)  # Pausa rápida para visualizar a página aberta

    # 4. Espera explícita (WebDriverWait) para garantir que a grade de produtos carregou
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card, .grid__item, li")))
    
    # Rola a página um pouco para baixo para forçar o carregamento via JavaScript
    driver.execute_script("window.scrollTo(0, 800);")
    time.sleep(10)

    # 5. Mapeia os cartões de produtos da vitrine principal
    # Na loja oficial (Shopify), os itens da vitrine ficam dentro da grade de produtos
    blocos_produtos = driver.find_elements(By.CSS_SELECTOR, "#ProductGridContainer li.grid__item, .product-grid li, .product-card")

    lista_produtos = []

    # 6. Percorre cada produto encontrado para extrair Título e Preço
    for bloco in blocos_produtos:
        try:
            # Busca o título e o preço dentro do bloco do produto usando seletores CSS/XPath
            elemento_titulo = bloco.find_element(By.CSS_SELECTOR, ".card__heading, .product-card__title, h3, a[href*='/products/']")
            elemento_preco = bloco.find_element(By.CSS_SELECTOR, ".price-item--regular, .price__regular, .price")

            titulo = elemento_titulo.text.strip()
            preco = elemento_preco.text.strip()

            # Se o texto vier vazio por conta de camadas ocultas de HTML, tenta pegar o conteúdo interno
            if not titulo:
                titulo = elemento_titulo.get_attribute("textContent").strip()
            if not preco:
                preco = elemento_preco.get_attribute("textContent").strip()

            # Limpa quebras de linha caso existam e salva no formato exato do enunciado
            if titulo and preco:
                preco_limpo = " ".join(preco.split())
                titulo_limpo = " ".join(titulo.split())
                
                # Evita duplicatas na lista
                item = {"titulo": titulo_limpo, "Preço": preco_limpo}
                if item not in lista_produtos:
                    lista_produtos.append(item)

        except Exception:
            # Se um bloco específico for apenas um banner vazio, ignora e passa para o próximo
            continue

    # 7. Exibe no terminal todos os produtos encontrados e o total
    print("\n" + "="*50)
    print("PRODUTOS ENCONTRADOS (UNDER $10)")
    print("="*50)
    
    for prod in lista_produtos:
        print(f"Título: {prod['titulo']} | Preço: {prod['Preço']}")

    print("="*50)
    print(f"Quantidade total coletada: {len(lista_produtos)} produtos.")
    print("="*50)

finally:
    # Fecha o navegador ao terminar tudo
    print("Fechando o navegador...")
    driver.quit()
