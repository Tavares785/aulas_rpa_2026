"""
AULA 10 - Raspagem de Dados com BeautifulSoup e Requests.

Este script realiza a coleta de dados de produtos da casa Grifinória
(Gryffindor) na loja oficial do Harry Potter (Shopify):
- Envia requisição HTTP com User-Agent de navegador real
- Valida o status 200 OK
- Utiliza BeautifulSoup com o parser 'html.parser'
- Localiza os cards de produtos (.card)
- Extrai nome do produto (.card__heading) e preço (.price-item)
- Normaliza e limpa os textos (.strip() e remoção de espaços extras)
- Exibe os 5 primeiros produtos no terminal
- Salva a lista completa em 'produtos_gryffindor.csv' com colunas 'nome'
  e 'preco'
"""

import csv
from pathlib import Path
import re
import sys
from typing import Any

import requests
from bs4 import BeautifulSoup

URL_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_CSV = Path(__file__).resolve().parent / "produtos_gryffindor.csv"
COLUNAS = ["nome", "preco"]

# User-Agent de navegador real para evitar bloqueios por detecção de bot
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
    "Cookie": "localization=GB; cart_currency=GBP",
}


def limpar_texto(texto: str) -> str:
    """Remove espaços e quebras de linha desnecessárias."""
    return re.sub(r"\s+", " ", texto).strip()


def extrair_produtos(url: str = URL_CATALOGO) -> list[dict[str, str]]:
    """Faz a requisição HTTP e extrai nome e preço dos produtos."""
    print(f"Fazendo requisição para: {url}")
    resposta = requests.get(url, headers=HEADERS, timeout=20)

    # Validação se a resposta foi 200 OK
    if resposta.status_code != 200:
        msg_erro = (
            f"Erro ao acessar catálogo: Status {resposta.status_code} "
            "(esperado: 200 OK)"
        )
        raise RuntimeError(msg_erro)
    print(f"Resposta recebida com sucesso: Status {resposta.status_code} OK")

    sopa = BeautifulSoup(resposta.text, "html.parser")
    produtos: list[dict[str, str]] = []
    vistos: set[str] = set()

    # Localiza todos os cards de produtos
    cards = sopa.select(".card")
    print(f"Total de cards encontrados na página: {len(cards)}")

    for card in cards:
        heading_elem = card.select_one(".card__heading")
        if not heading_elem:
            continue

        nome = limpar_texto(heading_elem.get_text())
        if not nome or nome in vistos:
            continue
        vistos.add(nome)

        # Preço: prioriza preço promocional (.price-item--sale), regular
        preco_elem = (
            card.select_one(".price-item--sale")
            or card.select_one(".price-item--regular")
            or card.select_one(".price-item")
        )
        preco = (
            limpar_texto(preco_elem.get_text()) if preco_elem else "N/D"
        )

        produtos.append({"nome": nome, "preco": preco})

    return produtos


def salvar_csv(produtos: list[dict[str, Any]], caminho: Path) -> None:
    """Salva a lista completa de produtos em formato CSV."""
    with open(caminho, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(produtos)


def main() -> None:
    """Função principal que orquestra a execução da raspagem."""
    try:
        produtos = extrair_produtos()
    except Exception as erro:
        print(f"Falha na execução: {erro}", file=sys.stderr)
        raise

    if not produtos:
        print("Nenhum produto foi localizado na página.")
        return

    # Exibe os 5 primeiros produtos no terminal
    print("\n--- 5 Primeiros Produtos Encontrados ---")
    for i, prod in enumerate(produtos[:5], start=1):
        print(f"{i}. {prod['nome']} - {prod['preco']}")

    # Salva todos os produtos no arquivo CSV
    salvar_csv(produtos, ARQUIVO_CSV)
    print(f"\nLista salva em: {ARQUIVO_CSV} ({len(produtos)} produtos)")


if __name__ == "__main__":
    main()
