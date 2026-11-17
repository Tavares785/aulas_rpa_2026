"""
Lab 10 - Extracao de Dados da Web com BeautifulSoup

Robo de monitoramento de precos: coleta nome e preco dos produtos da
colecao Gryffindor da loja oficial do Harry Potter (Shopify) e salva
o resultado em produtos_gryffindor.csv (colunas: nome, preco).

Requer: pip install requests beautifulsoup4
"""
import csv
import re
import time
from pathlib import Path
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

try:
    import requests
    from bs4 import BeautifulSoup

    LIBS_OK = True
except ImportError:
    requests = None  # type: ignore[assignment]
    BeautifulSoup = None  # type: ignore[assignment]
    LIBS_OK = False

URL_CATALOGO = "https://harrypottershop.co.uk/collections/gryffindor"
ARQUIVO_CSV = Path(__file__).parent / "produtos_gryffindor.csv"
COLUNAS = ["nome", "preco"]

# Cabecalho de navegador real: boa pratica para nao ser bloqueado.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9,pt-BR;q=0.8",
}

TENTATIVAS = 3
ESPERA_BASE_S = 5  # espera crescente entre tentativas (5s, 10s, ...)


def limpar_texto(texto: str) -> str:
    """Remove quebras de linha e espacos repetidos."""
    return re.sub(r"\s+", " ", texto or "").strip()


def scraping_permitido(url: str) -> bool:
    """Consulta o robots.txt do site antes de raspar (etica de scraping)."""
    robots_url = urljoin(url, "/robots.txt")
    parser = RobotFileParser()
    try:
        resposta = requests.get(robots_url, headers=HEADERS, timeout=10)
        if resposta.status_code != 200:
            # Sem robots.txt acessivel: segue, mas avisa.
            print(f"[robots] robots.txt indisponivel (HTTP {resposta.status_code}).")
            return True
        parser.parse(resposta.text.splitlines())
    except requests.RequestException as erro:
        print(f"[robots] Falha ao ler robots.txt: {erro}")
        return True
    permitido = parser.can_fetch(HEADERS["User-Agent"], url)
    print(f"[robots] Acesso a {url}: {'permitido' if permitido else 'BLOQUEADO'}")
    return permitido


def baixar_html(url: str) -> str:
    """Faz o GET e valida o 200 OK, tentando de novo em caso de 429/5xx."""
    for tentativa in range(1, TENTATIVAS + 1):
        resposta = requests.get(url, headers=HEADERS, timeout=15)
        if resposta.status_code == 200:
            print(f"[http] 200 OK ({len(resposta.text)} bytes)")
            return resposta.text

        reprocessavel = resposta.status_code == 429 or resposta.status_code >= 500
        if not reprocessavel or tentativa == TENTATIVAS:
            raise RuntimeError(
                f"Servidor respondeu HTTP {resposta.status_code} "
                f"(esperado 200 OK) apos {tentativa} tentativa(s)."
            )

        retry_after = resposta.headers.get("Retry-After", "")
        espera = int(retry_after) if retry_after.isdigit() else ESPERA_BASE_S * tentativa
        print(f"[http] HTTP {resposta.status_code}; nova tentativa em {espera}s...")
        time.sleep(espera)
    raise RuntimeError("Nao foi possivel baixar a pagina.")  # inalcancavel


def extrair_preco(card) -> str:
    """Preco efetivo: o de promocao (--sale) se houver, senao o regular."""
    elemento = (
        card.select_one(".price-item--sale")
        or card.select_one(".price-item--regular")
        or card.select_one(".price-item")
    )
    return limpar_texto(elemento.get_text()) if elemento else "N/D"


def extrair_produtos(html: str) -> list[dict[str, str]]:
    """Percorre os cards de produto e extrai nome e preco de cada um."""
    sopa = BeautifulSoup(html, "html.parser")
    produtos: list[dict[str, str]] = []
    vistos: set[str] = set()

    # O tema Shopify (Dawn) envolve cada produto em .card-wrapper;
    # se nao existir, cai para o .card diretamente.
    cards = sopa.select(".card-wrapper") or sopa.select(".card")

    for card in cards:
        titulo = card.select_one(".card__heading a") or card.select_one(".card__heading")
        if titulo is None:
            continue
        nome = limpar_texto(titulo.get_text())
        if not nome or nome in vistos:
            continue  # ignora cards vazios e duplicados (heading aparece 2x no tema)
        vistos.add(nome)
        produtos.append({"nome": nome, "preco": extrair_preco(card)})

    return produtos


def salvar_csv(produtos: list[dict[str, str]], caminho: Path) -> None:
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(produtos)


def main() -> int:
    if not LIBS_OK:
        print("Bibliotecas ausentes. Rode: pip install requests beautifulsoup4")
        return 1

    if not scraping_permitido(URL_CATALOGO):
        print("robots.txt nao permite raspar esta pagina. Encerrando.")
        return 1

    try:
        html = baixar_html(URL_CATALOGO)
    except (requests.RequestException, RuntimeError) as erro:
        print(f"Nao foi possivel acessar o catalogo: {erro}")
        return 1

    produtos = extrair_produtos(html)
    if not produtos:
        print("Nenhum produto encontrado. Confira os seletores no DevTools (F12).")
        return 1

    print("\nPrimeiros 5 produtos:")
    for i, produto in enumerate(produtos[:5], start=1):
        print(f"{i}. {produto['nome']} | {produto['preco']}")

    salvar_csv(produtos, ARQUIVO_CSV)
    print(f"\n{len(produtos)} produtos salvos em {ARQUIVO_CSV.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
