"""
Lab 10 - Extracao de dados da web com requests + BeautifulSoup.

Robo de monitoramento de precos: le o catalogo da colecao Grifinoria
(Gryffindor) da loja oficial do Harry Potter, pega nome e preco de cada
produto, mostra os 5 primeiros no terminal e grava a lista completa em CSV.

Cuidados eticos aplicados:
- consulta o robots.txt antes de acessar qualquer pagina;
- envia User-Agent de navegador e faz uma pausa entre as paginas;
- se o servidor responder 429 (muitas requisicoes), espera o tempo pedido
  no cabecalho Retry-After antes de tentar de novo, poucas vezes.

Instalar: pip install requests beautifulsoup4
Rodar:    python AULA10/scraper_loja.py
"""
import csv
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

LOJA = "https://harrypottershop.co.uk"
URL_COLECAO = LOJA + "/collections/gryffindor"
ARQUIVO_CSV = Path(__file__).resolve().parent / "produtos_gryffindor.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-GB,en;q=0.9",
}

TIMEOUT_SEGUNDOS = 20
PAUSA_ENTRE_PAGINAS = 2
MAX_TENTATIVAS = 3
ESPERA_MAXIMA_429 = 120
MAX_PAGINAS = 10

# Alguns produtos aparecem na listagem sem preco para a regiao de quem
# acessa (a loja converte a moeda pelo pais do visitante).
PRECO_INDISPONIVEL = "indisponivel"


def normalizar(texto):
    """Troca qualquer sequencia de espacos/quebras de linha por um espaco."""
    return re.sub(r"\s+", " ", texto or "").strip()


def pode_acessar(sessao, url):
    """Le o robots.txt da loja e diz se a URL pode ser raspada."""
    regras = RobotFileParser()
    resposta = sessao.get(LOJA + "/robots.txt", timeout=TIMEOUT_SEGUNDOS)
    if resposta.status_code != 200:
        print(f"robots.txt indisponivel (HTTP {resposta.status_code}); "
              "seguindo com cautela.")
        return True
    regras.parse(resposta.text.splitlines())
    return regras.can_fetch(HEADERS["User-Agent"], url)


def baixar_pagina(sessao, url):
    """Faz o GET e so devolve o HTML se a resposta for 200 OK.

    Em caso de 429, respeita o Retry-After do servidor e tenta de novo.
    """
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        resposta = sessao.get(url, timeout=TIMEOUT_SEGUNDOS)
        if resposta.status_code == 200:
            return resposta.text
        if resposta.status_code != 429 or tentativa == MAX_TENTATIVAS:
            break
        espera = int(resposta.headers.get("Retry-After", "30"))
        espera = min(espera, ESPERA_MAXIMA_429)
        print(f"Servidor pediu calma (HTTP 429). "
              f"Aguardando {espera}s (tentativa {tentativa}).")
        time.sleep(espera)
    raise RuntimeError(f"Resposta inesperada: HTTP {resposta.status_code} "
                       f"em {url}")


def extrair_preco(card):
    """Devolve o preco efetivo do card (promocao, se houver, ou o normal).

    O tema do Shopify deixa blocos de preco vazios escondidos no HTML,
    entao fica valendo o primeiro seletor que tiver texto de verdade.
    """
    if card.find(class_="price--on-sale") is not None:
        candidatos = [".price__sale .price-item--sale", ".price-item--sale"]
    else:
        candidatos = [".price__regular .price-item--regular",
                      ".price-item--regular"]
    candidatos.append(".price-item")
    for seletor in candidatos:
        for elemento in card.select(seletor):
            texto = normalizar(elemento.get_text())
            if texto:
                return texto
    return PRECO_INDISPONIVEL


def extrair_produtos(soup):
    """Percorre os cards da listagem e monta uma lista de dicionarios."""
    produtos = []
    links_vistos = set()
    for card in soup.find_all("div", class_="card-wrapper"):
        titulo = card.select_one(".card__heading a") or card.find(
            class_="card__heading")
        if titulo is None:
            continue
        link = titulo.get("href", "")
        nome = normalizar(titulo.get_text())
        if not nome or link in links_vistos:
            continue
        links_vistos.add(link)
        produtos.append({"nome": nome, "preco": extrair_preco(card)})
    return produtos


def proxima_pagina(soup, url_atual):
    """Acha o link da proxima pagina da colecao, se existir."""
    seta = soup.find("a", attrs={"aria-label": re.compile("next", re.I)})
    if seta is None:
        seta = soup.find("link", rel="next")
    if seta is None or not seta.get("href"):
        return None
    return urljoin(url_atual, seta["href"])


def raspar_colecao(sessao):
    """Raspa todas as paginas da colecao e junta os produtos."""
    todos = []
    url = URL_COLECAO
    for numero in range(1, MAX_PAGINAS + 1):
        html = baixar_pagina(sessao, url)
        soup = BeautifulSoup(html, "html.parser")
        da_pagina = extrair_produtos(soup)
        print(f"Pagina {numero}: {len(da_pagina)} produtos")
        todos.extend(da_pagina)
        url = proxima_pagina(soup, url)
        if url is None:
            break
        time.sleep(PAUSA_ENTRE_PAGINAS)
    return todos


def salvar_csv(produtos, caminho):
    """Grava a lista completa no CSV com as colunas nome e preco."""
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["nome", "preco"])
        escritor.writeheader()
        escritor.writerows(produtos)


def main():
    with requests.Session() as sessao:
        sessao.headers.update(HEADERS)
        if not pode_acessar(sessao, URL_COLECAO):
            print("O robots.txt da loja nao permite acessar a colecao.")
            return 1
        try:
            produtos = raspar_colecao(sessao)
        except (requests.RequestException, RuntimeError) as erro:
            print(f"Falha ao acessar a loja: {erro}")
            return 1

    if not produtos:
        print("Nenhum produto encontrado. Confira os seletores no DevTools.")
        return 1

    print("\nPrimeiros 5 produtos:")
    for posicao, produto in enumerate(produtos[:5], start=1):
        print(f"{posicao}. {produto['nome']} - {produto['preco']}")

    salvar_csv(produtos, ARQUIVO_CSV)
    print(f"\n{len(produtos)} produtos salvos em {ARQUIVO_CSV.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
