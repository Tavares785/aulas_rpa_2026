


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import time

URL_LOGIN = "https://www.harrypotter.com/pt/login"
URL_PRODUTOS = (
    "https://harry-potter-unified.myshopify.com/"
    "collections/gifts/Under-%2410"
)


def coletar_produtos():
    produtos = []
    navegador = webdriver.Chrome()
    espera = WebDriverWait(navegador, 30)

    try:
        # Abre a página de login solicitada no laboratório.
        navegador.get(URL_LOGIN)
        print("Página de login aberta:", navegador.current_url)

        # Abre a coleção de presentes.
        navegador.get(URL_PRODUTOS)

        espera.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[href*="/products/"]')
            )
        )
        time.sleep(3)

        print("Página da loja:", navegador.current_url)
        print("Título da página:", navegador.title)

        # Extrai título e preço diretamente dos cartões de produtos.
        dados = navegador.execute_script("""
            const links = Array.from(
                document.querySelectorAll('a[href*="/products/"]')
            );

            const vistos = new Set();

            return links.map(link => {
                const url = link.href;

                if (vistos.has(url)) {
                    return null;
                }
                vistos.add(url);

                const cartao =
                    link.closest('.card-wrapper') ||
                    link.closest('li.grid__item') ||
                    link.closest('.grid__item') ||
                    link.parentElement;

                const tituloElemento = cartao
                    ? cartao.querySelector(
                        '.card__heading a, .card__heading, ' +
                        '.product-card__title, h2, h3, h4'
                    )
                    : null;

                const imagem = cartao
                    ? cartao.querySelector('img')
                    : link.querySelector('img');

                const precoElementos = cartao
                    ? Array.from(cartao.querySelectorAll(
                        '.price__sale .price-item--sale, ' +
                        '.price-item--sale, ' +
                        '.price__regular .price-item--regular, ' +
                        '.price-item--regular, ' +
                        '.price-item'
                    ))
                    : [];

                return {
                    titulo: (
                        tituloElemento?.innerText ||
                        link.innerText ||
                        imagem?.alt ||
                        ''
                    ).trim(),
                    precos: precoElementos
                        .map(el => el.innerText.trim())
                        .filter(Boolean),
                    url: url
                };
            }).filter(Boolean);
        """)

        print("Cartões de produtos encontrados:", len(dados))

        for item in dados:
            titulo = re.sub(r"\\s+", " ", item["titulo"]).strip()

            # Procura um preço nos elementos de preço do cartão.
            preco_encontrado = None

            for texto_preco in item["precos"]:
                valores = re.findall(
                    r"[$£€]\s?\d[\d,]*(?:\.\d{2})?",
                    texto_preco
                )

                if valores:
                    # Se houver preço promocional e preço original,
                    # prefere o primeiro valor encontrado.
                    preco_encontrado = valores[0].strip()
                    break

            if titulo and preco_encontrado:
                produto = {
                    "titulo": titulo,
                    "preco": preco_encontrado,
                    "url": item["url"]
                }

                if not any(
                    p["url"] == produto["url"] for p in produtos
                ):
                    produtos.append(produto)

        # Salva o HTML para ajudar a investigar caso necessário.
        with open(
            "pagina_produtos.html", "w", encoding="utf-8"
        ) as arquivo:
            arquivo.write(navegador.page_source)

        if not produtos:
            print(
                "Não consegui localizar os preços nos cartões. "
                "O HTML foi salvo em pagina_produtos.html."
            )

    except Exception as erro:
        print("Erro durante a coleta:", erro)

    finally:
        navegador.quit()

    return produtos


if __name__ == "__main__":
    lista_produtos = coletar_produtos()

    print("\\n=== PRODUTOS ENCONTRADOS ===")

    for produto in lista_produtos:
        print("Título:", produto["titulo"])
        print("Preço:", produto["preco"])
        print("Link:", produto["url"])
        print("-" * 40)

    print("Quantidade total coletada:", len(lista_produtos))

    with open(
        "produtos_harry.json", "w", encoding="utf-8"
    ) as arquivo:
        json.dump(
            lista_produtos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    print("Arquivo salvo: produtos_harry.json")

