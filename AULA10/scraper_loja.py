import csv
import re
from urllib import robotparser
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_CSV = Path(__file__).parent / "produtos_gryffindor.csv"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def limpar(texto):
    """Remove espaços extras e quebras de linha."""
    return re.sub(r"\s+", " ", texto).strip()


def pode_raspar(url):
    """Ética: consulta o robots.txt antes de raspar."""
    rp = robotparser.RobotFileParser()
    rp.set_url("https://harrypottershop.co.uk/robots.txt")
    try:
        rp.read()
        return rp.can_fetch(HEADERS["User-Agent"], url)
    except Exception:
        return True  # se não conseguir ler o robots.txt, segue


def extrair_preco(card):
    """Pega o preço do bloco visível (produtos com variações têm blocos .price ocultos)."""
    bloco = card.select_one(".price:not(.hidden)") or card.select_one(".price")
    if bloco is None:
        return ""
    if "price--on-sale" in bloco.get("class", []):
        el = bloco.select_one(".price-item--sale")
    else:
        el = bloco.select_one(".price-item--regular")
    return limpar(el.get_text()) if el else ""


def raspar():
    if not pode_raspar(URL):
        print("robots.txt não permite raspar esta página.")
        return []

    resposta = requests.get(URL, headers=HEADERS, timeout=15)
    if resposta.status_code != 200:
        print(f"Erro: status {resposta.status_code}")
        return []
    print("Resposta 200 OK")

    soup = BeautifulSoup(resposta.text, "html.parser")
    produtos = []
    vistos = set()

    # .card = cards da listagem (não usar .card-wrapper: são recomendações do carrinho)
    for card in soup.select(".card"):
        titulo = card.select_one(".card__heading")
        if titulo is None:
            continue
        nome = limpar(titulo.get_text())
        if not nome or nome in vistos:  # evita duplicados
            continue
        vistos.add(nome)
        produtos.append({"nome": nome, "preco": extrair_preco(card)})

    return produtos


def salvar_csv(produtos):
    with open(ARQUIVO_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "preco"])
        writer.writeheader()
        writer.writerows(produtos)


if __name__ == "__main__":
    produtos = raspar()
    print(f"\nTotal de produtos: {len(produtos)}\n")
    for p in produtos[:5]:
        print(f"{p['nome']} - {p['preco']}")
    salvar_csv(produtos)
    print(f"\nArquivo salvo: {ARQUIVO_CSV}")

