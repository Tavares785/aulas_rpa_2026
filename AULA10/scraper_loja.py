"""
Lab 10 - Extracao de Dados da Web em Escala com BeautifulSoup

Robo de monitoramento de precos: raspa o catalogo da colecao Gryffindor
da loja oficial do Harry Potter (Shopify), extrai nome e preco de cada
produto, exibe os 5 primeiros no terminal e salva tudo em CSV.

Fluxo em duas etapas (evita o erro 429 - Too Many Requests):
  1. Baixa a pagina HTML UMA vez e salva em pagina_gryffindor.html.
  2. Faz o scraping a partir do arquivo local (sem novas requisicoes).

Se o servidor bloquear o download (429), abra a URL no navegador,
pressione Ctrl+S ("Pagina da Web, somente HTML") e salve como
pagina_gryffindor.html nesta mesma pasta. Depois rode o script de novo.

Requer: pip install requests beautifulsoup4
"""
import csv
import pathlib
import re

import requests
from bs4 import BeautifulSoup

URL_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
PASTA = pathlib.Path(__file__).parent
ARQUIVO_HTML = PASTA / "pagina_gryffindor.html"
ARQUIVO_CSV = PASTA / "produtos_gryffindor.csv"
COLUNAS = ["nome", "preco"]

# User-Agent de navegador real (boa pratica para nao ser bloqueado).
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}


def limpar_texto(texto):
    """Remove espacos extras e quebras de linha do texto extraido."""
    return re.sub(r"\s+", " ", texto).strip()


def baixar_pagina(url):
    """Faz a requisicao HTTP e valida se a resposta foi 200 OK."""
    resposta = requests.get(url, headers=HEADERS, timeout=20)
    if resposta.status_code != 200:
        raise RuntimeError(
            f"Resposta inesperada do servidor: {resposta.status_code} (esperado 200 OK)"
        )
    return resposta.text


def obter_html():
    """Retorna o HTML do catalogo, baixando-o apenas se ainda nao existir.

    - Se pagina_gryffindor.html ja existe, le o arquivo local (nenhuma
      requisicao e feita, entao nao ha risco de 429).
    - Caso contrario, baixa a pagina e salva o HTML em disco.
    """
    if ARQUIVO_HTML.exists():
        print(f"Usando HTML salvo localmente: {ARQUIVO_HTML.name}")
        return ARQUIVO_HTML.read_text(encoding="utf-8", errors="ignore")

    print(f"Baixando: {URL_CATALOGO}")
    html = baixar_pagina(URL_CATALOGO)
    print("Status 200 OK - pagina recebida.")
    ARQUIVO_HTML.write_text(html, encoding="utf-8")
    print(f"HTML salvo em {ARQUIVO_HTML.name}")
    return html


def extrair_preco(card):
    """Retorna o preco efetivo do card (promocao, se houver, ou regular)."""
    elemento = (
        card.select_one(".price-item--sale")
        or card.select_one(".price-item--regular")
        or card.select_one(".price-item")
    )
    return limpar_texto(elemento.get_text()) if elemento else ""


def extrair_produtos(html):
    """Localiza os cards de produto e extrai nome e preco de cada um."""
    sopa = BeautifulSoup(html, "html.parser")
    produtos = []
    vistos = set()

    for card in sopa.select(".card"):
        titulo = card.select_one(".card__heading a") or card.select_one(".card__heading")
        if titulo is None:
            continue
        nome = limpar_texto(titulo.get_text())
        preco = extrair_preco(card)
        # Um mesmo produto pode aparecer em mais de um .card (tema Shopify).
        if not nome or not preco or nome in vistos:
            continue
        vistos.add(nome)
        produtos.append({"nome": nome, "preco": preco})

    return produtos


def salvar_csv(produtos, caminho):
    """Salva a lista completa de produtos em CSV (colunas nome, preco)."""
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(produtos)


def main():
    try:
        html = obter_html()
    except (requests.RequestException, RuntimeError) as erro:
        print(f"Falha ao baixar o catalogo: {erro}")
        print(
            "Abra a URL no navegador, salve com Ctrl+S como "
            f"'{ARQUIVO_HTML.name}' na pasta {PASTA} e rode o script novamente."
        )
        return

    produtos = extrair_produtos(html)

    if not produtos:
        print("Nenhum produto encontrado. Verifique os seletores CSS.")
        return

    print("\nPrimeiros 5 produtos:")
    for i, produto in enumerate(produtos[:5], start=1):
        print(f"{i}. {produto['nome']} - {produto['preco']}")

    salvar_csv(produtos, ARQUIVO_CSV)
    print(f"\n{len(produtos)} produtos salvos em {ARQUIVO_CSV.name}")


if __name__ == "__main__":
    main()
