"""
Lab 10 - Web Scraping com BeautifulSoup
RA: 6326012

Raspa o catalogo da Grifinoria na loja do Harry Potter, pega o nome e o
preco de cada produto, mostra os 5 primeiros e salva tudo em CSV.
"""
import csv
import re

import requests
from bs4 import BeautifulSoup

URL = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_CSV = "produtos_gryffindor.csv"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    )
}


def limpar(texto):
    # tira espacos e quebras de linha repetidos
    return re.sub(r"\s+", " ", texto).strip()


def baixar_pagina(url):
    resposta = requests.get(url, headers=HEADERS, timeout=15)
    if resposta.status_code != 200:
        raise Exception(f"Erro ao acessar a pagina: status {resposta.status_code}")
    print("Pagina baixada com sucesso (status 200)")
    return resposta.text


def pegar_preco(card):
    # se o produto estiver em promocao o preco certo e o --sale
    if card.select_one(".price--on-sale"):
        preco = card.select_one(".price-item--sale")
    else:
        preco = card.select_one(".price-item--regular")
    return limpar(preco.get_text()) if preco else ""


def extrair_produtos(html):
    soup = BeautifulSoup(html, "html.parser")
    produtos = []
    for card in soup.select("#product-grid .card__information"):
        titulo = card.select_one(".card__heading")
        if not titulo:
            continue
        produtos.append({
            "nome": limpar(titulo.get_text()),
            "preco": pegar_preco(card),
        })
    return produtos


def salvar_csv(produtos, arquivo):
    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["nome", "preco"])
        escritor.writeheader()
        escritor.writerows(produtos)


def main():
    html = baixar_pagina(URL)
    produtos = extrair_produtos(html)
    print(f"Total de produtos encontrados: {len(produtos)}\n")

    print("5 primeiros produtos:")
    for produto in produtos[:5]:
        print(f"- {produto['nome']} | {produto['preco']}")

    salvar_csv(produtos, ARQUIVO_CSV)
    print(f"\nLista completa salva em {ARQUIVO_CSV}")


if __name__ == "__main__":
    main()
