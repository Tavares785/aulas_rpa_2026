"""Coleta nomes e preços dos produtos da coleção Grifinória."""

import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ENDERECO_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_SAIDA = Path(__file__).resolve().with_name("produtos_gryffindor.csv")
COLUNAS = ["nome", "preco"]
CABECALHOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def limpar_texto(texto: str) -> str:
    """Normaliza espaços e quebras de linha."""
    return re.sub(r"\s+", " ", texto).strip()


def coletar_produtos(endereco: str = ENDERECO_CATALOGO) -> list[dict[str, str]]:
    """Baixa o catálogo e extrai o nome e o preço de cada produto."""
    resposta = requests.get(endereco, headers=CABECALHOS, timeout=15)
    if resposta.status_code != 200:
        raise requests.HTTPError(
            f"Esperada resposta HTTP 200, recebida {resposta.status_code}.",
            response=resposta,
        )
    sopa = BeautifulSoup(resposta.text, "html.parser")

    produtos = []
    for cartao in sopa.select(".card"):
        titulo = cartao.select_one(".card__heading")
        preco = (
            cartao.select_one(".price-item--sale")
            or cartao.select_one(".price-item--regular")
            or cartao.select_one(".price-item")
        )
        if titulo is None or preco is None:
            raise ValueError("Card de produto sem nome ou preço.")

        produtos.append(
            {
                "nome": limpar_texto(titulo.get_text(" ", strip=True)),
                "preco": limpar_texto(preco.get_text(" ", strip=True)),
            }
        )

    if not produtos:
        raise ValueError("Nenhum produto foi encontrado no catálogo.")

    return produtos


def salvar_csv(produtos: list[dict[str, str]], caminho: Path = ARQUIVO_SAIDA) -> None:
    """Salva todos os produtos em CSV com as colunas exigidas."""
    with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(produtos)


def executar() -> None:
    """Coleta, exibe os cinco primeiros produtos e exporta o catálogo."""
    produtos = coletar_produtos()
    for produto in produtos[:5]:
        print(f"{produto['nome']} | {produto['preco']}")

    salvar_csv(produtos)
    print(f"{len(produtos)} produtos salvos em {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    executar()
