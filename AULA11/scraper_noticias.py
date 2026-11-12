"""
AULA 11 - Web Scraping com BeautifulSoup
Script de suporte estrutural para testes e validação da suíte.
"""

import csv
from pathlib import Path
import requests
from bs4 import BeautifulSoup

URL = "https://news.ycombinator.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
ARQUIVO_CSV = Path(__file__).resolve().parent / "noticias.csv"


def extrair_noticias():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
    except requests.RequestException as err:
        print(f"Erro na requisição: {err}")
        return []

    if response.status_code != 200:
        print(f"Status inválido: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    elementos = soup.find_all("span", class_="titleline")

    noticias = []
    for item in elementos:
        link = item.find("a")
        if link:
            titulo = link.get_text(strip=True)
            url = link.get("href", "")
            noticias.append({"titulo": titulo, "url": url})

    return noticias


def salvar_em_csv(noticias: list, destino: Path):
    if not noticias:
        return
    with open(destino, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["titulo", "url"])
        writer.writeheader()
        writer.writerows(noticias)


def main():
    noticias = extrair_noticias()
    salvar_em_csv(noticias, ARQUIVO_CSV)


if __name__ == "__main__":
    main()
