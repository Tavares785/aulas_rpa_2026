"""
Lab 08 - Web scraping com Selenium na loja do Harry Potter.

O robo abre o Chrome na pagina de login do site oficial, depois navega ate a
colecao de presentes abaixo de US$ 10 e coleta titulo e preco de cada produto
numa lista de dicionarios. No final mostra tudo no terminal com o total.

O Selenium 4.6+ baixa o driver do Chrome sozinho (Selenium Manager).

Instalar: pip install selenium
Rodar:    python AULA08/bot_products_harry.py
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_COLECAO = "https://harrypottershop.com/collections/gifts/Under-$10"

ESPERA_IMPLICITA = 5
ESPERA_PRODUTOS = 20

# A loja e Shopify: cada produto da listagem fica num "card". Deixamos mais de
# um seletor porque o tema pode variar; vale o primeiro que encontrar algo.
SELETORES_CARD = [
    (By.CSS_SELECTOR, "div.card-wrapper"),
    (By.CSS_SELECTOR, ".product-card"),
    (By.XPATH, "//li[contains(@class, 'grid__item')]"),
]
SELETORES_TITULO = [
    (By.CSS_SELECTOR, ".card__heading a"),
    (By.CSS_SELECTOR, ".card__heading"),
    (By.CSS_SELECTOR, ".product-card__title"),
]
SELETORES_PRECO = [
    (By.CSS_SELECTOR, ".price__sale .price-item--sale"),
    (By.CSS_SELECTOR, ".price__regular .price-item--regular"),
    (By.CSS_SELECTOR, ".price-item"),
    (By.CSS_SELECTOR, ".price"),
]


def criar_navegador():
    """Abre o Chrome maximizado com uma espera implicita curta."""
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--start-maximized")
    navegador = webdriver.Chrome(options=opcoes)
    navegador.implicitly_wait(ESPERA_IMPLICITA)
    return navegador


def primeiro_texto(elemento, seletores):
    """Devolve o primeiro texto nao vazio encontrado pelos seletores."""
    for por, valor in seletores:
        for achado in elemento.find_elements(por, valor):
            texto = " ".join(achado.text.split())
            if texto:
                return texto
    return ""


def localizar_cards(navegador):
    """Espera os produtos aparecerem (JavaScript) e devolve os cards."""
    for por, valor in SELETORES_CARD:
        try:
            WebDriverWait(navegador, ESPERA_PRODUTOS).until(
                EC.presence_of_all_elements_located((por, valor))
            )
        except TimeoutException:
            continue
        cards = navegador.find_elements(por, valor)
        if cards:
            return cards
    return []


def coletar_produtos(navegador):
    """Monta a lista de dicionarios {titulo, Preço} sem repetir produto."""
    produtos = []
    vistos = set()
    for card in localizar_cards(navegador):
        titulo = primeiro_texto(card, SELETORES_TITULO)
        if not titulo or titulo in vistos:
            continue
        vistos.add(titulo)
        preco = primeiro_texto(card, SELETORES_PRECO) or "sem preço"
        produtos.append({"titulo": titulo, "Preço": preco})
    return produtos


def exibir(produtos):
    """Mostra cada produto (titulo + preco) e o total coletado."""
    print("\nProdutos encontrados:")
    for numero, produto in enumerate(produtos, start=1):
        print(f"{numero:2d}. {produto['titulo']} - {produto['Preço']}")
    print(f"\nTotal coletado: {len(produtos)} produtos")


def main():
    navegador = criar_navegador()
    try:
        print(f"Abrindo {URL_LOGIN}")
        navegador.get(URL_LOGIN)
        WebDriverWait(navegador, ESPERA_PRODUTOS).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print(f"Navegando para {URL_COLECAO}")
        navegador.get(URL_COLECAO)
        produtos = coletar_produtos(navegador)
    except WebDriverException as erro:
        print(f"Falha no navegador: {erro.msg}")
        return
    finally:
        navegador.quit()

    if not produtos:
        print("Nenhum produto encontrado. A loja pode ter bloqueado o acesso "
              "(HTTP 429) ou mudado o layout; confira com o DevTools (F12).")
        return
    exibir(produtos)


if __name__ == "__main__":
    main()
