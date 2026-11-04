import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def obter_links_produtos(driver):

    links = driver.find_elements(
        By.CSS_SELECTOR,
        "a[href*='/products/']"
    )

    produtos = {}

    for link in links:
        endereco = link.get_attribute("href")

        if endereco and "/products/" in endereco:
            produtos[endereco] = link

    return produtos


def carregar_produtos(driver, wait):

    print("\nCarregando os produtos da coleção...")

    quantidade_anterior = 0
    tentativas_sem_novos = 0

    while tentativas_sem_novos < 3:

        altura_anterior = driver.execute_script(
            "return document.body.scrollHeight"
        )

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(2)

        altura_atual = driver.execute_script(
            "return document.body.scrollHeight"
        )

        links_produtos = obter_links_produtos(driver)
        quantidade_atual = len(links_produtos)

        print(
            f"Produtos encontrados até agora: "
            f"{quantidade_atual}"
        )

        botoes = driver.find_elements(
            By.XPATH,
            "//button[contains("
            "translate(normalize-space(.),"
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            "'abcdefghijklmnopqrstuvwxyz'),"
            "'load more')]"
            " | //a[contains("
            "translate(normalize-space(.),"
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            "'abcdefghijklmnopqrstuvwxyz'),"
            "'load more')]"
        )

        botao_load_more = None

        for botao in botoes:
            if botao.is_displayed() and botao.is_enabled():
                botao_load_more = botao
                break

        if botao_load_more is not None:
            print("Botão 'Load More' encontrado!")

            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                botao_load_more
            )

            time.sleep(1)

            driver.execute_script(
                "arguments[0].click();",
                botao_load_more
            )

            time.sleep(4)

            novos_links = obter_links_produtos(driver)

            if len(novos_links) > quantidade_atual:
                print("Novos produtos carregados!")
                tentativas_sem_novos = 0
            else:
                tentativas_sem_novos += 1

        elif quantidade_atual > quantidade_anterior:
            tentativas_sem_novos = 0

        else:
            tentativas_sem_novos += 1

        quantidade_anterior = quantidade_atual

        if altura_atual == altura_anterior and botao_load_more is None:
            break

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    print(
        "\nTotal de links de produtos encontrados:",
        len(obter_links_produtos(driver))
    )


