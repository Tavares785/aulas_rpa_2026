"""Coleta nomes e preços do catálogo Grifinória da loja Harry Potter."""

import csv
import re
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

ENDERECO_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_SAIDA = "produtos_gryffindor.csv"
COLUNAS = ["nome", "preco"]
TIMEOUT = 15
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
CABECALHOS = {"User-Agent": USER_AGENT}


def limpar_texto(texto: str) -> str:
    """Normaliza espaços em nomes e preços extraídos do HTML."""
    return re.sub(r"\s+", " ", texto).strip()


def verificar_robots(url: str) -> None:
    """Interrompe a coleta se o robots.txt proibir ou não puder ser consultado."""
    robots_url = urljoin(url, "/robots.txt")
    resposta = requests.get(
        robots_url,
        headers=CABECALHOS,
        timeout=TIMEOUT,
    )
    if resposta.status_code == 404:
        return
    resposta.raise_for_status()

    regras = RobotFileParser()
    regras.parse(resposta.text.splitlines())
    if not regras.can_fetch(USER_AGENT, url):
        raise PermissionError(f"A coleta de {url} não é permitida pelo robots.txt.")


def coletar_produtos(url: str = ENDERECO_CATALOGO) -> list[dict[str, str]]:
    """Consulta o catálogo permitido e extrai os títulos e preços dos cards."""
    verificar_robots(url)

    resposta = requests.get(url, headers=CABECALHOS, timeout=TIMEOUT)
    if resposta.status_code != 200:
        raise requests.HTTPError(
            f"Esperado HTTP 200 para {url}; recebido {resposta.status_code}.",
            response=resposta,
        )
    resposta.raise_for_status()

    sopa = BeautifulSoup(resposta.text, "html.parser")
    produtos = []

    for titulo in sopa.select(".card__heading"):
        nome = limpar_texto(titulo.get_text(" ", strip=True))
        if not nome:
            continue

        cartao = titulo.find_parent(class_="card")
        if cartao is None:
            cartao = titulo.find_parent(class_="card-wrapper")
        if cartao is None:
            cartao = titulo.parent

        elemento_preco = (
            cartao.select_one(".price-item--sale")
            or cartao.select_one(".price-item--regular")
            or cartao.select_one(".price-item")
        )
        preco = (
            limpar_texto(elemento_preco.get_text(" ", strip=True))
            if elemento_preco
            else "N/D"
        )
        produtos.append({"nome": nome, "preco": preco})

    return produtos


def salvar_csv(produtos: list[dict[str, str]], caminho: str = ARQUIVO_SAIDA) -> None:
    """Salva os produtos em CSV UTF-8 com as colunas nome e preco."""
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(produtos)


def executar() -> None:
    """Coleta, exibe os cinco primeiros produtos e grava o catálogo completo."""
    produtos = coletar_produtos()
    for produto in produtos[:5]:
        print(f"{produto['nome']} | {produto['preco']}")

    salvar_csv(produtos)
    print(f"\n{len(produtos)} produtos salvos em {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    executar()
