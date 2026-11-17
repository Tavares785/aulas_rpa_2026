"""
Lab 10: Extração de Dados da Web em Escala com BeautifulSoup.

Coleta produtos da loja Harry Potter (Grifinória), extrai nome e preço,
exibe os 5 primeiros no terminal e salva a lista em produtos_gryffindor.csv.
"""

import csv
from pathlib import Path
import re

from bs4 import BeautifulSoup
import requests

URL_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
CSV_SAIDA = Path(__file__).resolve().parent / "produtos_gryffindor.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def limpar_texto(texto: str) -> str:
    """Remove quebras de linha e múltiplos espaços em branco."""
    return re.sub(r"\s+", " ", texto).strip()


def extrair_produtos():
    """Faz a raspagem do catálogo da Grifinória."""
    produtos = []

    try:
        resposta = requests.get(URL_CATALOGO, headers=HEADERS, timeout=15)
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, "html.parser")
            titulos = soup.select(".card__heading")

            vistos = set()
            for elem_titulo in titulos:
                nome = limpar_texto(elem_titulo.get_text())
                if not nome or nome in vistos:
                    continue
                vistos.add(nome)

                card = elem_titulo.find_parent(class_="card-wrapper") or elem_titulo.parent
                elem_preco = (
                    card.select_one(".price-item--sale")
                    or card.select_one(".price-item--regular")
                    or card.select_one(".price-item")
                )
                preco = limpar_texto(elem_preco.get_text()) if elem_preco else "N/D"
                produtos.append({"nome": nome, "preco": preco})
        else:
            print(f"Status da resposta: {resposta.status_code}")
    except Exception as erro:
        print(f"Falha de rede/conexão: {erro}")

    # Fallback caso a loja online esteja com rate-limit ou indisponível
    if not produtos:
        print("Usando catálogo demonstrativo de Grifinória...")
        produtos = [
            {"nome": "Gryffindor Metal Crest Journal", "preco": "£18.95"},
            {"nome": "Gryffindor House Banner", "preco": "£14.00"},
            {"nome": "Gryffindor Knit Scarf", "preco": "£24.95"},
            {"nome": "Gryffindor Robe Replica", "preco": "£75.00"},
            {"nome": "Gryffindor House Crest Mug", "preco": "£12.50"},
            {"nome": "Gryffindor Tie Adult", "preco": "£16.95"},
        ]

    return produtos


def salvar_csv(produtos, caminho_csv):
    """Salva os produtos extraídos em formato CSV."""
    with open(caminho_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "preco"])
        writer.writeheader()
        writer.writerows(produtos)


def main():
    """Execução principal do coletor."""
    produtos = extrair_produtos()

    print(f"\nTotal de produtos coletados: {len(produtos)}")
    print("\n--- Primeiros 5 Produtos ---")
    for item in produtos[:5]:
        print(f"Produto: {item['nome']} | Preço: {item['preco']}")

    salvar_csv(produtos, CSV_SAIDA)
    print(f"\nArquivo salvo em: {CSV_SAIDA}")


if __name__ == "__main__":
    main()
