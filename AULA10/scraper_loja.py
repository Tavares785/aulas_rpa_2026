import csv
import time
import requests
from bs4 import BeautifulSoup

url_home = "https://harrypottershop.co.uk/"
url_colecao = "https://harrypottershop.co.uk/collections/gryffindor"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-GB,en;q=0.9,pt-BR;q=0.8",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
}

# Usa uma Session para manter os cookies entre as requisições
sessao = requests.Session()

# 1. Visita a página inicial para receber os cookies legítimos da loja
sessao.get(url_home, headers=headers)
time.sleep(3)

# 2. Acessa o catálogo da Grifinória usando os cookies recebidos
resposta = sessao.get(url_colecao, headers=headers)

# 3. Valida se a resposta foi 200 OK
if resposta.status_code == 200:
    soup = BeautifulSoup(resposta.text, "html.parser")
    cards = soup.select(".card")

    produtos = []

    for card in cards:
        # Extrai o nome do produto
        elemento_nome = card.select_one(".card__heading")

        # Extrai o preço (prioriza promocional; se não houver, pega o regular)
        elemento_preco = card.select_one(
            ".price-item--sale"
        ) or card.select_one(".price-item--regular")

        if elemento_nome and elemento_preco:
            # Remove espaços extras e quebras de linha
            nome = " ".join(elemento_nome.get_text().split())
            preco = " ".join(elemento_preco.get_text().split())
            produtos.append({"nome": nome, "preco": preco})

    # 4. Exibe os 5 primeiros produtos no terminal
    print("Top 5 produtos encontrados:\n")
    for item in produtos[:5]:
        print(f"- {item['nome']} | {item['preco']}")

    # 5. Salva a lista completa no arquivo CSV
    arquivo_csv = "produtos_gryffindor.csv"
    with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["nome", "preco"])
        escritor.writeheader()
        escritor.writerows(produtos)

    print(
        f"\nSucesso! {len(produtos)} produtos salvos em '{arquivo_csv}'."
    )

else:
    print(f"Erro ao acessar a página. Status code: {resposta.status_code}")