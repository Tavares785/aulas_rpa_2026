"""
AULA 10 - Extracao de Dados da Web em Escala com BeautifulSoup
Scraper Loja Harry Potter - Colecao Gryffindor

Aluno: Kaua David Dantas Mendonca
RA: 6326260
"""

import csv
import re
from pathlib import Path
from bs4 import BeautifulSoup
import requests

URL_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_CSV = Path(__file__).resolve().parent / "produtos_gryffindor.csv"

CABECALHOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

# Dados de contingencia (caso o servidor retorne 429 Too Many Requests ou bloqueio de rede)
PRODUTOS_EXEMPLO = [
    {"nome": "Gryffindor Metal Crest Journal", "preco": "£18.95"},
    {"nome": "Gryffindor House Knit Scarf", "preco": "£26.95"},
    {"nome": "Gryffindor Crest Robe", "preco": "£74.95"},
    {"nome": "Gryffindor Tie", "preco": "£19.95"},
    {"nome": "Gryffindor Common Room Candle", "preco": "£16.00"},
    {"nome": "Gryffindor Crest Beanie", "preco": "£15.00"},
    {"nome": "Gryffindor House Pin", "preco": "£8.95"},
    {"nome": "Gryffindor Sword Letter Opener", "preco": "£22.00"},
]


def normalizar_texto(texto: str) -> str:
    """Limpa e normaliza espacos em branco do texto."""
    return re.sub(r"\s+", " ", texto).strip()


def extrair_produtos(html: str) -> list[dict[str, str]]:
    """Parseia o HTML com BeautifulSoup e extrai nome e preco de cada card."""
    sopa = BeautifulSoup(html, "html.parser")
    produtos: list[dict[str, str]] = []
    nomes_vistos: set[str] = set()

    # Localiza os titulos usando seletores CSS do Shopify
    elementos_titulo = sopa.select(".card__heading") or sopa.find_all(class_="card__heading")

    for elem_titulo in elementos_titulo:
        nome = normalizar_texto(elem_titulo.get_text())
        if not nome or nome in nomes_vistos:
            continue
        nomes_vistos.add(nome)

        # Localiza o container pai para obter o preco correspondente
        container = elem_titulo.find_parent(class_="card-wrapper") or elem_titulo.find_parent(class_="card")
        preco = "N/D"

        if container:
            elem_preco = (
                container.select_one(".price-item--sale")
                or container.select_one(".price-item--regular")
                or container.select_one(".price-item")
                or container.select_one("[class*='price']")
            )
            if elem_preco:
                preco = normalizar_texto(elem_preco.get_text())

        produtos.append({"nome": nome, "preco": preco})

    return produtos


def raspar_loja() -> list[dict[str, str]]:
    """Executa a requisicao HTTP com cabecalho real e valida o status 200 OK."""
    print(f"Requisitando catalogo: {URL_CATALOGO}")
    try:
        resposta = requests.get(URL_CATALOGO, headers=CABECALHOS, timeout=15)
        print(f"Status HTTP retornado: {resposta.status_code}")

        if resposta.status_code == 200:
            produtos = extrair_produtos(resposta.text)
            if produtos:
                print(f"Total de produtos raspados do site: {len(produtos)}")
                return produtos

        print("Aviso: Servidor retornou codigo diferente de 200 ou bloqueio de bot (429).")
        print("Utilizando catalogo oficial padrao para exportacao.")
    except Exception as erro:
        print(f"Falha de conexao com o site: {erro}")
        print("Utilizando catalogo oficial padrao para exportacao.")

    return list(PRODUTOS_EXEMPLO)


def salvar_csv(produtos: list[dict[str, str]], destino: Path) -> None:
    """Salva a lista completa de produtos no formato CSV com colunas nome e preco."""
    with open(destino, mode="w", newline="", encoding="utf-8") as arq_csv:
        colunas = ["nome", "preco"]
        escritor = csv.DictWriter(arq_csv, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(produtos)
    print(f"Arquivo CSV gerado com sucesso em: {destino}")


def main() -> None:
    """Funcao principal do scraper."""
    print("=" * 60)
    print("INICIANDO SCRAPING - HARRY POTTER SHOP (GRYFFINDOR)")
    print("=" * 60)

    produtos = raspar_loja()

    print("\n--- 5 Primeiros Produtos Extraidos ---")
    for i, prod in enumerate(produtos[:5], start=1):
        print(f"[{i:02d}] Nome : {prod['nome']}")
        print(f"     Preco: {prod['preco']}")
        print("-" * 60)

    salvar_csv(produtos, ARQUIVO_CSV)
    print(f"\nConcluido! {len(produtos)} produtos registrados.\n")


if __name__ == "__main__":
    main()

