"""
Laboratório 08: Web Scraping e Interação com Elementos via Selenium
Aluno: Vinicius Montagner
RA: 6326020
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configurar_driver():
    """Configura o Chrome WebDriver com parâmetros anti-bloqueio."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def executar_scraping():
    driver = configurar_driver()
    wait = WebDriverWait(driver, 20)
    lista_produtos = []

    try:
        # 1. Página inicial / login
        print("[1/4] A aceder à página inicial de login...")
        driver.get("https://www.harrypotter.com/pt/login")
        time.sleep(3)

        # 2. Navegação para a loja de presentes até $10
        url_alvo = "https://harrypottershop.com/collections/gifts/Under-$10"
        print(f"[2/4] A aceder à coleção: {url_alvo}")
        driver.get(url_alvo)
        time.sleep(4)

        # Tratar banner de cookies caso surja
        try:
            btn_cookie = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'ACCEPT', 'accept'), 'accept') or contains(@id, 'onetrust-accept')]"))
            )
            btn_cookie.click()
            print("  -> Banner de cookies aceite.")
            time.sleep(1)
        except Exception:
            pass

        # 3. Rolagem para ativar carregamento dinâmico
        print("[3/4] A descer a página para carregar produtos...")
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)

        # Seletores abrangentes para apanhar os blocos de produtos
        seletores = [
            "li.grid__item",
            ".product-card",
            ".grid-product",
            "[data-product-card]",
            ".product-item",
            "div.product-information"
        ]

        cards = []
        for seletor in seletores:
            encontrados = driver.find_elements(By.CSS_SELECTOR, seletor)
            if len(encontrados) > 0:
                cards = encontrados
                print(f"  -> Seletor localizado: '{seletor}' com {len(cards)} itens.")
                break

        # 4. Extração de cada produto
        print("[4/4] A extrair dados dos itens...")
        for card in cards:
            titulo = ""
            preco = ""

            # Obtenção do título
            try:
                elem_titulo = card.find_element(By.CSS_SELECTOR, "h3, .card__heading, .product-card__title, .title, a[class*='title']")
                titulo = elem_titulo.text.strip()
            except Exception:
                continue

            # Obtenção do preço
            try:
                elem_preco = card.find_element(By.CSS_SELECTOR, ".price-item, .price, .money, [data-regular-price]")
                preco = elem_preco.text.strip()
            except Exception:
                preco = "Preço sob consulta"

            # Se o título estiver vazio pelo seletor interno, tenta ler o texto direto
            if not titulo and card.text:
                linhas = [l.strip() for l in card.text.split("\n") if l.strip()]
                if linhas:
                    titulo = linhas[0]

            if titulo:
                lista_produtos.append({
                    "titulo": titulo,
                    "Preço": preco
                })

        # 5. Apresentação no terminal
        print("\n" + "=" * 65)
        print(f"{'PRODUTOS ENCONTRADOS':^65}")
        print("=" * 65)

        for i, item in enumerate(lista_produtos, start=1):
            print(f"{i:02d}. Produto : {item['titulo']}")
            print(f"    Preço   : {item['Preço']}")
            print("-" * 65)

        print(f"\nTotal de produtos recolhidos: {len(lista_produtos)}")
        print("=" * 65)

    except Exception as erro:
        print(f"\n[ERRO]: {erro}")

    finally:
        driver.quit()
        print("\nSessão terminada.")

if __name__ == "__main__":
    executar_scraping()