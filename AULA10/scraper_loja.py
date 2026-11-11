"""
Lab 10 - Extração de Dados da Web em Escala com BeautifulSoup
================================================================
Scraper do catálogo de produtos da casa Grifinória da loja oficial
do Harry Potter (harrypottershop.co.uk), construída em Shopify.

Objetivos:
  - Fazer requisições HTTP seguras com a biblioteca requests.
  - Parsear a árvore DOM do HTML com BeautifulSoup.
  - Navegar e extrair dados via find(), find_all() e seletores CSS.
  - Aplicar princípios éticos de Web Scraping (verificação do robots.txt).

Autor: Lab 10 - Web Scraping
Data: 2026-11-11
"""

import csv
import re
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
URL_COLECAO = "https://harrypottershop.co.uk/collections/gryffindor"
URL_ROBOTS = "https://harrypottershop.co.uk/robots.txt"
ARQUIVO_CSV = "produtos_gryffindor.csv"

# Parâmetro de URL para forçar exibição dos preços em libras (£).
# O Shopify faz geo-detecção por IP e pode exibir em outra moeda (ex: BRL);
# o parâmetro ?currency=GBP garante o preço na moeda base da loja.
URL_REQUISICAO = f"{URL_COLECAO}?currency=GBP"

# User-Agent de navegador real (boa prática para não ser bloqueado)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}


# ---------------------------------------------------------------------------
# Funções utilitárias
# ---------------------------------------------------------------------------
def verificar_robots_txt(url_alvo: str, url_robots: str) -> bool:
    """
    Verifica o robots.txt do site para garantir que a raspagem
    da URL alvo é permitida (princípios éticos de Web Scraping).

    Retorna True se o acesso for permitido, False caso contrário.
    """
    parser = RobotFileParser()
    parser.set_url(url_robots)
    try:
        parser.read()
        permitido = parser.can_fetch(HEADERS["User-Agent"], url_alvo)
        print(f"[robots.txt] Acesso permitido a {url_alvo}: {permitido}")
        return permitido
    except Exception as exc:
        # Se não conseguir ler o robots.txt, avisa mas segue (fallback comum)
        print(f"[robots.txt] Aviso: não foi possível ler o robots.txt ({exc}).")
        print("[robots.txt] Seguindo com cautela...")
        return True


def limpar_texto(texto: str) -> str:
    """
    Limpa o texto extraído: remove espaços extras, quebras de linha
    e tabulações desnecessárias, normalizando para um único espaço.
    """
    if texto is None:
        return ""
    # Substitui sequências de espaços/quebras/tabulações por um único espaço
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def extrair_preco(card) -> str:
    """
    Extrai o preço efetivo de um card de produto.

    Estratégia (conforme estrutura Shopify):
      1. Se houver .price-item--sale, usar o preço promocional (preço efetivo).
      2. Caso contrário, usar .price-item--regular.

    Parâmetros:
      card: elemento BeautifulSoup representando um <li class="grid__item">.

    Retorna:
      String com o preço limpo (ex: "£18.95") ou string vazia se não encontrado.
    """
    # Tenta primeiro o preço de promoção (preço efetivo quando há desconto)
    preco_sale = card.select_one(".price-item--sale")
    if preco_sale:
        return limpar_texto(preco_sale.get_text())

    # Caso não haja promoção, pega o preço regular
    preco_regular = card.select_one(".price-item--regular")
    if preco_regular:
        return limpar_texto(preco_regular.get_text())

    return ""


def extrair_nome(card) -> str:
    """
    Extrai o nome do produto de um card.

    O título fica em um elemento com a classe .card__heading,
    geralmente dentro de um <a> (link do produto).

    Parâmetros:
      card: elemento BeautifulSoup representando um <li class="grid__item">.

    Retorna:
      String com o nome limpo do produto ou string vazia se não encontrado.
    """
    heading = card.select_one(".card__heading")
    if heading is None:
        return ""

    # O nome geralmente está dentro de um <a> dentro do .card__heading
    link = heading.find("a")
    if link:
        return limpar_texto(link.get_text())

    # Fallback: texto direto do heading
    return limpar_texto(heading.get_text())


# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------
def main():
    # ---- 1. Verificação ética: robots.txt ----
    print("=" * 60)
    print("Lab 10 - Web Scraper: Catálogo Grifinória")
    print("=" * 60)

    if not verificar_robots_txt(URL_COLECAO, URL_ROBOTS):
        print("[ERRO] O robots.txt proíbe o acesso a esta página. Abortando.")
        return

    # ---- 2. Requisição HTTP com User-Agent de navegador real ----
    print(f"\n[1] Fazendo requisicao para: {URL_REQUISICAO}")
    try:
        resposta = requests.get(URL_REQUISICAO, headers=HEADERS, timeout=30)
    except requests.RequestException as exc:
        print(f"[ERRO] Falha na requisicao: {exc}")
        return

    # ---- 3. Validação da resposta (200 OK) ----
    print(f"[2] Status code recebido: {resposta.status_code}")
    if resposta.status_code != 200:
        print(f"[ERRO] Resposta não-200 ({resposta.status_code}). Abortando.")
        return
    print("[2] Resposta 200 OK confirmada!")

    # ---- 4. Parsing do HTML com BeautifulSoup (html.parser) ----
    print("\n[3] Parseando HTML com BeautifulSoup (html.parser)...")
    soup = BeautifulSoup(resposta.text, "html.parser")

    # ---- 5. Localização dos cards de produto ----
    # O catálogo está em <ul id="product-grid">, cada produto em <li class="grid__item">
    grade_produtos = soup.select("ul#product-grid > li.grid__item")
    print(f"[4] Produtos encontrados no catálogo: {len(grade_produtos)}")

    if not grade_produtos:
        print("[ERRO] Nenhum produto encontrado. Os seletores podem ter mudado.")
        return

    # ---- 6. Extração de nome e preço para cada produto ----
    produtos = []
    for card in grade_produtos:
        nome = extrair_nome(card)
        preco = extrair_preco(card)

        # Só adiciona produtos que tenham pelo menos o nome
        if nome:
            produtos.append({"nome": nome, "preco": preco})

    print(f"[5] Produtos válidos extraídos: {len(produtos)}")

    # ---- 7. Exibição dos 5 primeiros produtos no terminal ----
    print("\n" + "=" * 60)
    print("PRIMEIROS 5 PRODUTOS:")
    print("=" * 60)
    for i, prod in enumerate(produtos[:5], start=1):
        print(f"  {i}. {prod['nome']} | {prod['preco']}")
    print("=" * 60)

    # ---- 8. Salvando a lista completa em CSV ----
    print(f"\n[6] Salvando lista completa em '{ARQUIVO_CSV}'...")
    with open(ARQUIVO_CSV, "w", newline="", encoding="utf-8") as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=["nome", "preco"])
        escritor.writeheader()
        escritor.writerows(produtos)

    print(f"[6] Arquivo CSV criado com {len(produtos)} produtos!")
    print("\nConcluído com sucesso!")


if __name__ == "__main__":
    main()
