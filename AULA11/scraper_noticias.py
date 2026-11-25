"""
Lab 11: Web Scraping com BeautifulSoup.

Coleta notícias/artigos da web via requests, faz o parsing com
BeautifulSoup (html.parser) e exporta os dados estruturados em CSV.
"""

import csv
from pathlib import Path

from bs4 import BeautifulSoup
import requests


def coletar_noticias():
    """Realiza requisição HTTP e extrai títulos e links com BeautifulSoup."""
    url = "https://news.ycombinator.com/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    print(f"Fazendo requisição para: {url}")
    resposta = requests.get(url, headers=headers, timeout=10)

    # Validação do status_code 200
    if resposta.status_code != 200:
        print(f"Erro na requisição: status code {resposta.status_code}")
        return []

    soup = BeautifulSoup(resposta.text, "html.parser")
    elementos = soup.find_all("span", class_="titleline")

    noticias = []
    for item in elementos:
        tag_link = item.find("a")
        if tag_link:
            titulo = tag_link.text.strip()
            link = tag_link.get("href", "").strip()
            noticias.append({"titulo": titulo, "link": link})

    print(f"Total de notícias coletadas: {len(noticias)}")
    print("\n--- Primeiras 5 Notícias ---")
    for noticia in noticias[:5]:
        print(f"Título: {noticia['titulo']}\nLink: {noticia['link']}\n")

    # Salvamento em arquivo CSV
    diretorio_base = Path(__file__).resolve().parent
    caminho_csv = diretorio_base / "noticias.csv"

    with open(caminho_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["titulo", "link"])
        writer.writeheader()
        writer.writerows(noticias)

    print(f"Arquivo CSV salvo em: {caminho_csv}")
    return noticias


if __name__ == "__main__":
    coletar_noticias()
