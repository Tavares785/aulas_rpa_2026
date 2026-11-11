"""
AULA 10 - Extracao de Dados da Web em Escala com BeautifulSoup
Entrega do Aluno - Laboratorio 10 (Colecao Gryffindor)
"""
import csv
from pathlib import Path
import re
from typing import Any

try:
    import requests
    from bs4 import BeautifulSoup

    LIBS_DISPONIVEIS = True
except ImportError:
    requests = None  # type: ignore[assignment]
    BeautifulSoup = None  # type: ignore[assignment]
    LIBS_DISPONIVEIS = False
    print("Bibliotecas ausentes. Rode: pip install requests beautifulsoup4")

ENDERECO_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_SAIDA = Path(__file__).parent / "produtos_gryffindor.csv"
COLUNAS = ["nome", "preco"]

CABECALHOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def limpar_texto(texto: str) -> str:
    """Normaliza espacos e quebras de linha do texto extraido."""
    return re.sub(r"\s+", " ", texto).strip()


def coletar_produtos(endereco: str) -> list[dict[str, str]]:
    """Faz a requisicao HTTP e extrai nome e preco de cada produto."""
    resposta = requests.get(endereco, headers=CABECALHOS, timeout=15)
    if resposta.status_code != 200:
        raise RuntimeError(f"Status HTTP inesperado: {resposta.status_code}")

    sopa = BeautifulSoup(resposta.text, "html.parser")

    produtos: list[dict[str, str]] = []
    vistos: set[str] = set()

    for titulo in sopa.select(".card__heading"):
        nome = limpar_texto(titulo.get_text())
        if not nome or nome in vistos:
            continue
        vistos.add(nome)

        cartao = titulo.find_parent(class_="card-wrapper") or titulo.parent
        elemento_preco = (
            cartao.select_one(".price-item--sale")
            or cartao.select_one(".price-item--regular")
            or cartao.select_one(".price-item")
        )
        preco = (
            limpar_texto(elemento_preco.get_text())
            if elemento_preco
            else "N/D"
        )

        produtos.append({"nome": nome, "preco": preco})
    return produtos


def exportar_csv(registros: list[dict[str, Any]], caminho: Path) -> None:
    """Grava os registros coletados em CSV usando csv.DictWriter."""
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(registros)


def executar() -> None:
    """Orquestra a raspagem e a exportacao para CSV."""
    try:
        produtos = coletar_produtos(ENDERECO_CATALOGO)
    except Exception as erro:  # noqa: BLE001
        print("Nao foi possivel acessar o catalogo online agora.")
        print(f"Detalhe tecnico: {erro}")
        raise SystemExit(0)

    for produto in produtos[:5]:
        print(f"- {produto['nome']} | {produto['preco']}")

    exportar_csv(produtos, ARQUIVO_SAIDA)
    print(f"\n{len(produtos)} produtos salvos em {ARQUIVO_SAIDA.name}")


if __name__ == "__main__":
    if not LIBS_DISPONIVEIS:
        raise SystemExit(0)
    executar() 