import csv
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://harrypottershop.co.uk"
COLLECTION_URL = f"{BASE_URL}/collections/gryffindor"
OUTPUT_CSV = "produtos_gryffindor.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}


def limpar_texto(texto: str) -> str:
    """Remove quebras de linha e normaliza espaços consecutivos."""
    return " ".join(texto.split())


def verificar_robots(url: str, user_agent: str = "*") -> bool:
    """Verifica no robots.txt se a URL pode ser coletada."""
    rp = RobotFileParser()
    rp.set_url(f"{BASE_URL}/robots.txt")
    try:
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        return True


def extrair_produtos(html: str) -> list[dict[str, str]]:
    """Faz o parse do HTML e extrai nome e preço efetivo de cada card."""
    soup = BeautifulSoup(html, "html.parser")
    produtos = []
    vistos = set()

    cards = soup.select(".card-wrapper") or soup.select(".card")

    for card in cards:
        # Prioriza .card__content para evitar duplicatas internas do tema Shopify
        titulo_el = (
            card.select_one(".card__content .card__heading a")
            or card.select_one(".card__heading a")
            or card.select_one(".card__heading")
        )
        if not titulo_el:
            continue

        nome = limpar_texto(titulo_el.get_text())
        if not nome or nome in vistos:
            continue

        # Em temas Shopify, .price-item--sale pode existir vazio em itens sem desconto
        sale_el = card.select_one(".price-item--sale")
        regular_el = card.select_one(".price-item--regular")

        preco = ""
        if sale_el and limpar_texto(sale_el.get_text()):
            preco = limpar_texto(sale_el.get_text())
        elif regular_el and limpar_texto(regular_el.get_text()):
            preco = limpar_texto(regular_el.get_text())

        if not preco:
            continue

        vistos.add(nome)
        produtos.append({"nome": nome, "preco": preco})

    return produtos


def salvar_csv(produtos: list[dict[str, str]], caminho: str) -> None:
    """Salva os produtos extraídos em CSV com cabeçalho 'nome,preco'."""
    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=["nome", "preco"])
        writer.writeheader()
        writer.writerows(produtos)


def main() -> None:
    if not verificar_robots(COLLECTION_URL, HEADERS["User-Agent"]):
        print("Coleta não permitida pelo robots.txt.")
        return

    response = requests.get(COLLECTION_URL, headers=HEADERS, timeout=15)

    if response.status_code != 200:
        raise RuntimeError(
            f"Erro na requisição HTTP. Status code: {response.status_code}"
        )

    produtos = extrair_produtos(response.text)

    print(f"Produtos encontrados: {len(produtos)}\n")
    print("Top 5 produtos:")
    for idx, item in enumerate(produtos[:5], start=1):
        print(f"{idx}. {item['nome']} — {item['preco']}")

    salvar_csv(produtos, OUTPUT_CSV)
    print(f"\nDados salvos em '{OUTPUT_CSV}'.")


if __name__ == "__main__":
    main()
