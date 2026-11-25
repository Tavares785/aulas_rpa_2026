import csv
import re
import time
import requests
from bs4 import BeautifulSoup

URL = "https://harrypottershop.co.uk/collections/gryffindor"
URL_JSON = "https://harrypottershop.co.uk/collections/gryffindor/products.json"
ARQUIVO_SAIDA = "produtos_gryffindor.csv"


def limpar_texto(texto: str) -> str:
    if not texto:
        return ""
    return re.sub(r"\s+", " ", texto).strip()


def extrair_via_html(sessao: requests.Session, url: str) -> list[dict[str, str]] | None:
    for tentativa in range(1, 3):
        resposta = sessao.get(url, timeout=20)

        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, "html.parser")
            cards = soup.select("ul#product-grid li.grid__item")
            if not cards:
                cards = soup.select(".card-wrapper") or soup.select(".card")

            produtos = []
            nomes_vistos = set()

            for card in cards:
                elemento_nome = card.select_one(".card__heading a") or card.select_one(
                    ".card__heading"
                )
                if not elemento_nome:
                    continue

                nome = limpar_texto(elemento_nome.get_text())
                if not nome or nome in nomes_vistos:
                    continue

                elemento_preco = card.select_one(
                    ".price--on-sale .price-item--sale"
                ) or card.select_one(".price-item--regular")

                if not elemento_preco:
                    elemento_preco = card.select_one(".price-item")

                preco = limpar_texto(elemento_preco.get_text()) if elemento_preco else "N/A"
                nomes_vistos.add(nome)
                produtos.append({"nome": nome, "preco": preco})

            return produtos

        if resposta.status_code == 429:
            espera = int(resposta.headers.get("Retry-After", tentativa * 3))
            time.sleep(espera)
            continue

        raise RuntimeError(f"Falha ao acessar a página. Status HTTP: {resposta.status_code}")

    return None


def extrair_via_json_shopify(sessao: requests.Session, url_json: str) -> list[dict[str, str]]:
    resposta = sessao.get(url_json, params={"limit": 250}, timeout=20)
    if resposta.status_code != 200:
        raise RuntimeError(f"Falha ao acessar a página. Status HTTP: {resposta.status_code}")

    dados = resposta.json()
    produtos = []

    for item in dados.get("products", []):
        nome = limpar_texto(item.get("title", ""))
        variantes = item.get("variants", [])
        valor = variantes[0].get("price") if variantes else None
        preco = f"£{float(valor):.2f}" if valor is not None else "N/A"

        if nome:
            produtos.append({"nome": nome, "preco": preco})

    return produtos


def extrair_produtos(url: str) -> list[dict[str, str]]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
    }

    sessao = requests.Session()
    sessao.headers.update(headers)

    produtos = extrair_via_html(sessao, url)
    if produtos:
        return produtos

    return extrair_via_json_shopify(sessao, URL_JSON)


def salvar_csv(produtos: list[dict[str, str]], caminho_arquivo: str) -> None:
    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=["nome", "preco"])
        writer.writeheader()
        writer.writerows(produtos)


def main() -> None:
    print(f"Coletando catálogo de: {URL}\n")
    produtos = extrair_produtos(URL)

    print(f"Total de produtos extraídos: {len(produtos)}")
    print("Top 5 primeiros produtos:\n")

    for i, produto in enumerate(produtos[:5], start=1):
        print(f"{i}. {produto['nome']} — {produto['preco']}")

    salvar_csv(produtos, ARQUIVO_SAIDA)
    print(f"\nArquivo '{ARQUIVO_SAIDA}' gerado com sucesso!")


if __name__ == "__main__":
    main()