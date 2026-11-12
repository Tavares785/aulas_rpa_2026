import csv
import pathlib
import time
import requests
from bs4 import BeautifulSoup

URL = "https://harrypottershop.co.uk/collections/gryffindor"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
ARQUIVO_CSV = pathlib.Path(__file__).parent / "produtos_gryffindor.csv"


def limpar_texto(texto: str) -> str:
    """Remove quebras de linha e espaços duplicados."""
    return " ".join(texto.split()).strip()


def buscar_html(url: str) -> BeautifulSoup | None:
    """Faz a requisição HTTP com User-Agent e valida status 200."""
    time.sleep(3)
    resposta = requests.get(url, headers=HEADERS, timeout=15)
    print(f"Status HTTP: {resposta.status_code}")

    if resposta.status_code != 200:
        print(f"Erro ao acessar a página: status {resposta.status_code}")
        return None

    return BeautifulSoup(resposta.text, "html.parser")


def extrair_produtos(soup: BeautifulSoup) -> list[dict[str, str]]:
    """Extrai nome e preço de cada card de produto da listagem."""
    produtos = []
    cards = soup.select(".card")

    for card in cards:
        titulo_el = card.select_one(".card__heading")
        preco_el = (
            card.select_one(".price-item--sale")
            or card.select_one(".price-item--regular")
            or card.select_one(".price-item")
        )

        if titulo_el and preco_el:
            nome = limpar_texto(titulo_el.get_text())
            preco = limpar_texto(preco_el.get_text())
            if nome and preco:
                produtos.append({"nome": nome, "preco": preco})

    return produtos


def salvar_csv(produtos: list[dict[str, str]], caminho: pathlib.Path) -> None:
    """Salva a lista de produtos em CSV com colunas 'nome' e 'preco'."""
    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["nome", "preco"])
        escritor.writeheader()
        escritor.writerows(produtos)


if __name__ == "__main__":
    soup = buscar_html(URL)
    if soup:
        lista_produtos = extrair_produtos(soup)
        print(f"Total de produtos extraídos: {len(lista_produtos)}\n")

        print("5 primeiros produtos:")
        for item in lista_produtos[:5]:
            print(f"- {item['nome']} | {item['preco']}")

        salvar_csv(lista_produtos, ARQUIVO_CSV)
        print(f"\nArquivo salvo em: {ARQUIVO_CSV}")
