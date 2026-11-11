import csv
import re
import requests
from bs4 import BeautifulSoup

URL = "https://harrypottershop.co.uk/collections/gryffindor"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}


def limpar_texto(texto: str) -> str:
    """Remove espaços extras e quebras de linha desnecessárias."""
    return re.sub(r"\s+", " ", texto).strip()


def extrair_preco(card: BeautifulSoup) -> str:
    """Extrai o preço efetivo do card de produto (promoção ou regular)."""
    bloco_preco = card.select_one(".price")
    if bloco_preco and "price--on-sale" in bloco_preco.get("class", []):
        preco_el = bloco_preco.select_one(".price__sale .price-item--sale") or card.select_one(".price-item--sale")
    else:
        preco_el = (
            card.select_one(".price__regular .price-item--regular")
            or card.select_one(".price-item--regular")
            or card.select_one(".price-item--sale")
            or card.select_one(".price-item")
        )

    if not preco_el:
        return ""
    return limpar_texto(preco_el.get_text())


def main() -> None:
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
    except requests.RequestException as err:
        print(f"Erro de conexão com o site: {err}")
        return

    if response.status_code == 429:
        print("\n[Erro 429] O site limitou as requisições temporariamente (rate-limit do Shopify).")
        print("Aguarde cerca de 1 a 2 minutos antes de executar o comando novamente.")
        return

    if response.status_code != 200:
        print(f"Erro na requisição HTTP: status {response.status_code}")
        return

    print(f"Status da resposta: {response.status_code} OK")

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select(".card")

    produtos = []
    vistos = set()

    for card in cards:
        titulo_el = card.select_one(".card__heading a") or card.select_one(".card__heading")
        if not titulo_el:
            continue

        nome = limpar_texto(titulo_el.get_text())
        preco = extrair_preco(card)

        if not nome or not preco:
            continue

        chave = (nome, preco)
        if chave in vistos:
            continue
        vistos.add(chave)

        produtos.append({"nome": nome, "preco": preco})

    print(f"\nTotal de produtos extraídos: {len(produtos)}")
    print("\n--- 5 Primeiros Produtos ---")
    for idx, prod in enumerate(produtos[:5], start=1):
        print(f"{idx}. {prod['nome']} - {prod['preco']}")

    arquivo_csv = "produtos_gryffindor.csv"
    with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "preco"])
        writer.writeheader()
        writer.writerows(produtos)

    print(f"\nLista completa salva com sucesso em '{arquivo_csv}'.")


if __name__ == "__main__":
    main()

