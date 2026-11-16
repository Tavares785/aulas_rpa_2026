"""
Lab 10 - Extração de Dados da Web com BeautifulSoup
Script: scraper_loja.py

Objetivo: raspar nome e preço dos produtos da coleção Grifinória da loja
oficial do Harry Potter (Shopify) usando requests + BeautifulSoup.

Requer: pip install requests beautifulsoup4
"""
import csv
import re
from typing import Any

# Guard de ImportError: o módulo ainda carrega sem as libs externas,
# encerrando de forma graciosa (exit 0) em ambientes sem internet.
try:
    import requests
    from bs4 import BeautifulSoup

    LIBS_DISPONIVEIS = True
except ImportError:
    requests = None       # type: ignore[assignment]
    BeautifulSoup = None  # type: ignore[assignment]
    LIBS_DISPONIVEIS = False
    print("Bibliotecas ausentes. Instale com: pip install requests beautifulsoup4")

URL_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_SAIDA = "produtos_gryffindor.csv"
COLUNAS = ["nome", "preco"]

# User-Agent de navegador real — boa prática para evitar bloqueios simples.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def limpar_texto(texto: str) -> str:
    """Remove espaços extras e quebras de linha do texto extraído."""
    return re.sub(r"\s+", " ", texto).strip()


def coletar_produtos(url: str) -> list[dict[str, str]]:
    """Faz a requisição HTTP GET e extrai nome e preço de cada produto.

    Seletores utilizados (tema Shopify padrão):
    - `.card__heading`  → título do produto (dentro de um <a>)
    - `.card-wrapper`   → container pai que agrupa título + preço
    - `.price-item--sale`     → preço promocional (prioridade)
    - `.price-item--regular`  → preço regular (fallback)
    - `.price-item`           → qualquer elemento de preço (último recurso)
    """
    resposta = requests.get(url, headers=HEADERS, timeout=15)

    # Valida se a resposta foi 200 OK; lança exceção clara caso contrário.
    resposta.raise_for_status()
    print(f"✅ Resposta do servidor: {resposta.status_code} OK")

    soup = BeautifulSoup(resposta.text, "html.parser")

    produtos: list[dict[str, str]] = []
    vistos: set[str] = set()

    # Itera sobre cada título de produto encontrado no DOM.
    for titulo in soup.select(".card__heading"):
        nome = limpar_texto(titulo.get_text())
        if not nome or nome in vistos:
            continue  # ignora elementos vazios ou duplicados
        vistos.add(nome)

        # Sobe até o container do card para localizar o preço do mesmo item.
        card = titulo.find_parent(class_="card-wrapper") or titulo.parent

        elemento_preco = (
            card.select_one(".price-item--sale")
            or card.select_one(".price-item--regular")
            or card.select_one(".price-item")
        )
        preco = limpar_texto(elemento_preco.get_text()) if elemento_preco else "N/D"

        produtos.append({"nome": nome, "preco": preco})

    return produtos


def salvar_csv(registros: list[dict[str, Any]], caminho: str) -> None:
    """Grava a lista de produtos em um arquivo CSV."""
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUNAS)
        writer.writeheader()
        writer.writerows(registros)


def executar() -> None:
    """Orquestra a raspagem, a exibição e a exportação dos dados."""
    try:
        produtos = coletar_produtos(URL_CATALOGO)
    except Exception as erro:  # noqa: BLE001
        print("Não foi possível acessar o catálogo online agora.")
        print(f"Detalhe técnico: {erro}")
        print("Execução encerrada sem erro (sem internet é um caso esperado).")
        raise SystemExit(0)

    if not produtos:
        print("Nenhum produto encontrado. Verifique os seletores CSS.")
        raise SystemExit(0)

    # Exibe os 5 primeiros produtos no terminal.
    print("\n--- 5 primeiros produtos ---")
    for p in produtos[:5]:
        print(f"  {p['nome']}  |  {p['preco']}")

    # Salva a lista completa em CSV.
    salvar_csv(produtos, ARQUIVO_SAIDA)
    print(f"\n✅ {len(produtos)} produtos salvos em '{ARQUIVO_SAIDA}'")


if __name__ == "__main__":
    if not LIBS_DISPONIVEIS:
        raise SystemExit(0)
    executar()
