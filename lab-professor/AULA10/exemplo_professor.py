"""
AULA 10 - Extracao de Dados da Web com BeautifulSoup
Exemplo do PROFESSOR

Tema didatico: requisicao HTTP com requests + parsing de HTML com
BeautifulSoup (seletores CSS via .select/.select_one) + exportacao CSV.

Cenario de negocio: monitoramento de precos de concorrentes no e-commerce.
O robo coleta nome e preco dos produtos da colecao Ravenclaw da loja
oficial do Harry Potter (site real, construido em Shopify).

Requer: pip install requests beautifulsoup4
"""
import csv
import re
from typing import Any

# Guard de ImportError: se as libs externas faltarem, o modulo ainda
# carrega e a execucao padrao degrada graciosamente (exit 0).
try:
    import requests
    from bs4 import BeautifulSoup

    LIBS_DISPONIVEIS = True
except ImportError:
    requests = None  # type: ignore[assignment]
    BeautifulSoup = None  # type: ignore[assignment]
    LIBS_DISPONIVEIS = False
    print("Bibliotecas ausentes. Rode: pip install requests beautifulsoup4")

ENDERECO_CATALOGO = "https://harrypottershop.co.uk/collections/ravenclaw"
ARQUIVO_SAIDA = "catalogo_ravenclaw.csv"
COLUNAS = ["produto", "valor"]

# User-Agent de navegador real evita bloqueios comuns a bots.
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
    """Faz a requisicao HTTP e extrai nome e preco de cada produto.

    Usa seletores CSS para navegar na arvore DOM (tema Shopify):
    - o titulo de cada produto fica em um elemento com classe .card__heading
    - subimos ate o container .card-wrapper para achar o preco do item
    - o preco fica em .price-item (preferindo o de promocao, .price-item--sale)
    """
    resposta = requests.get(endereco, headers=CABECALHOS, timeout=15)
    resposta.raise_for_status()  # dispara erro explicito se o HTTP nao for 200
    sopa = BeautifulSoup(resposta.text, "html.parser")

    produtos: list[dict[str, str]] = []
    vistos: set[str] = set()

    for titulo in sopa.select(".card__heading"):  # seletor CSS do titulo
        nome = limpar_texto(titulo.get_text())
        if not nome or nome in vistos:
            continue  # ignora blocos vazios ou produtos repetidos
        vistos.add(nome)

        # Sobe ate o container do produto para localizar o preco.
        cartao = titulo.find_parent(class_="card-wrapper") or titulo.parent
        elemento_preco = (
            cartao.select_one(".price-item--sale")
            or cartao.select_one(".price-item--regular")
            or cartao.select_one(".price-item")
        )
        preco = limpar_texto(elemento_preco.get_text()) if elemento_preco else "N/D"

        produtos.append({"produto": nome, "valor": preco})
    return produtos


def exportar_csv(registros: list[dict[str, Any]], caminho: str) -> None:
    """Grava os registros coletados em CSV usando csv.DictWriter."""
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(registros)


def executar() -> None:
    """Orquestra a raspagem e a exportacao, degradando sem rede/lib."""
    # A chamada de rede fica protegida: qualquer falha de conexao vira
    # mensagem amigavel e saida zero, nunca um traceback de erro.
    try:
        produtos = coletar_produtos(ENDERECO_CATALOGO)
    except Exception as erro:  # noqa: BLE001 - captura ampla proposital
        print("Nao foi possivel acessar o catalogo online agora.")
        print(f"Detalhe tecnico: {erro}")
        print("Execucao encerrada sem erro (sem internet e um caso esperado).")
        raise SystemExit(0)

    for produto in produtos[:5]:
        print(produto["produto"], "|", produto["valor"])

    exportar_csv(produtos, ARQUIVO_SAIDA)
    print(f"\n{len(produtos)} produtos salvos em {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    # Sem as libs externas instaladas, encerra de forma graciosa (exit 0).
    if not LIBS_DISPONIVEIS:
        raise SystemExit(0)
    executar()
    # DICA DE AULA: compare a VELOCIDADE deste scraping estatico com o
    # Selenium (aula 8), que sobe um navegador real e consome mais recursos.
