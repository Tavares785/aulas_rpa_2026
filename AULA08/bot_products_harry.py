import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def executar_bot_harry_potter():
  # Configurações iniciais do Chrome WebDriver
  options = webdriver.ChromeOptions()
  # options.add_argument("--headless") # Descomente esta linha se preferir rodar em segundo plano sem abrir a janela do navegador

  # Instancia o WebDriver do Chrome (o Selenium 4.6+ baixa e gerencia o driver automaticamente)
  driver = webdriver.Chrome(options=options)

  try:
    print("1. Abrindo o navegador Chrome no site oficial...")
    driver.get("https://www.harrypotter.com/pt/login")
    time.sleep(3)  # Pausa breve para estabilização inicial

    print(
        "2. Navegando para a página de produtos:"
        " https://harrypottershop.com/collections/gifts/Under-$10"
    )
    driver.get("https://harrypottershop.com/collections/gifts/Under-$10")

    print(
        "3. Aplicando WebDriverWait para aguardar o carregamento dinâmico via"
        " JavaScript..."
    )
    # Utilizamos o WebDriverWait combinando com expected_conditions para garantir que os elementos carregaram
    wait = WebDriverWait(driver, 15)

    # Aguarda a presença dos elementos principais da grade de produtos da loja
    wait.until(
        EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                ".product-card, .grid__item, .card, div[class*='product'],"
                " article",
            )
        )
    )

    # Rolagem da página (scroll) para garantir o carregamento completo (caso haja lazy load)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(2)

    print("4. Mapeando e extraindo Títulos e Preços dos produtos...")

    # Mapeando os elementos HTML usando diferentes seletores (CSS_SELECTOR e TAG_NAME)
    # Buscamos títulos e preços utilizando classes comuns de plataformas de e-commerce (Shopify)
    titulos_elementos = driver.find_elements(
        By.CSS_SELECTOR,
        ".card__heading, .product-item__title, h3 a, h2 a, .title",
    )
    precos_elementos = driver.find_elements(
        By.CSS_SELECTOR, ".price, .money, .product-item__price, span[class*='price']"
    )

    lista_produtos = []

    # Determinamos o limite seguro para iterar e evitar erros de índice (IndexError)
    quantidade_itens = min(len(titulos_elementos), len(precos_elementos))

    for i in range(quantidade_itens):
      titulo = titulos_elementos[i].text.strip()
      preco = precos_elementos[i].text.strip()

      # Armazenamos na estrutura de dados solicitada (lista de dicionários)
      if titulo and preco:
        produto = {"titulo": titulo, "Preço": preco}
        lista_produtos.append(produto)

    # 5. Exibindo os resultados no terminal
    print("\n" + "=" * 60)
    print(" 🧹 RESULTADOS DO WEB SCRAPING - HARRY POTTER SHOP (UNDER $10)")
    print("=" * 60)

    for idx, produto in enumerate(lista_produtos, 1):
      print(f"{idx}. Título: {produto['titulo']} | Preço: {produto['Preço']}")

    print("=" * 60)
    print(f" Quantidade total coletada: {len(lista_produtos)} produtos.")
    print("=" * 60)

  except Exception as erro:
    print(f"Ocorreu um erro durante a execução do bot: {erro}")

  finally:
    # Garante que o navegador será fechado ao finalizar a execução
    print("\nFechando o navegador...")
    driver.quit()


if __name__ == "__main__":
  executar_bot_harry_potter()