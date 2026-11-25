
import requests
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

# URL da loja
URL = "https://harrypottershop.co.uk/collections/gryffindor"
ROBOTS_URL = "https://harrypottershop.co.uk/robots.txt"

# Cabeçalho da requisição
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def verificar_robots():
    """Verifica se o acesso automatizado é permitido."""
    print("Verificando robots.txt...")

    try:
        response = requests.get(
            ROBOTS_URL,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code == 404:
            print("robots.txt não encontrado.")
            return True

        response.raise_for_status()

        parser = RobotFileParser()
        parser.set_url(ROBOTS_URL)
        parser.parse(response.text.splitlines())

        permitido = parser.can_fetch(HEADERS["User-Agent"], URL)

        if not permitido:
            print("Acesso não permitido pelo robots.txt.")

        return permitido

    except requests.RequestException as erro:
        print(f"Não foi possível verificar robots.txt: {erro}")
        return False


def extrair_produtos():
    """Acessa a loja e extrai nome e preço dos produtos."""

    print("Iniciando o Web Scraping...")

    if not verificar_robots():
        print("Extração cancelada por segurança.")
        return

    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=20
        )

        if response.status_code == 429:
            print("Erro 429: o servidor limitou as requisições.")
            print("Tente novamente mais tarde.")
            return

        response.raise_for_status()

        print("Conexão realizada com sucesso!")

        # Interpretando o HTML
        soup = BeautifulSoup(response.text, "html.parser")

        print("HTML carregado com sucesso!")

        # Localizando os cards de produtos
        cards = soup.select(".card")

        if not cards:
            cards = soup.select(".card-wrapper")

        produtos = []

        for card in cards:

            # Extraindo o nome
            titulo = card.select_one(".card__heading")

            if not titulo:
                continue

            nome = titulo.get_text(" ", strip=True)

            # Extraindo o preço
            preco = card.select_one(".price-item--sale")

            if not preco:
                preco = card.select_one(".price-item--regular")

            if not preco:
                preco = card.select_one(".price-item")

            if not preco:
                continue

            preco = preco.get_text(" ", strip=True)

            # Normalizando espaços
            nome = re.sub(r"\s+", " ", nome).strip()
            preco = re.sub(r"\s+", " ", preco).strip()

            produtos.append({
                "nome": nome,
                "preco": preco
            })

        # Verificando se encontrou produtos
        if not produtos:
            print("Nenhum produto encontrado.")
            print("Os seletores CSS podem ter mudado.")
            return

        # Exibindo os cinco primeiros produtos
        print("\n===== PRIMEIROS 5 PRODUTOS =====")

        for produto in produtos[:5]:
            print(f"Nome: {produto['nome']}")
            print(f"Preço: {produto['preco']}")
            print("-" * 35)

        # Salvando em CSV
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

        print(f"\nTotal de produtos encontrados: {len(produtos)}")
        print("Arquivo CSV salvo com sucesso!")

    except requests.exceptions.Timeout:
        print("Tempo limite da conexão excedido.")

    except requests.exceptions.HTTPError as erro:
        print(f"Erro HTTP: {erro}")

    except requests.exceptions.RequestException as erro:
        print(f"Erro na conexão: {erro}")

    except Exception as erro:
        print(f"Erro inesperado: {erro}")


# Executando o programa
if __name__ == "__main__":
    extrair_produtos()
