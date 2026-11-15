"""Testes do scraper de produtos da AULA10 sem requisições externas."""

import csv
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest


SCRIPT_PATH = (
    Path(__file__).parent.parent / "AULA10" / "scraper_loja.py"
)
SPEC = importlib.util.spec_from_file_location("scraper_loja", SCRIPT_PATH)
scraper_loja = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scraper_loja)


def test_coletar_produtos_normaliza_dados_e_prioriza_preco_promocional(
    monkeypatch,
):
    respostas = [
        SimpleNamespace(
            status_code=200,
            text="User-agent: *\nAllow: /",
            raise_for_status=lambda: None,
        ),
        SimpleNamespace(
            status_code=200,
            text="""
                <div class="card-wrapper">
                  <div class="card">
                    <h3 class="card__heading"><a>
                      Gryffindor
                      Metal Crest Journal
                    </a></h3>
                    <span class="price-item--regular">£ 22.00</span>
                    <span class="price-item--sale">£ 18.95</span>
                  </div>
                </div>
            """,
            raise_for_status=lambda: None,
        ),
    ]

    def fake_get(url, headers, timeout):
        assert headers == scraper_loja.CABECALHOS
        assert timeout == scraper_loja.TIMEOUT
        return respostas.pop(0)

    monkeypatch.setattr(scraper_loja.requests, "get", fake_get)

    assert scraper_loja.coletar_produtos("https://example.com/catalog") == [
        {"nome": "Gryffindor Metal Crest Journal", "preco": "£ 18.95"}
    ]


def test_coletar_produtos_rejeita_catalogo_que_nao_retornou_200(monkeypatch):
    responses = iter(
        [
            SimpleNamespace(
                status_code=200,
                text="User-agent: *\nAllow: /",
                raise_for_status=lambda: None,
            ),
            SimpleNamespace(
                status_code=503,
                text="",
                raise_for_status=lambda: None,
            ),
        ]
    )
    monkeypatch.setattr(
        scraper_loja.requests,
        "get",
        lambda *args, **kwargs: next(responses),
    )

    with pytest.raises(scraper_loja.requests.HTTPError, match="recebido 503"):
        scraper_loja.coletar_produtos("https://example.com/catalog")


def test_coletar_produtos_usa_preco_regular_ou_nd(monkeypatch):
    respostas = iter(
        [
            SimpleNamespace(
                status_code=200,
                text="User-agent: *\nAllow: /",
                raise_for_status=lambda: None,
            ),
            SimpleNamespace(
                status_code=200,
                text="""
                    <div class="card-wrapper">
                      <div class="card">
                        <h3 class="card__heading">Crest Mug</h3>
                        <span class="price-item--regular">£12.50</span>
                      </div>
                    </div>
                    <div class="card-wrapper">
                      <div class="card">
                        <h3 class="card__heading">House Scarf</h3>
                      </div>
                    </div>
                """,
                raise_for_status=lambda: None,
            ),
        ]
    )
    monkeypatch.setattr(
        scraper_loja.requests,
        "get",
        lambda *args, **kwargs: next(respostas),
    )

    assert scraper_loja.coletar_produtos("https://example.com/catalog") == [
        {"nome": "Crest Mug", "preco": "£12.50"},
        {"nome": "House Scarf", "preco": "N/D"},
    ]


def test_verificar_robots_bloqueia_coleta(monkeypatch):
    monkeypatch.setattr(
        scraper_loja.requests,
        "get",
        lambda *args, **kwargs: SimpleNamespace(
            status_code=200,
            text="User-agent: *\nDisallow: /collections/",
            raise_for_status=lambda: None,
        ),
    )

    with pytest.raises(PermissionError, match="robots.txt"):
        scraper_loja.verificar_robots(
            "https://example.com/collections/gryffindor"
        )


def test_salvar_csv_grava_cabecalho_e_registros(tmp_path):
    caminho = tmp_path / "produtos.csv"
    produtos = [{"nome": "Diário", "preco": "£18.95"}]

    scraper_loja.salvar_csv(produtos, str(caminho))

    with caminho.open(encoding="utf-8", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    assert linhas == produtos
