
import requests
import csv
from bs4 import BeautifulSoup
from pathlib import Path


# URL da loja
URL = "https://harrypottershop.co.uk/collections/gryffindor"

# Caminho da pasta do projeto
PASTA_PROJETO = Path(__file__).resolve().parent
CAMINHO_CSV = PASTA_PROJETO / "produtos_gryffindor.csv"

# Cabeçalho da requisição
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/157.0.0.0 Safari/537.36"
    )
}


def extrair_produtos():

    print("Iniciando extração de produtos...")

    try:
        resposta = requests.get(
            URL,
            headers=HEADERS,
            timeout=30
        )

        print(f"Status HTTP: {resposta.status_code}")

        # Valida se a resposta foi HTTP 200
        if resposta.status_code != 200:

            if resposta.status_code == 429:
                print("\nO site limitou temporariamente "
                      "as requisições.")

                retry = resposta.headers.get("Retry-After")

                if retry:
                    print(f"Tente novamente após: {retry}")

            print("\nA requisição não retornou HTTP 200 OK.")
            return []

        print("Página recebida com sucesso!")

        # Converte o HTML utilizando BeautifulSoup
        sopa = BeautifulSoup(
            resposta.text,
            "html.parser"
        )

        produtos = []

        # Localiza os cartões de produtos
        cards = sopa.select("li.grid__item")

        # Se não encontrar, tenta outros seletores
        if not cards:
            cards = sopa.select(".card")

        if not cards:
            cards = sopa.select(".card-wrapper")

        print(f"Cartões encontrados: {len(cards)}")

        # Percorre os cartões encontrados
        for card in cards:

            # Localiza o nome do produto
            titulo_elemento = card.select_one(
                ".card__heading a"
            )

            if not titulo_elemento:
                titulo_elemento = card.select_one(
                    ".card__heading"
                )

            if not titulo_elemento:
                continue

            # Extrai e limpa o nome
            titulo = titulo_elemento.get_text(
                " ",
                strip=True
            )

            titulo = " ".join(titulo.split())

            # Localiza o preço
            preco_elemento = (
                card.select_one(".price-item--sale")
                or card.select_one(".price-item--regular")
                or card.select_one(".price-item")
            )

            if not preco_elemento:
                continue

            # Extrai e limpa o preço
            preco = preco_elemento.get_text(
                " ",
                strip=True
            )

            preco = " ".join(preco.split())

            # Verifica se os dados são válidos
            if not titulo or not preco:
                continue

            # Armazena somente nome e preço
            produto = {
                "nome": titulo,
                "preco": preco
            }

            produtos.append(produto)

        return produtos

    except requests.exceptions.Timeout:

        print("A conexão demorou muito para responder.")
        return []

    except requests.exceptions.ConnectionError:

        print("Não foi possível conectar ao site.")
        return []

    except requests.exceptions.RequestException as erro:

        print(f"Erro na requisição HTTP: {erro}")
        return []

    except Exception as erro:

        print(f"Erro inesperado: {erro}")
        return []


def salvar_csv(produtos):

    campos = [
        "nome",
        "preco"
    ]

    with open(
        CAMINHO_CSV,
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos,
            delimiter=";"
        )

        escritor.writeheader()
        escritor.writerows(produtos)

    print("\nArquivo CSV gerado com sucesso!")
    print(f"Local: {CAMINHO_CSV}")


def main():

    print("=" * 50)
    print("      SCRAPER - HARRY POTTER SHOP")
    print("=" * 50)

    produtos = extrair_produtos()

    if not produtos:

        print("\nNenhum produto foi encontrado.")
        print("Verifique o acesso ao site e tente "
              "novamente quando estiver disponível.")

        return

    # Exibe os cinco primeiros produtos
    print("\n===== PRIMEIROS 5 PRODUTOS =====")

    for produto in produtos[:5]:

        print(f"\nNome: {produto['nome']}")
        print(f"Preço: {produto['preco']}")

    # Exibe o resultado final
    print("\n===== RESULTADO FINAL =====")

    print(f"Total de produtos: {len(produtos)}")

    # Salva os produtos no CSV
    salvar_csv(produtos)


if __name__ == "__main__":
    main()
