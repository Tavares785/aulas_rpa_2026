from AULA10 import scraper_loja


class RespostaFake:
    status_code = 200

    def __init__(self, texto):
        self.text = texto

    def raise_for_status(self):
        return None


def test_extrai_produtos_e_prioriza_preco_promocional(monkeypatch):
    html = """
    <div class="card">
      <h3 class="card__heading"> Gryffindor <br> Journal </h3>
      <span class="price-item--regular">£20.00</span>
      <span class="price-item--sale"> £18.95 </span>
    </div>
    <div class="card">
      <h3 class="card__heading">Scarf</h3>
      <span class="price-item--regular">£15.00</span>
    </div>
    """
    requisicoes = []

    def get_falso(endereco, **kwargs):
        requisicoes.append((endereco, kwargs))
        return RespostaFake(html)

    monkeypatch.setattr(scraper_loja.requests, "get", get_falso)

    produtos = scraper_loja.coletar_produtos()

    assert produtos == [
        {"nome": "Gryffindor Journal", "preco": "£18.95"},
        {"nome": "Scarf", "preco": "£15.00"},
    ]
    assert requisicoes[0][1]["headers"]["User-Agent"]
    assert requisicoes[0][1]["timeout"] > 0


def test_erro_http_e_propagado(monkeypatch):
    resposta = RespostaFake("")
    resposta.status_code = 503

    monkeypatch.setattr(
        scraper_loja.requests, "get", lambda *args, **kwargs: resposta
    )

    try:
        scraper_loja.coletar_produtos()
    except scraper_loja.requests.HTTPError as erro:
        assert "503" in str(erro)
    else:
        raise AssertionError("Uma resposta diferente de HTTP 200 deveria falhar.")


def test_salva_csv_com_colunas_exigidas(tmp_path):
    caminho = tmp_path / "produtos.csv"
    produtos = [{"nome": "Diário", "preco": "£18.95"}]

    scraper_loja.salvar_csv(produtos, caminho)

    conteudo = caminho.read_text(encoding="utf-8-sig")
    assert conteudo.splitlines() == ["nome,preco", "Diário,£18.95"]
