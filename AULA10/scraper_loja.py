import csv
from bs4 import BeautifulSoup
import pandas as pd
import requests


def executar_scraping():
  url = "https://harrypottershop.co.uk/collections/gryffindor"

  # Cabeçalho User-Agent de um navegador real para evitar bloqueios de segurança
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
          " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      ),
      "Accept-Language": "en-US,en;q=0.9",
  }

  print(f"Fazendo requisição HTTP para: {url}...")

  try:
    response = requests.get(url, headers=headers, timeout=15)

    # Validando se a resposta do servidor foi 200 OK
    if response.status_code != 200:
      print(f"Erro: O servidor retornou o status code {response.status_code}")
      return

    print("Requisição bem-sucedida! Parseando o HTML...")

    # Parseando a árvore DOM com o parser 'html.parser'
    soup = BeautifulSoup(response.text, "html.parser")

    # Localizando os cards de produto da listagem (padrão Shopify / tema padrão)
    # Buscamos pelas classes de card comuns na plataforma
    cards = soup.select(".card, .product-item, .card-wrapper")

    if not cards:
      print(
          "Aviso: Nenhum card padrão foi encontrado diretamente com os"
          " seletores primários. Verifique se a estrutura da página mudou."
      )
      return

    produtos = []

    for card in cards:
      # Extraindo o nome do produto (buscando em elementos de título comuns)
      title_element = card.select_one(
          ".card__heading, .card-information__text, h3 a, a.full-unstyled-link"
      )

      # Extraindo o preço do produto (procurando preço promocional ou regular)
      price_element = card.select_one(
          ".price-item--sale, .price-item--regular, .price-item"
      )

      if title_element and price_element:
        # Limpeza do texto com .strip() e normalização de espaços em branco
        nome = " ".join(title_element.get_text().split())
        preco = " ".join(price_element.get_text().split())

        # Evita duplicatas caso a mesma tag seja capturada mais de uma vez
        produto_dict = {"nome": nome, "preco": preco}
        if produto_dict not in produtos:
          produtos.append(produto_dict)

    if not produtos:
      print("Nenhum produto com nome e preço válidos foi extraído.")
      return

    # Exibindo os 5 primeiros produtos no terminal
    print("\n--- OS 5 PRIMEIROS PRODUTOS ENCONTRADOS ---")
    for i, prod in enumerate(produtos[:5], start=1):
      print(f"{i}. Produto: {prod['nome']} | Preço: {prod['preco']}")

    print(
        f"\nTotal de produtos extraídos com sucesso: {len(produtos)} itens."
    )

    # Salvando a lista completa em um arquivo CSV (produtos_gryffindor.csv)
    nome_arquivo = "produtos_gryffindor.csv"
    df = pd.DataFrame(produtos)
    df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")

    print(f"Lista completa salva com sucesso no arquivo: '{nome_arquivo}'")

  except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro de conexão durante a requisição: {e}")


if __name__ == "__main__":
  executar_scraping()