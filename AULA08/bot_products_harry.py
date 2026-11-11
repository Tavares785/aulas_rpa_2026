import re
import time
 
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
 
URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_COLECAO = "https://harrypottershop.com/collections/gifts/Under-$10"
 
TIMEOUT = 20  # wait time
 
# Prices: $5.00, $ 9,99, US$ 7.50 etc.
REGEX_PRECO = re.compile(r"(?:US)?\$\s?\d+(?:[.,]\d{2})?")
 
 
# Browser settings
def criar_driver() -> webdriver.Chrome:
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--start-maximized")
    opcoes.add_argument("--disable-notifications")
    # Pretty sure this reduces false positives for "selenium detected" popups, but not guaranteed.
    opcoes.add_experimental_option("excludeSwitches", ["enable-automation"])
 
    driver = webdriver.Chrome(options=opcoes)
 
    # max amt of time selenium spnds trying to fnd an elment
    # b4 throwin NoSuchElementException.
    driver.implicitly_wait(3)
    return driver
 
 
def fechar_popups(driver: webdriver.Chrome) -> None:
    # tries clsing popups and da lik tht may blck prdct viewin. Hopeflly without isses if nt fnd.
    candidatos = [
        (By.ID, "onetrust-accept-btn-handler"),
        (By.XPATH, "//button[contains(translate(., 'ACEITAR', 'aceitar'), 'aceitar')]"),
        (By.XPATH, "//button[contains(translate(., 'ACCEPT', 'accept'), 'accept')]"),
        (By.CSS_SELECTOR, "button[aria-label='Close'], button[aria-label='Fechar']"),
    ]
    for by, seletor in candidatos:
        try:
            botao = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((by, seletor)))
            botao.click()
            time.sleep(0.5)
            return
        except (TimeoutException, StaleElementReferenceException):
            continue
 
 
def rolar_pagina(driver: webdriver.Chrome) -> None:
    # Scrolls 2 end of pge to lod prodcts, stppng if no contnt appers after 10 scrlls
    altura_anterior = 0
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        altura_atual = driver.execute_script("return document.body.scrollHeight")
        if altura_atual == altura_anterior:
            break
        altura_anterior = altura_atual
 
 
def texto_do_primeiro(card, seletores: list[tuple[str, str]]) -> str:
    # Tries each selector (By, valor) and returns the first non-empty text.
    for by, valor in seletores:
        try:
            for el in card.find_elements(by, valor):
                texto = el.text.strip() or (el.get_attribute("textContent") or "").strip()
                if texto:
                    return texto
        except (NoSuchElementException, StaleElementReferenceException):
            continue
    return ""
 
 
# Bot steps

def etapa_1_abrir_login(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    print("[1/4] Abrindo página de login do site oficial...")
    driver.get(URL_LOGIN)
    # By.TAG_NAME: waits for <body> to exist, meaning the page has loaded
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    fechar_popups(driver)
    print(f"      Página aberta: {driver.title!r}")
 
 
def etapa_2_abrir_colecao(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
    print("[2/4] Navegando até a coleção 'Gifts under $10'...")
    driver.get(URL_COLECAO)
    #Waits until at least one product link is present (JS may load products asynchronously)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/products/']"))
    )
    fechar_popups(driver)
    rolar_pagina(driver)
 
 
def localizar_cards(driver: webdriver.Chrome) -> list:
    # Locats prodct "cards", tries vrious selctors cuz da stre theme may chng da html
    seletores_css = [
        "li.grid__item",
        "div.product-card",
        "div.grid-product",
        "div.product-item",
        "div[class*='product-card']",
        "li[class*='product']",
    ]
    for css in seletores_css:
        cards = driver.find_elements(By.CSS_SELECTOR, css)
        cards = [c for c in cards if c.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")]
        if cards:
            return cards
 
    # 2) By.XPATH - fallback: goes from the product link 2 closest container (li, div, or article)
    cards = driver.find_elements(
        By.XPATH,
        "//a[contains(@href,'/products/')]/ancestor::*[self::li or self::div or self::article][1]",
    )
    return cards
 
 
def extrair_produto(card) -> dict | None:
    # title and price from a product card, returns None if not found
    titulo = texto_do_primeiro(
        card,
        [
            (By.CSS_SELECTOR, ".card__heading a, .card__heading"),       # By.CSS_SELECTOR
            (By.CSS_SELECTOR, "[class*='title'], [class*='product-name']"),
            (By.XPATH, ".//a[contains(@href,'/products/')][normalize-space(.)!='']"),  # By.XPATH
            (By.TAG_NAME, "h3"),                                           # By.TAG_NAME
            (By.TAG_NAME, "h2"),
        ],
    )
 
    # price
    # Prioritizes sales, if none then regular prices
    preco = texto_do_primeiro(
        card,
        [
            (By.CSS_SELECTOR, ".price-item--sale"),
            (By.CSS_SELECTOR, ".price-item--regular"),
            (By.CSS_SELECTOR, "[class*='price']"),
            (By.XPATH, ".//*[contains(text(),'$')]"),
        ],
    )
 
    # Final fallback
    if not REGEX_PRECO.search(preco or ""):
        achado = REGEX_PRECO.search(card.get_attribute("textContent") or "")
        preco = achado.group(0) if achado else ""
    else:
        preco = REGEX_PRECO.search(preco).group(0)
 
    if not titulo or not preco:
        return None
    return {"titulo": titulo, "Preço": preco}
 
 
def etapa_3_coletar_produtos(driver: webdriver.Chrome, wait: WebDriverWait) -> list[dict]:
    print("[3/4] Extraindo título e preço dos produtos...")
    produtos: list[dict] = []
    vistos: set[tuple[str, str]] = set()
    pagina = 1
 
    while True:
        cards = localizar_cards(driver)
        print(f"      Página {pagina}: {len(cards)} cards encontrados")
 
        for card in cards:
            try:
                item = extrair_produto(card)
            except StaleElementReferenceException:
                continue
            if item is None:
                continue
            chave = (item["titulo"], item["Preço"])
            if chave in vistos:  # avoids duplicates
                continue
            vistos.add(chave)
            produtos.append(item)
 
        # Changes pages (?)
        proximos = driver.find_elements(
            By.CSS_SELECTOR, "a[rel='next'], a[aria-label*='Next'], a[aria-label*='róxima']"
        )
        if not proximos:
            break
        try:
            driver.execute_script("arguments[0].click();", proximos[0])
            pagina += 1
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/products/']"))
            )
            rolar_pagina(driver)
        except (TimeoutException, StaleElementReferenceException):
            break
 
    return produtos
 
 
def etapa_4_exibir(produtos: list[dict]) -> None:
    print("\n[4/4] Resultado da coleta")
    print("=" * 60)
    for i, p in enumerate(produtos, start=1):
        print(f"{i:>3}. {p['titulo']}  ->  {p['Preço']}")
    print("=" * 60)
    print(f"Total de produtos coletados: {len(produtos)}")
 
 
# Main
def main() -> None:
    driver = criar_driver()
    wait = WebDriverWait(driver, TIMEOUT)  # explicit wait 4 elements 2 appear
    try:
        etapa_1_abrir_login(driver, wait)
        etapa_2_abrir_colecao(driver, wait)
        produtos = etapa_3_coletar_produtos(driver, wait)
        etapa_4_exibir(produtos)
    except TimeoutException:
        print("Erro: tempo esgotado esperando a página carregar. Verifique a conexão ou os seletores.")
    finally:
        driver.quit()
 
 
if __name__ == "__main__":
    main()