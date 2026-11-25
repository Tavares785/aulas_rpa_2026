import csv
import sys
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup

URL = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_CSV = Path(__file__).resolve().with_name("produtos_gryffindor.csv")
MAX_RETRIES = 3

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeb"
        "Kit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}


def segundos_ate_retry(retry_after: str | None) -> float | None:
    if not retry_after:
        return None

    try:
        return max(0.0, float(int(retry_after)))
    except ValueError:
        try:
            data_retry = parsedate_to_datetime(retry_after)
        except (TypeError, ValueError, OverflowError):
            return None

        if data_retry.tzinfo is None:
            data_retry = data_retry.replace(tzinfo=timezone.utc)
        return max(0.0, (data_retry - datetime.now(timezone.utc)).total_seconds())


def limpar(texto: str) -> str:
    return " ".join(texto.split()).strip()


def baixar_pagina(url: str) -> str:
    for tentativa in range(MAX_RETRIES + 1):
        try:
            resposta = requests.get(url, headers=HEADERS, timeout=15)
        except requests.RequestException as erro:
            sys.exit(f"Erro de conexão: {erro}")

        if resposta.status_code == 429:
            if tentativa == MAX_RETRIES:
                sys.exit(
                    f"A loja continuou limitando as requisições após "
                    f"{MAX_RETRIES} tentativas."
                )

            retry_after = resposta.headers.get("Retry-After")
            segundos = segundos_ate_retry(retry_after)
            if segundos is None:
                sys.exit(
                    "A loja limitou a requisição (HTTP 429), mas não informou "
                    "um Retry-After válido."
                )

            print(f"Limite de requisições atingido. Tentando novamente em {segundos:g}s.")
            time.sleep(segundos)
            continue

        if resposta.status_code != 200:
            sys.exit(f"Falha na requisição: HTTP {resposta.status_code}")

        print(f"Requisição OK (HTTP {resposta.status_code})")
        return resposta.text

    raise RuntimeError("Fluxo de tentativas inesperado.")


def extrair_preco(card) -> str:
    for seletor in (".price-item--sale", ".price-item--regular", ".price-item"):
        for elemento in card.select(seletor):
            texto = limpar(elemento.get_text())
            if texto:
                return texto
    return ""


def extrair_produtos(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select(".card")
    if not cards:  # alternativa comum em temas Shopify
        cards = soup.select(".card-wrapper")

    produtos = []
    vistos = set()

    for card in cards:
        titulo = card.select_one(".card__heading a") or card.select_one(".card__heading")
        if titulo is None:
            continue

        nome = limpar(titulo.get_text())
        preco = extrair_preco(card)

        # Evita duplicatas e cards vazios
        if not nome or (nome, preco) in vistos:
            continue
        vistos.add((nome, preco))

        produtos.append({"nome": nome, "preco": preco})

    return produtos


def salvar_csv(produtos: list[dict], caminho: str | Path) -> None:
    with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["nome", "preco"])
        escritor.writeheader()
        escritor.writerows(produtos)


def main() -> None:
    html = baixar_pagina(URL)
    produtos = extrair_produtos(html)

    if not produtos:
        sys.exit("Nenhum produto encontrado. Verifique os seletores e o HTML da página.")

    print(f"\n{len(produtos)} produtos encontrados. Os 5 primeiros:\n")
    for i, produto in enumerate(produtos[:5], start=1):
        print(f"{i}. {produto['nome']} - {produto['preco']}")

    salvar_csv(produtos, ARQUIVO_CSV)
    print(f"\nLista completa salva em '{ARQUIVO_CSV}'.")


if __name__ == "__main__":
    main()
