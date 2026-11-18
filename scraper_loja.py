
import csv
import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

cabecalho = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

resposta = requests.get(url, headers=cabecalho, timeout=20)
resposta.encoding = "utf-8"

soup = BeautifulSoup(resposta.text, "html.parser")
produtos = soup.select("article.product_pod")

lista_produtos = []

# Coletar todos os produtos
for produto in produtos:
    nome = produto.select_one("h3 a")["title"]
    preco = produto.select_one(".price_color").get_text(strip=True)

    lista_produtos.append({
        "nome": nome,
        "preco": preco
    })

# Exibir somente os 5 primeiros
for produto in lista_produtos[:5]:
    print("Nome:", produto["nome"])
    print("Preço:", produto["preco"])
    print("--------------------")

print("Quantidade de produtos encontrados:", len(produtos))
print("Status da requisição:", resposta.status_code)
print("Tamanho do HTML:", len(resposta.text))

# Exportar todos os produtos para CSV
with open("produtos.csv", "w", newline="", encoding="utf-8-sig") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=["nome", "preco"])
    escritor.writeheader()
    escritor.writerows(lista_produtos)

print("Arquivo CSV salvo com sucesso!")