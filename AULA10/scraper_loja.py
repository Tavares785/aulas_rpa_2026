import csv
import re
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup

URL_BASE = "https://harrypottershop.co.uk"
URL_CATALOGO = f"{URL_BASE}/collections/gryffindor"
ARQUIVO_SAIDA = "produtos_gryffindor.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}


def pode_raspar(url: str, user_agent: str = "*") -> bool:
    """Verifica no robots.txt se a URL permite o acesso do robô."""
    rp = RobotFileParser()
    rp.set_url(f"{URL_BASE}/robots.txt")
    try:
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        # Se n ler fudeu, porém de um jeito estiloso
        return True


def limpar_texto(texto: str) -> str:
    """Remove quebras de linha e excesso de espaços em branco."""
    return re.sub(r"\s+", " ", texto).strip()


def extrair_produtos():
    # Checar esse porra
    if not pode_raspar(URL_CATALOGO):
        print("Acesso bloqueado pelo robots.txt da loja.")
        return

    # Requisition com timeout pra n dar merda
    print(f"Acessando {URL_CATALOGO}...")
    resposta = requests.get(URL_CATALOGO, headers=HEADERS, timeout=15)

    # Validação do status 200 OK
    if resposta.status_code != 200:
        print(f"Erro ao acessar a página. Status HTTP: {resposta.status_code}")
        return

    # Parseamento da árvore DOM
    soup = BeautifulSoup(resposta.text, "html.parser")

    # Novo projeto lulatron 3000
    cards = soup.select(".card-wrapper")
    if not cards:
        cards = soup.select(".card")

    produtos = []

    for card in cards:
        # extraction del name
        elemento_nome = card.select_one(".card__heading a") or card.select_one(".card__heading")
        if not elemento_nome:
            continue

        nome = limpar_texto(elemento_nome.get_text())

        # Extração do preço (desgraça de site)
        elemento_preco = (
            card.select_one(".price--on-sale .price-item--sale")
            or card.select_one(".price-item--regular")
            or card.select_one(".price-item")
        )

        preco = limpar_texto(elemento_preco.get_text()) if elemento_preco else "Indisponível"

        # Se vier bagulho duplicado ou vazio eu me mato
        if nome:
            produtos.append({"nome": nome, "preco": preco})

    # Os 5 primeiros resultados do terminal
    print(f"\nTotal de produtos encontrados: {len(produtos)}\n")
    print(" Top 5 Produtos ")
    for i, item in enumerate(produtos[:5], start=1):
        print(f"{i}. {item['nome']} -> {item['preco']}")

    # Exportion pra csv
    with open(ARQUIVO_SAIDA, mode="w", newline="", encoding="utf-8") as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=["nome", "preco"])
        escritor.writeheader()
        escritor.writerows(produtos)

    print(f"\nArquivo '{ARQUIVO_SAIDA}' salvo com sucesso!")


if __name__ == "__main__":
    extrair_produtos()
