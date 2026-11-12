import requests as req
import csv
from bs4 import BeautifulSoup as bs
import time
time.sleep(2)

url = "https://harrypottershop.co.uk/collections/gryffindor"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

response = req.get(url, headers=headers)

if response.status_code != 200:
    print(f"Erro na requisição: {response.status_code}")
    exit()

soup = bs(response.text, "html.parser")

# Localiza todos os cards de produto
# .select() é chamado em soup (objeto), não em bs (classe)
cards = soup.select(".card")

produtos = []

for card in cards:
    titulo_tag = card.select_one(".card__heading a")
    nome = titulo_tag.get_text(strip=True) if titulo_tag else "N/A"

    preco_tag = (
        card.select_one(".price-item--sale")
        or card.select_one(".price-item--regular")
    )
    preco = preco_tag.get_text(strip=True) if preco_tag else "N/A"

    if nome != "N/A":
        produtos.append({"nome": nome, "preco": preco})

# Exibe os 5 primeiros
print("=== 5 primeiros produtos ===")
for produto in produtos[:5]:
    print(f"Nome: {produto['nome']} | Preço: {produto['preco']}")

# Salva o CSV completo
with open("AULA10/produtos_gryffindor.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["nome", "preco"])
    writer.writeheader()
    writer.writerows(produtos)

print(f"\nTotal de produtos salvos: {len(produtos)}")
