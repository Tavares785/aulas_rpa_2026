
import csv
import logging
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


URL = "https://harrypottershop.co.uk/collections/gryffindor"
RA = "6326269"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def verificar_robots(session, url):
    """Verifica se o robots.txt permite acessar a página."""
    robots_url = urljoin(url, "/robots.txt")

    resposta = session.get(
        robots_url,
        headers=HEADERS,
        timeout=20
    )

    if resposta.status_code == 404:
        logging.info("robots.txt não encontrado.")
        return True

    resposta.raise_for_status()

    robots = RobotFileParser()
    robots.set_url(robots_url)
    robots.parse(resposta.text.splitlines())

    permitido = robots.can_fetch(HEADERS["User-Agent"], url)

    if not permitido:
        logging.warning("O robots.txt não permite acessar esta página.")

    return permitido


def limpar_texto(elemento):
    """Remove espaços e quebras de linha desnecessárias."""
    if elemento is None:
        return ""

    return " ".join(elemento.get_text(" ", strip=True).split())


def extrair_produtos(soup):
    """Localiza os cards e extrai nome e preço."""
    produtos = []

    cards = soup.select(".card")

    logging.info("Cards encontrados: %s", len(cards))

    for card in cards:
        titulo = card.select_one(".card__heading")

        preco = (
            card.select_one(".price-item--sale")
            or card.select_one(".price-item--regular")
            or card.select_one(".price-item")
        )

        nome = limpar_texto(titulo)
        valor = limpar_texto(preco)

        if nome and valor:
            produtos.append({
                "nome": nome,
                "preco": valor
            })

    return produtos


def salvar_csv(produtos):
    """Salva todos os produtos em um arquivo CSV."""
    with open(
        "produtos_gryffindor.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:
        campos = ["nome", "preco"]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()
        escritor.writerows(produtos)

    logging.info("Arquivo CSV salvo com sucesso!")


def main():
    logging.info("Iniciando scraper da loja Harry Potter.")

    try:
        with requests.Session() as session:

            if not verificar_robots(session, URL):
                logging.warning("Raspagem cancelada por regra do robots.txt.")
                return

            resposta = session.get(
                URL,
                headers=HEADERS,
                timeout=30
            )

            resposta.raise_for_status()

            assert resposta.status_code == 200

            logging.info("Resposta HTTP: %s OK", resposta.status_code)

            soup = BeautifulSoup(
                resposta.text,
                "html.parser"
            )

            produtos = extrair_produtos(soup)

            if not produtos:
                logging.warning(
                    "Nenhum produto encontrado. "
                    "Verifique os seletores HTML da loja."
                )
                return

            print("\n===== 5 PRIMEIROS PRODUTOS =====")

            for produto in produtos[:5]:
                print(
                    f"Nome: {produto['nome']} | "
                    f"Preço: {produto['preco']}"
                )

            salvar_csv(produtos)

            logging.info(
                "Total de produtos extraídos: %s",
                len(produtos)
            )

    except requests.RequestException:
        logging.exception("Erro na requisição HTTP.")

    except Exception:
        logging.exception("Erro durante a raspagem dos produtos.")


if __name__ == "__main__":
    main()