def extrair_dados_produto(link):

    card = None

    ancestrais = [
        "./ancestor::li[contains(@class, 'grid__item')][1]",
        "./ancestor::div[contains(@class, 'card-wrapper')][1]",
        "./ancestor::div[contains(@class, 'product-card')][1]"
    ]

    for xpath in ancestrais:
        try:
            elemento = link.find_element(By.XPATH, xpath)

            if elemento:
                card = elemento
                break

        except Exception:
            continue

    if card is None:
        card = link

    seletores_nome = [
        ".card__heading a",
        ".card__heading",
        "h3",
        "h2",
        ".full-unstyled-link",
        "[class*='product-title']"
    ]

    titulo = ""

    for seletor in seletores_nome:
        try:
            elementos = card.find_elements(
                By.CSS_SELECTOR,
                seletor
            )

            for elemento in elementos:
                texto = elemento.text.strip()

                if (
                    texto
                    and len(texto) > 2
                    and texto.lower() not in [
                        "quick shop",
                        "regular price",
                        "on sale",
                        "selling fast"
                    ]
                ):
                    titulo = texto
                    break

            if titulo:
                break

        except Exception:
            continue

    if not titulo:
        titulo = (
            link.get_attribute("aria-label")
            or link.get_attribute("title")
            or link.text.strip()
        )

    titulo = titulo.strip()

    titulo = re.sub(
        r"\s*(On Sale|Selling Fast|New In)\s*$",
        "",
        titulo,
        flags=re.IGNORECASE
    ).strip()

    preco = "Preço não disponível"

    seletores_preco = [
        ".price-item--sale",
        ".price-item--regular",
        ".price__regular .price-item",
        ".price__sale .price-item",
        ".price"
    ]

    for seletor in seletores_preco:
        try:
            elementos = card.find_elements(
                By.CSS_SELECTOR,
                seletor
            )

            for elemento in elementos:
                texto = elemento.text.strip()

                resultado = re.search(
                    r"\$\s*\d+(?:[.,]\d{2})?",
                    texto
                )

                if resultado:
                    preco = resultado.group(0)
                    break

            if preco != "Preço não disponível":
                break

        except Exception:
            continue

    if preco == "Preço não disponível":
        texto_card = card.text

        resultado = re.search(
            r"\$\s*\d+(?:[.,]\d{2})?",
            texto_card
        )

        if resultado:
            preco = resultado.group(0)

    textos_invalidos = [
        "regular price",
        "on sale",
        "selling fast",
        "quick shop",
        "new in",
        "sold out",
        "notify me"
    ]

    if not titulo or titulo.lower() in textos_invalidos:
        return None

    return {
        "titulo": titulo,
        "Preço": preco
    }


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        wait = WebDriverWait(driver, 20)

        print("Abrindo a loja Harry Potter...")

        driver.get(
            "https://harrypottershop.com/"
            "?utm_medium=nav&utm_campaign=HPShop&utm_source=wwd_web"
        )

        time.sleep(5)

        print("Procurando o botão 'Stay in this site'...")

        try:
            botao_ficar = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//*[self::button or self::a]"
                    "[contains(normalize-space(.), 'Stay in this site')]"
                ))
            )

            botao_ficar.click()

            print("Botão 'Stay in this site' clicado!")

            time.sleep(3)

        except Exception:
            print(
                "Aviso: botão de região não encontrado "
                "ou já fechado."
            )

        print("Tentando aceitar cookies...")

        botoes_cookie = [
            "//button[contains(translate(., "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz'), 'accept')]",

            "//button[contains(translate(., "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz'), 'aceitar')]",

            "//button[contains(@id, 'accept')]",

            "//button[contains(@class, 'accept')]",

            "//a[contains(translate(., "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
            "'abcdefghijklmnopqrstuvwxyz'), 'accept')]"
        ]

        for xpath in botoes_cookie:
            try:
                elem_cookie = driver.find_element(
                    By.XPATH,
                    xpath
                )

                if (
                    elem_cookie.is_displayed()
                    and elem_cookie.is_enabled()
                ):
                    elem_cookie.click()

                    print("Cookies aceitos!")

                    time.sleep(2)
                    break

            except Exception:
                continue

        print("Procurando a seção 'Shop Gifts'...")

        elementos_shop_gifts = wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//*[normalize-space()='Shop Gifts']"
            ))
        )

        shop_gifts = None

        for elemento in elementos_shop_gifts:
            if elemento.is_displayed():
                shop_gifts = elemento
                break

        if shop_gifts is None:
            raise Exception(
                "Menu Shop Gifts não está visível."
            )

        ActionChains(driver).move_to_element(
            shop_gifts
        ).perform()

        print("Menu 'Shop Gifts' localizado!")

        time.sleep(2)

        print("Procurando o link 'Gifts Under $10'...")

        xpath_gifts = (
            "//a[contains(@href, '/collections/gifts/Under-')]"
        )

        wait.until(
            lambda d: len(
                d.find_elements(By.XPATH, xpath_gifts)
            ) > 0
        )

        links_gifts = driver.find_elements(
            By.XPATH,
            xpath_gifts
        )

        print("Links encontrados:", len(links_gifts))

        gifts_under_10 = None

        for link in links_gifts:
            endereco = link.get_attribute("href")

            print("Endereço encontrado:", endereco)

            if (
                "Under-$10" in endereco
                and link.is_displayed()
            ):
                gifts_under_10 = link
                break

        if gifts_under_10 is None:
            for link in links_gifts:
                endereco = link.get_attribute("href")

                if "Under-$10" in endereco:
                    gifts_under_10 = link
                    break

        if gifts_under_10 is None:
            raise Exception(
                "Não foi possível encontrar o link "
                "Gifts Under $10."
            )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            gifts_under_10
        )

        time.sleep(1)

        driver.execute_script(
            "arguments[0].click();",
            gifts_under_10
        )

        print("Clicou em 'Gifts Under $10'!")

        wait.until(
            EC.url_contains("/collections/gifts/Under-")
        )

        print("Página acessada com sucesso!")
        print("URL atual:", driver.current_url)

        time.sleep(5)

        carregar_produtos(driver, wait)

        print("\nRastreando produtos e preços da coleção...")

        links_produtos = obter_links_produtos(driver)

        lista_produtos = []

        for link in links_produtos.values():
            try:
                produto = extrair_dados_produto(link)

                if produto is None:
                    continue

                if not any(
                    p["titulo"] == produto["titulo"]
                    for p in lista_produtos
                ):
                    lista_produtos.append(produto)

            except Exception as erro:
                print(
                    "Não foi possível extrair um produto:",
                    erro
                )

        print("\n" + "=" * 55)

        print(
            "QUANTIDADE TOTAL DE PRODUTOS COLETADOS:",
            len(lista_produtos)
        )

        print("=" * 55)

        for i, produto in enumerate(lista_produtos, 1):
            print(
                f"{i}. Título: {produto['titulo']} | "
                f"Preço: {produto['Preço']}"
            )

        print("=" * 55)

    except Exception as e:
        print("\nOcorreu um erro durante a execução do bot:")
        print(type(e).__name__, repr(e))

    finally:
        driver.quit()

        print("\nNavegador fechado com sucesso.")


if __name__ == "__main__":
    main()
