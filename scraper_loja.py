import csv
import requests
from bs4 import BeautifulSoup

url = "https://harrypottershop.co.uk"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}

response = requests.get(url, headers=headers, timeout=15)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select(".card-wrapper")
    produtos = []

    for card in cards:
        titulo_el = card.select_one(".card__link")
        preco_el = card.select_one(".card__price")

        if titulo_el and preco_el:
            nome = " ".join(titulo_el.get_text().split())
            preco = " ".join(preco_el.get_text().split())
            if nome and preco:
                produtos.append({"nome": nome, "preco": preco})

    print("Top 5 produtos encontrados:")
    for prod in produtos[:5]:
        print(f"- {prod['nome']} | {prod['preco']}")

    arquivo_csv = "produtos_gryffindor.csv"
    with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["nome", "preco"])
        writer.writeheader()
        writer.writerows(produtos)

    print(f"\nSucesso! {len(produtos)} produtos salvos em '{arquivo_csv}'.")
else:
    print(f"Erro ao acessar a página. Status code: {response.status_code}")
