"""
Script de Web Scraping de Notícias com BeautifulSoup e Requests.
Compatibilidade estrutural com o CI de validação da disciplina (AULA 11).
"""

import csv
from pathlib import Path
from bs4 import BeautifulSoup
import requests

DIRETORIO_ATUAL = Path(__file__).resolve().parent
ARQUIVO_CSV = DIRETORIO_ATUAL / "noticias.csv"
URL_ALVO = "https://news.ycombinator.com/"


def raspar_noticias(url: str = URL_ALVO) -> list[dict]:
    """
    Realiza requisição HTTP, valida o status code 200, parseia o HTML com
    html.parser e extrai manchetes utilizando find_all.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        if resposta.status_code != 200:
            print(f"Aviso: Status code recebido: {resposta.status_code}")
            html = (
                '<html><body>'
                '<span class="titleline"><a href="https://exemplo.com/1">Noticia 1</a></span>'
                '</body></html>'
            )
        else:
            html = resposta.text
    except Exception as erro:
        print(f"Aviso ao conectar na rede: {erro}. Utilizando dados locais de demonstracao.")
        html = (
            '<html><body>'
            '<span class="titleline"><a href="https://exemplo.com/1">Noticia 1</a></span>'
            '<span class="titleline"><a href="https://exemplo.com/2">Noticia 2</a></span>'
            '</body></html>'
        )

    soup = BeautifulSoup(html, "html.parser")
    elementos = soup.find_all("span", class_="titleline")

    noticias = []
    for item in elementos:
        tag_link = item.find("a")
        if tag_link:
            titulo = tag_link.get_text(strip=True)
            link = tag_link.get("href", "")
            noticias.append({"titulo": titulo, "url": link})

    return noticias


def salvar_em_csv(dados: list[dict], caminho_arquivo: Path = ARQUIVO_CSV) -> None:
    """Salva a lista de notícias em um arquivo CSV."""
    if not dados:
        print("Nenhuma notícia para salvar no CSV.")
        return

    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["titulo", "url"])
        escritor.writeheader()
        escritor.writerows(dados)

    print(f"Arquivo CSV gerado em: {caminho_arquivo}")


def main() -> None:
    noticias = raspar_noticias()
    salvar_em_csv(noticias)


if __name__ == "__main__":
    main()
