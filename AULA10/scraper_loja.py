import csv
import requests
from bs4 import BeautifulSoup

url = "https://harrypottershop.co.uk/collections/gryffindor"

# Cabeçalho que finge ser um navegador de verdade
cabecalho = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

# Pede a página pro servidor
resposta = requests.get(url, headers=cabecalho)

# Só continua se deu 200 OK
if resposta.status_code != 200:
    print("Erro ao acessar a página:", resposta.status_code)
    exit()

# Transforma o HTML num objeto que dá pra pesquisar
sopa = BeautifulSoup(resposta.text, "html.parser")

# Pega todos os cards de produto
cards = sopa.select(".card")

produtos = []

for card in cards:
    # Nome do produto
    tag_nome = card.select_one(".card__heading")
    if tag_nome is None:
        continue
    nome = " ".join(tag_nome.get_text().split())

    # Preço: tenta o de promoção, se vier vazio usa o regular
    preco = ""
    tag_preco = card.select_one(".price-item--sale")
    if tag_preco is not None:
        preco = " ".join(tag_preco.get_text().split())
    if preco == "":
        tag_preco = card.select_one(".price-item--regular")
        if tag_preco is not None:
            preco = " ".join(tag_preco.get_text().split())

    produtos.append([nome, preco])

# Mostra os 5 primeiros
print("Total de produtos:", len(produtos))
for produto in produtos[:5]:
    print(produto[0], "-", produto[1])

# Salva tudo no CSV
arquivo = open("produtos_gryffindor.csv", "w", newline="", encoding="utf-8")
escritor = csv.writer(arquivo)
escritor.writerow(["nome", "preco"])
escritor.writerows(produtos)
arquivo.close()

print("CSV salvo!")
