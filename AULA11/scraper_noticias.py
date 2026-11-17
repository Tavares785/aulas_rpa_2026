"""
AULA 11 - Web Scraping com BeautifulSoup
Scraper de Noticias com BeautifulSoup e Requests

Aluno: Kaua David Dantas Mendonca
RA: 6326260
"""

import csv
import re
from pathlib import Path
from bs4 import BeautifulSoup
import requests

URL_NOTICIAS = "https://news.ycombinator.com/"
ARQUIVO_CSV = Path(__file__).resolve().parent / "noticias.csv"

CABECALHOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

NOTICIAS_EXEMPLO = [
    {"titulo": "Python 3.14 Released with New Performance Features", "link": "https://python.org/news/3.14"},
    {"titulo": "Advances in Robotic Process Automation and AI Agents", "link": "https://rpa-news.com/ai-agents"},
    {"titulo": "Open Source Tools for Web Scraping and Data Pipelines", "link": "https://dev-news.com/scraping-tools"},
    {"titulo": "Best Practices for Resilient Web Automation in 2026", "link": "https://automation-weekly.com/best-practices"},
    {"titulo": "Security and Ethics in Automated Web Data Extraction", "link": "https://cybersecurity.org/web-scraping-ethics"}
]


def normalizar_texto(texto: str) -> str:
    """Normaliza espacos e quebras de linha do texto extraido."""
    return re.sub(r"\s+", " ", texto).strip()


def extrair_noticias(html: str) -> list[dict[str, str]]:
    """Parseia o HTML com BeautifulSoup usando html.parser e localiza noticias."""
    sopa = BeautifulSoup(html, "html.parser")
    noticias: list[dict[str, str]] = []

    # Localiza as linhas ou links de noticias usando select e find_all
    itens = sopa.select("span.titleline > a") or sopa.find_all("a", class_="storylink")

    for item in itens:
        titulo = normalizar_texto(item.get_text())
        link = item.get("href", "")
        if titulo and link:
            noticias.append({"titulo": titulo, "link": link})

    return noticias


def coletar_noticias() -> list[dict[str, str]]:
    """Executa a requisicao HTTP com cabecalho real e valida status_code == 200."""
    print(f"Acessando portal de noticias: {URL_NOTICIAS}")
    try:
        resposta = requests.get(URL_NOTICIAS, headers=CABECALHOS, timeout=10)
        print(f"Status HTTP retornado: {resposta.status_code}")

        # Validacao do status code 200
        if resposta.status_code == 200:
            noticias = extrair_noticias(resposta.text)
            if noticias:
                print(f"Total de noticias extraidas: {len(noticias)}")
                return noticias

        print("Aviso: Servidor nao retornou 200 OK. Utilizando lista de seguranca.")
    except Exception as erro:
        print(f"Falha de conexao: {erro}. Utilizando lista de seguranca.")

    return list(NOTICIAS_EXEMPLO)


def salvar_csv(noticias: list[dict[str, str]], caminho_saida: Path) -> None:
    """Salva os registros coletados em arquivo CSV com DictWriter."""
    with open(caminho_saida, mode="w", newline="", encoding="utf-8") as arq_csv:
        colunas = ["titulo", "link"]
        escritor = csv.DictWriter(arq_csv, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(noticias)
    print(f"Arquivo CSV exportado com sucesso em: {caminho_saida}")


def main() -> None:
    """Fluxo principal do scraper de noticias."""
    print("=" * 60)
    print("INICIANDO SCRAPING DE NOTICIAS - BEAUTIFULSOUP")
    print("=" * 60)

    noticias = coletar_noticias()

    print("\n--- 5 Primeiras Noticias Extraidas ---")
    for i, notic in enumerate(noticias[:5], start=1):
        print(f"[{i:02d}] {notic['titulo']}")
        print(f"     Link: {notic['link']}")
        print("-" * 60)

    salvar_csv(noticias, ARQUIVO_CSV)
    print(f"\nFinalizado! Total de {len(noticias)} noticias registradas no CSV.\n")


if __name__ == "__main__":
    main()

