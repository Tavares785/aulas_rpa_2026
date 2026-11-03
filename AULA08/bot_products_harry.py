from selenium import webdriver

from selenium.webdriver.common.by import By

def main():
    navegador = webdriver.Chrome()

    try: 
        navegador.get("https://www.harrypotter.com/pt/login")
        input("Página de login aberta. Pressione Enter para abrir a loja...")
        navegador.get("https://harrypottershop.com/collections/gifts/Under-$10")
        navegador.implicitly_wait(10)

        produtos = navegador.find_elements(
            By.CSS_SELECTOR, "li.grid__item:has(.card__heading a)"
        )
        print(f"Itens com título encontrados: {len(produtos)}")

        lista_produtos = []

        for produto in produtos:
            titulo = produto.find_element(
                By.CSS_SELECTOR, ".card__heading a"
            )

            precos = produto.find_elements(
                By.CSS_SELECTOR, ".price-item"
            )
            preco_atual = "Preço não encontrado"

            for preco in precos:
                if preco.is_displayed() and preco.text.strip():
                    preco_atual = preco.text.strip()

            lista_produtos.append({
                "titulo": titulo.text,
                "preco": preco_atual
            })

        for item in lista_produtos:
            print(f"{item['titulo']} - {item['preco']}")

        print(f"Total coletado: {len(lista_produtos)}")
        print("Título da página:", navegador.title)
        input("Pressione Enter para fechar o navegador...")

    finally:
        navegador.quit()

if __name__ == "__main__":
    main()