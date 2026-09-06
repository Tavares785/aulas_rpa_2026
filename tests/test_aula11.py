"""
Testes estruturais para AULA11/scraper_noticias.py.

Valida que:
- O script existe
- Importa requests e BeautifulSoup
- Valida status 200
- Salva resultado em CSV
"""

import pathlib

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA11" / "scraper_noticias.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        assert SCRIPT_PATH.exists(), "AULA11/scraper_noticias.py não encontrado."

    def test_arquivo_nao_vazio(self):
        assert SCRIPT_PATH.stat().st_size > 0, "scraper_noticias.py está vazio."


@pytest.fixture(scope="module")
def source_code():
    if not SCRIPT_PATH.exists():
        pytest.skip("Script não encontrado")
    return SCRIPT_PATH.read_text(encoding="utf-8")


class TestImports:
    def test_importa_requests(self, source_code):
        assert "requests" in source_code, "requests não importado."

    def test_importa_beautifulsoup(self, source_code):
        assert "BeautifulSoup" in source_code, "BeautifulSoup não importado."


class TestLogica:
    def test_valida_status_code(self, source_code):
        """O script deve verificar o status code 200."""
        assert "status_code" in source_code or "200" in source_code, (
            "Verificação de status_code 200 não encontrada."
        )

    def test_usa_html_parser(self, source_code):
        """O script deve usar 'html.parser'."""
        assert "html.parser" in source_code, "'html.parser' não utilizado."

    def test_usa_find_all_ou_select(self, source_code):
        """O script deve usar find_all ou select para raspar elementos."""
        usa = "find_all" in source_code or "select" in source_code
        assert usa, "find_all() ou select() não utilizados."


class TestSaida:
    def test_salva_csv(self, source_code):
        """O script deve salvar resultado em CSV."""
        assert "csv" in source_code.lower(), "Referência a CSV não encontrada."
