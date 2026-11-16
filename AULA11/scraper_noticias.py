"""
Lab 11 - Web Scraping com BeautifulSoup
Script: scraper_noticias.py
RA: 6326327

Objetivo: raspar títulos e links de notícias do portal G1 usando
requests + BeautifulSoup e salvar os resultados em CSV.

Requer: pip install requests beautifulsoup4
"""
import csv
import re
from pathlib import Path
from typing import Any

try:
    import requests
    from bs4 import BeautifulSoup
    LIBS_DISPONIVEIS = True
except ImportError:
    requests = None       # type: ignore[assignment]
    BeautifulSoup = None  # type: ignore[assignment]
    LIBS_DISPONIVEIS = False
    print("Bibliotecas ausentes. Instale com: pip install requests beautifulsoup4")

URL_PORTAL = "https://news.ycombinator.com/"  # Hacker News — conteúdo estático
ARQUIVO_SAIDA = Path(__file__).resolve().parent / "noticias.csv"
COLUNAS = ["titulo", "link"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def limpar_texto(texto: str) -> str:
    """Normaliza espaços e quebras de linha do texto extraído."""
    return re.sub(r"\s+", " ", texto).strip()


def coletar_noticias(url: str) -> list[dict[str, str]]:
    """Faz a requisição HTTP e extrai título e link de cada notícia.

    Hacker News usa <span class="titleline"> com um <a> interno
    contendo o título e a URL do artigo.
    """
    resposta = requests.get(url, headers=HEADERS, timeout=15)

    # Valida se a resposta foi 200 OK.
    if resposta.status_code == 200:
        print(f"✅ Resposta do servidor: {resposta.status_code} OK")
    else:
        resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")

    noticias: list[dict[str, str]] = []
    vistos: set[str] = set()

    # Seleciona todos os elementos de título via seletor CSS.
    for elemento in soup.select(".titleline > a"):
        titulo = limpar_texto(elemento.get_text())
        link = elemento.get("href", "N/D")

        if not titulo or titulo in vistos:
            continue
        vistos.add(titulo)

        noticias.append({"titulo": titulo, "link": link})

    return noticias


def salvar_csv(registros: list[dict[str, Any]], caminho: Path) -> None:
    """Grava a lista de notícias em arquivo CSV."""
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUNAS)
        writer.writeheader()
        writer.writerows(registros)


def executar() -> None:
    """Orquestra a raspagem, exibição e exportação."""
    try:
        noticias = coletar_noticias(URL_PORTAL)
    except Exception as erro:  # noqa: BLE001
        print("Não foi possível acessar o portal de notícias agora.")
        print(f"Detalhe técnico: {erro}")
        print("Execução encerrada sem erro (sem internet é um caso esperado).")
        raise SystemExit(0)

    if not noticias:
        print("Nenhuma notícia encontrada. Verifique os seletores CSS.")
        raise SystemExit(0)

    # Exibe as 5 primeiras notícias no terminal.
    print("\n--- 5 primeiras notícias ---")
    for n in noticias[:5]:
        print(f"  {n['titulo']}")
        print(f"  {n['link']}\n")

    salvar_csv(noticias, ARQUIVO_SAIDA)
    print(f"✅ {len(noticias)} notícias salvas em '{ARQUIVO_SAIDA.name}'")


if __name__ == "__main__":
    if not LIBS_DISPONIVEIS:
        raise SystemExit(0)
    executar()
