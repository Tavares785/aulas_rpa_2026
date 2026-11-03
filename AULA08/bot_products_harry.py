import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def criar_driver():
    opcoes = Options()
    opcoes.add_argument("--start-maximized")
    opcoes.add_argument("--disable-blink-features=AutomationControlled")
    opcoes.add_experimental_option("excludeSwitches", ["enable-automation"])
    opcoes.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=opcoes)
    driver.implicitly_wait(10)
    return driver


def obter_produtos_json(driver):
    comando = """
        var callback = arguments[arguments.length - 1];
        fetch('/collections/gifts/Under-$10/products.json')
            .then(function(res) {
                return res.json();
            })
            .then(function(dados) {
                callback(dados.products);
            })
            .catch(function() {
                callback(null);
            });
    """
    return driver.execute_async_script(comando)


def processar_dados_api(produtos_api):
    lista_formatada = []
    for item in produtos_api:
        titulo = item.get("title", "").strip()
        variantes = item.get("variants", [])
        preco = f"${variantes[0].get('price', 'N/A')}" if variantes else "N/A"
        if titulo:
            lista_formatada.append({
                "titulo": titulo,
                "Preço": preco
            })
    return lista_formatada


def raspar_via_dom(driver):
    cards = driver.find_elements(
        By.XPATH,
        "//div[contains(@class, 'product')] | //li[contains(@class, 'product')]"
    )
    itens = []
    titulos = set()
    for card in cards:
        texto = card.text.strip()
        linhas = [linha.strip() for linha in texto.split("\n") if linha.strip()]
        if not linhas or len(linhas[0]) < 3 or linhas[0] in titulos:
            continue
        titulo = linhas[0]
        preco = "N/A"
        for linha in linhas[1:]:
            if any(simb in linha for simb in ["$", "R$", "£"]) or any(c.isdigit() for c in linha):
                preco = linha
                break
        titulos.add(titulo)
        itens.append({"titulo": titulo, "Preço": preco})
    return itens


def extrair_produtos():
    driver = criar_driver()
    driver.implicitly_wait(10)
    url_login = "https://www.harrypotter.com/pt/login"
    url_loja = "https://harrypottershop.com/collections/gifts/Under-$10"
    produtos = []

    try:
        driver.get(url_login)
        time.sleep(2)
        driver.get(url_loja)
        time.sleep(4)

        dados_api = obter_produtos_json(driver)
        if dados_api:
            produtos = processar_dados_api(dados_api)
        else:
            driver.execute_script("window.scrollTo(0, 800);")
            time.sleep(2)
            produtos = raspar_via_dom(driver)
    finally:
        driver.quit()

    return produtos


def main():
    produtos = extrair_produtos()

    print("\n--- PRODUTOS ENCONTRADOS ---")
    for item in produtos:
        print(f"Titulo: {item['titulo']} | Preço: {item['Preço']}")

    print("----------------------------")
    print(f"Quantidade total coletada: {len(produtos)}\n")


if __name__ == "__main__":
    main()
