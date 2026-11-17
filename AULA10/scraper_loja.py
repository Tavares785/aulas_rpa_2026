"""
Lab 10 - Extração de Dados da Web em Escala com BeautifulSoup
Aluno: Icaro Ferrari de Senço - RA 1926102

Raspa o catálogo da casa Grifinória na loja oficial do Harry Potter
(Shopify), extraindo nome e preço de cada produto.

Saídas:
- Os 5 primeiros produtos no terminal.
- A lista completa em produtos_gryffindor.csv (colunas: nome, preco).
"""

import csv
import re
import time
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://harrypottershop.co.uk"
URL_CATALOGO = BASE_URL + "/collections/gryffindor"
ARQUIVO_CSV = "produtos_gryffindor.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9,pt-BR;q=0.8",
}
TIMEOUT = 15
TENTATIVAS = 4
ESPERA_429 = 10  # segundos (multiplicado a cada tentativa)
PAUSA_ENTRE_PAGINAS = 3  # segundos - scraping educado
MAX_PAGINAS = 10  # trava de segurança


def limpar_texto(texto):
    """Remove quebras de linha e espaços repetidos."""
    if not texto:
        return ""
    return re.sub(r"\s+", " ", texto).strip()


def pode_raspar(sessao, url):
    """Consulta o robots.txt (com o mesmo User-Agent) antes de acessar a página."""
    robots = RobotFileParser()
    try:
        resposta = sessao.get(urljoin(BASE_URL, "/robots.txt"), timeout=TIMEOUT)
        resposta.raise_for_status()
        robots.parse(resposta.text.splitlines())
    except requests.RequestException as erro:
        print(f"[AVISO] Não foi possível ler o robots.txt ({erro}). Seguindo com cautela.")
        return True
    return robots.can_fetch(HEADERS["User-Agent"], url)


def baixar_pagina(sessao, url):
    """Faz o GET e valida o status 200. Em caso de 429, espera e tenta de novo."""
    for tentativa in range(1, TENTATIVAS + 1):
        resposta = sessao.get(url, timeout=TIMEOUT)
        if resposta.status_code == 200:
            print(f"[OK] {url} -> 200 OK")
            return resposta.text

        if resposta.status_code == 429 and tentativa < TENTATIVAS:
            retry_after = resposta.headers.get("Retry-After", "")
            espera = int(retry_after) if retry_after.isdigit() else ESPERA_429 * tentativa
            print(f"[429] Muitas requisições. Aguardando {espera}s (tentativa {tentativa}/{TENTATIVAS})...")
            time.sleep(espera)
            continue

        raise RuntimeError(f"Falha na requisição: {url} -> HTTP {resposta.status_code}")
    raise RuntimeError(f"Falha na requisição: {url}")


def extrair_preco(card):
    """Retorna o preço efetivo: o de promoção, se existir; senão o regular."""
    preco_sale = card.select_one(".price-item--sale")
    if preco_sale and limpar_texto(preco_sale.get_text()):
        return limpar_texto(preco_sale.get_text())

    preco_regular = card.select_one(".price-item--regular")
    if preco_regular:
        return limpar_texto(preco_regular.get_text())
    return ""


def extrair_produtos(html):
    """Lê o HTML e devolve uma lista de dicionários {nome, preco}."""
    soup = BeautifulSoup(html, "html.parser")
    produtos = []
    vistos = set()

    for card in soup.select(".card"):
        titulo = card.select_one(".card__heading")
        if titulo is None:
            continue

        link = titulo.find("a")
        nome = limpar_texto((link or titulo).get_text())
        preco = extrair_preco(card)

        # O tema Shopify pode repetir o título em mais de um bloco do card
        if not nome or nome in vistos:
            continue
        vistos.add(nome)
        produtos.append({"nome": nome, "preco": preco})

    return produtos


def raspar_catalogo(sessao):
    """Percorre as páginas do catálogo (?page=N) até não haver mais produtos."""
    todos = []
    for pagina in range(1, MAX_PAGINAS + 1):
        url = URL_CATALOGO if pagina == 1 else f"{URL_CATALOGO}?page={pagina}"
        produtos = extrair_produtos(baixar_pagina(sessao, url))

        nomes_atuais = {p["nome"] for p in todos}
        novos = [p for p in produtos if p["nome"] not in nomes_atuais]
        if not novos:
            break

        todos.extend(novos)
        print(f"     Página {pagina}: {len(novos)} produtos")
        time.sleep(PAUSA_ENTRE_PAGINAS)
    return todos


def salvar_csv(produtos, caminho=ARQUIVO_CSV):
    with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["nome", "preco"])
        escritor.writeheader()
        escritor.writerows(produtos)


def main():
    sessao = requests.Session()
    sessao.headers.update(HEADERS)

    if not pode_raspar(sessao, URL_CATALOGO):
        print("[BLOQUEADO] O robots.txt não permite raspar esta página.")
        return

    time.sleep(PAUSA_ENTRE_PAGINAS)
    try:
        produtos = raspar_catalogo(sessao)
    except (requests.RequestException, RuntimeError) as erro:
        print(f"[ERRO] {erro}")
        return

    if not produtos:
        print("[AVISO] Nenhum produto encontrado. Confira os seletores no DevTools (F12).")
        return

    print("\n=== 5 primeiros produtos ===")
    for i, produto in enumerate(produtos[:5], start=1):
        print(f"{i}. {produto['nome']} - {produto['preco']}")

    salvar_csv(produtos)
    print(f"\nTotal: {len(produtos)} produtos salvos em '{ARQUIVO_CSV}'.")


if __name__ == "__main__":
    main()
