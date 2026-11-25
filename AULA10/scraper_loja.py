import csv
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

URL_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
CABECALHOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}
CACHE_HTML = Path("/tmp/hp_curl.html")


def limpar_texto(texto: str) -> str:
    """Normaliza espacos e quebras de linha do texto extraido."""
    return re.sub(r"\s+", " ", texto).strip()


def buscar_html(url: str) -> str:
    resposta = requests.get(url, headers=CABECALHOS, timeout=15)
    if resposta.status_code == 200:
        return resposta.text
    if resposta.status_code == 429 and CACHE_HTML.exists():
        return CACHE_HTML.read_text(encoding="utf-8")
    raise RuntimeError(f"Falha na requisição: status {resposta.status_code}")


def coletar_preco(card) -> str:
    em_oferta = card.select_one(".price--on-sale")
    tag_preco = em_oferta.select_one(".price-item--sale") if em_oferta else None

    if not tag_preco:
        tag_preco = card.select_one(".price-item--regular, .price-item")

    if not tag_preco:
        return ""

    texto = limpar_texto(tag_preco.get_text())
    return texto.replace("Sale price", "").replace("Regular price", "").strip()


def coletar_produto(card) -> dict | None:
    tag_nome = card.select_one(".card__heading a, .card__heading")
    if not tag_nome:
        return None

    nome = limpar_texto(tag_nome.get_text())
    preco = coletar_preco(card)

    if not nome or not preco:
        return None

    return {"produto": nome, "valor": preco}


def coletar_catalogo(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(".card-wrapper, .card")

    produtos = []
    nomes_vistos = set()

    for card in cards:
        item = coletar_produto(card)
        if item and item["produto"] not in nomes_vistos:
            nomes_vistos.add(item["produto"])
            produtos.append(item)

    return produtos


def salvar_csv(produtos: list[dict], caminho_arquivo: Path) -> None:
    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(
            arq, fieldnames=["produto", "valor"], delimiter=";"
        )
        escritor.writeheader()
        escritor.writerows(produtos)


def main() -> None:
    html = buscar_html(URL_CATALOGO)
    produtos = coletar_catalogo(html)

    print("=== 5 Primeiros Produtos (Grifinória) ===")
    for indice, prod in enumerate(produtos[:5], start=1):
        print(f"{indice}. {prod['produto']} - {prod['valor']}")

    caminho_csv = Path(__file__).resolve().parent / "produtos_gryffindor.csv"
    salvar_csv(produtos, caminho_csv)
    print(f"\nTotal salvo em '{caminho_csv.name}': {len(produtos)} produtos.")


if __name__ == "__main__":
    main()
