import requests
from bs4 import BeautifulSoup
import csv

url = "https://harrypottershop.co.uk/collections/gryffindor"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Erro ao acessar o site: {response.status_code}")
    print("O servidor pode estar aplicando limitação de acesso ou proteção anti-bot.")
    exit()

print("Página carregada com sucesso!")

soup = BeautifulSoup(response.text, "html.parser")

produtos = soup.select(".card")

lista_produtos = []

for produto in produtos:

    nome_tag = produto.select_one(".card__heading")

    preco_tag = (
        produto.select_one(".price-item--sale")
        or produto.select_one(".price-item--regular")
        or produto.select_one(".price-item")
    )

    if nome_tag and preco_tag:

        nome = nome_tag.get_text(strip=True)
        preco = preco_tag.get_text(strip=True)

        lista_produtos.append({
            "nome": nome,
            "preco": preco
        })

print("\nPrimeiros 5 produtos:\n")

for produto in lista_produtos[:5]:
    print(f"{produto['nome']} - {produto['preco']}")

with open(
    "produtos_gryffindor.csv",
    "w",
    newline="",
    encoding="utf-8"
) as arquivo:

    writer = csv.DictWriter(
        arquivo,
        fieldnames=["nome", "preco"]
    )

    writer.writeheader()
    writer.writerows(lista_produtos)

print(
    f"\nCSV salvo com sucesso! "
    f"Total de produtos: {len(lista_produtos)}"
)

print("Status:", response.status_code)

print(response.text[:1000])




#Durante os testes, o servidor da loja respondeu com HTTP 429 (Too Many Requests), impedindo a obtenção do catálogo.
# O código foi implementado conforme o enunciado utilizando requests e BeautifulSoup, 
# mas a extração depende da disponibilidade e permissões do servidor remoto.