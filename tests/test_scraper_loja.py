from pathlib import Path
from types import SimpleNamespace

import pytest

from AULA10 import scraper_loja


def resposta(status_code, headers=None, text=""):
    return SimpleNamespace(
        status_code=status_code,
        headers=headers or {},
        text=text,
    )


def test_baixar_pagina_espera_retry_after_e_tenta_novamente(monkeypatch):
    chamadas = []
    esperas = []
    respostas = [
        resposta(429, {"Retry-After": "60"}),
        resposta(200, text="<html>ok</html>"),
    ]

    def get(*args, **kwargs):
        chamadas.append((args, kwargs))
        return respostas.pop(0)

    monkeypatch.setattr(scraper_loja.requests, "get", get)
    monkeypatch.setattr(scraper_loja.time, "sleep", esperas.append)

    assert scraper_loja.baixar_pagina("https://example.com") == "<html>ok</html>"
    assert len(chamadas) == 2
    assert esperas == [60]


def test_baixar_pagina_para_apos_maximo_de_tentativas(monkeypatch):
    chamadas = []
    esperas = []

    def get(*args, **kwargs):
        chamadas.append((args, kwargs))
        return resposta(429, {"Retry-After": "60"})

    monkeypatch.setattr(scraper_loja.requests, "get", get)
    monkeypatch.setattr(scraper_loja.time, "sleep", esperas.append)

    with pytest.raises(SystemExit, match="continuou limitando"):
        scraper_loja.baixar_pagina("https://example.com")

    assert len(chamadas) == scraper_loja.MAX_RETRIES + 1
    assert esperas == [60] * scraper_loja.MAX_RETRIES


def test_baixar_pagina_rejeita_retry_after_invalido(monkeypatch):
    monkeypatch.setattr(
        scraper_loja.requests,
        "get",
        lambda *args, **kwargs: resposta(429, {"Retry-After": "depois"}),
    )
    monkeypatch.setattr(scraper_loja.time, "sleep", lambda _: pytest.fail("não deve esperar"))

    with pytest.raises(SystemExit, match="Retry-After válido"):
        scraper_loja.baixar_pagina("https://example.com")


def test_extrair_produtos_inclui_precos():
    html = """
    <div class="card">
      <h3 class="card__heading">
        <a>Produto em promoção</a>
      </h3>
      <span class="price-item--sale">£12.50</span>
      <span class="price-item--regular">£15.00</span>
    </div>
    <div class="card">
      <h3 class="card__heading">Produto regular</h3>
      <span class="price-item--regular">£18.95</span>
    </div>
    """

    assert scraper_loja.extrair_produtos(html) == [
        {"nome": "Produto em promoção", "preco": "£12.50"},
        {"nome": "Produto regular", "preco": "£18.95"},
    ]


def test_main_exibe_precos_e_salva_csv(monkeypatch, tmp_path, capsys):
    html = """
    <div class="card">
      <h3 class="card__heading"><a>Produto exemplo</a></h3>
      <span class="price-item--regular">£18.95</span>
    </div>
    """
    caminho_csv = tmp_path / "produtos_gryffindor.csv"
    monkeypatch.setattr(scraper_loja, "baixar_pagina", lambda _: html)
    monkeypatch.setattr(scraper_loja, "ARQUIVO_CSV", caminho_csv)

    scraper_loja.main()

    assert "Produto exemplo - £18.95" in capsys.readouterr().out
    assert caminho_csv.read_text(encoding="utf-8-sig").splitlines() == [
        "nome,preco",
        "Produto exemplo,£18.95",
    ]


def test_csv_padrao_fica_ao_lado_do_script():
    assert scraper_loja.ARQUIVO_CSV == (
        Path(scraper_loja.__file__).resolve().parent / "produtos_gryffindor.csv"
    )
