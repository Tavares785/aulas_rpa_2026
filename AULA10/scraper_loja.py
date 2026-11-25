import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ENDERECO_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_CSV = Path(__file__).with_name("produtos_gryffindor.csv")
CABECALHOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def limpar_texto(texto: str) -> str:
    return re.sub(r"\s+", " ", texto).strip()


def extrair_produtos(html: str) -> list[dict[str, str]]:
    sopa = BeautifulSoup(html, "html.parser")
    produtos = []

    for cartao in sopa.select(".card"):
        titulo = cartao.select_one(".card__heading")
        if titulo is None:
            continue

        elemento_preco = (
            cartao.select_one(".price-item--sale")
            or cartao.select_one(".price-item--regular")
            or cartao.select_one(".price-item")
        )
        nome = limpar_texto(titulo.get_text(" ", strip=True))
        preco = (
            limpar_texto(elemento_preco.get_text(" ", strip=True))
            if elemento_preco is not None
            else ""
        )
        if nome and preco:
            produtos.append({"nome": nome, "preco": preco})

    if not produtos:
        raise ValueError("Nenhum produto com nome e preço foi encontrado no catálogo.")
    return produtos


def coletar_produtos() -> list[dict[str, str]]:
    resposta = requests.get(
        ENDERECO_CATALOGO,
        headers=CABECALHOS,
        timeout=15,
    )
    if resposta.status_code == 429:
        retry_after = resposta.headers.get("Retry-After")
        orientacao = (
            f"Tente novamente após {retry_after}."
            if retry_after
            else "Aguarde antes de tentar novamente."
        )
        raise requests.HTTPError(
            f"A loja limitou as requisições (HTTP 429). {orientacao}",
            response=resposta,
        )
    if resposta.status_code != 200:
        resposta.raise_for_status()
        raise requests.HTTPError(
            f"Esperado HTTP 200, recebido {resposta.status_code}.",
            response=resposta,
        )

    return extrair_produtos(resposta.text)


def salvar_csv(produtos: list[dict[str, str]]) -> None:
    with ARQUIVO_CSV.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["nome", "preco"])
        escritor.writeheader()
        escritor.writerows(produtos)


def main() -> None:
    try:
        produtos = coletar_produtos()
    except requests.HTTPError as erro:
        print(f"Não foi possível coletar o catálogo: {erro}")
        raise SystemExit(1) from None

    for produto in produtos[:5]:
        print(f"{produto['nome']} | {produto['preco']}")

    salvar_csv(produtos)
    print(f"\n{len(produtos)} produtos salvos em {ARQUIVO_CSV}")


if __name__ == "__main__":
    main()
