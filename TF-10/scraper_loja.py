
import requests
import csv
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

# ==========================================
# LABORATORIO 10 - WEB SCRAPING
# Loja Harry Potter - Casa Grifinoria
# ==========================================

URL = "https://harrypottershop.co.uk/collections/gryffindor"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def limpar_texto(texto):
    """Remove espacos e quebras de linha desnecessarios."""
    return re.sub(r"\s+", " ", texto).strip()


def verificar_robots(session):
    """Consulta o robots.txt antes de acessar a colecao."""

    robots_url = urljoin(URL, "/robots.txt")

    resposta = session.get(robots_url, timeout=20)

    if resposta.status_code == 200:
        parser = RobotFileParser()
        parser.parse(resposta.text.splitlines())

        permitido = parser.can_fetch(
            HEADERS["User-Agent"], URL
        )

        if not permitido:
            raise PermissionError(
                "O robots.txt nao permite acessar a pagina."
            )

        print("Robots.txt: acesso permitido!")

    elif resposta.status_code == 404:
        print("Robots.txt nao encontrado (404).")

    else:
        raise RuntimeError(
            f"Nao foi possivel verificar o robots.txt: "
            f"HTTP {resposta.status_code}"
        )


def extrair_produtos():
    """Acessa as paginas e extrai nomes e precos."""

    produtos = []
    produtos_encontrados = set()

    with requests.Session() as session:
        session.headers.update(HEADERS)

        verificar_robots(session)

        # Percorre as paginas da colecao
        for pagina in range(1, 21):

            url_pagina = f"{URL}?page={pagina}"

            print(f"\nAcessando pagina {pagina}...")

            resposta = session.get(
                url_pagina,
                timeout=20
            )

            print("Status HTTP:", resposta.status_code)

            if resposta.status_code != 200:
                print("Nao foi possivel acessar esta pagina.")
                break

            # Analisa o HTML
            soup = BeautifulSoup(
                resposta.text,
                "html.parser"
            )

            # Localiza os cartoes de produtos
            cartoes = soup.select(".card")

            if not cartoes:
                print("Nenhum cartao encontrado.")
                break

            novos_produtos = 0

            for cartao in cartoes:

                # Extrai o nome
                titulo = cartao.select_one(
                    ".card__heading a"
                )

                if not titulo:
                    titulo = cartao.select_one(
                        ".card__heading"
                    )

                if not titulo:
                    continue

                nome = limpar_texto(
                    titulo.get_text(" ", strip=True)
                )

                if not nome or nome in produtos_encontrados:
                    continue

                # Extrai o preco promocional ou normal
                preco_elemento = cartao.select_one(
                    ".price-item--sale"
                )

                if not preco_elemento:
                    preco_elemento = cartao.select_one(
                        ".price-item--regular"
                    )

                if not preco_elemento:
                    preco_elemento = cartao.select_one(
                        ".price-item"
                    )

                if not preco_elemento:
                    continue

                preco = limpar_texto(
                    preco_elemento.get_text(
                        " ", strip=True
                    )
                )

                # Guarda os dados
                produtos.append({
                    "nome": nome,
                    "preco": preco
                })

                produtos_encontrados.add(nome)
                novos_produtos += 1

            print(
                f"Novos produtos encontrados: {novos_produtos}"
            )

            if novos_produtos == 0:
                print("Fim da listagem de produtos.")
                break

            # Pequena pausa entre requisicoes
            time.sleep(2)

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

    print("\nArquivo produtos_gryffindor.csv salvo!")


def main():

    try:
        print("=" * 45)
        print("LABORATORIO 10 - HARRY POTTER")
        print("=" * 45)

        produtos = extrair_produtos()

        if not produtos:
            print("\nNenhum produto foi extraido.")
            return

        # Exibe os cinco primeiros produtos
        print("\n===== CINCO PRIMEIROS PRODUTOS =====")

        for produto in produtos[:5]:
            print(f"Nome: {produto['nome']}")
            print(f"Preco: {produto['preco']}")
            print("-" * 35)

        print(
            f"\nTotal de produtos encontrados: {len(produtos)}"
        )

        # Salva a lista completa
        salvar_csv(produtos)

        print("\nProcesso finalizado com sucesso!")

    except requests.RequestException as erro:
        print(f"\nErro na requisicao HTTP: {erro}")

    except PermissionError as erro:
        print(f"\nAcesso nao permitido: {erro}")

    except Exception as erro:
        print(f"\nErro inesperado: {erro}")


if __name__ == "__main__":
    main()
