"""
Testes estruturais para AULA08/bot_products_harry.py.

Valida que:
- O script existe e não está vazio
- Importa selenium e usa webdriver
- Referencia o site da loja do Harry Potter (harrypottershop.com)
- Configura alguma estratégia de espera (implicitly_wait ou WebDriverWait)
- Usa seletores do Selenium para localizar os produtos
- Coleta título e preço dos produtos em uma estrutura de dados
"""

import pathlib

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA08" / "bot_products_harry.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        assert SCRIPT_PATH.exists(), "AULA08/bot_products_harry.py não encontrado."

    def test_arquivo_nao_vazio(self):
        assert SCRIPT_PATH.exists(), "AULA08/bot_products_harry.py não encontrado."
        assert SCRIPT_PATH.stat().st_size > 0, "bot_products_harry.py está vazio."


@pytest.fixture(scope="module")
def source_code():
    if not SCRIPT_PATH.exists():
        pytest.skip("Script não encontrado")
    return SCRIPT_PATH.read_text(encoding="utf-8")


class TestImportSelenium:
    def test_importa_selenium(self, source_code):
        """O script deve importar selenium."""
        assert "selenium" in source_code, "selenium não importado no script."

    def test_usa_webdriver(self, source_code):
        """O script deve usar webdriver."""
        assert "webdriver" in source_code, "webdriver não referenciado."


class TestLogicaScraping:
    def test_url_harry_potter(self, source_code):
        """O script deve acessar a loja do Harry Potter."""
        assert "harrypottershop.com" in source_code, (
            "URL da loja do Harry Potter (harrypottershop.com) não encontrada no script."
        )

    def test_configura_espera(self, source_code):
        """O script deve configurar alguma espera (implicitly_wait ou WebDriverWait)."""
        assert ("implicitly_wait" in source_code) or ("WebDriverWait" in source_code), (
            "Nenhuma espera configurada (use implicitly_wait ou WebDriverWait)."
        )

    def test_usa_seletor(self, source_code):
        """O script deve localizar elementos com algum seletor do Selenium."""
        assert ("find_element" in source_code) or ("By." in source_code), (
            "Nenhum seletor do Selenium (find_element / By.) encontrado."
        )

    def test_coleta_titulo_e_preco(self, source_code):
        """O script deve coletar título e preço dos produtos."""
        texto = source_code.lower()
        assert "titulo" in texto or "título" in texto, (
            "O script deve coletar o 'titulo' dos produtos."
        )
        assert "preço" in texto or "preco" in texto, (
            "O script deve coletar o 'preço' dos produtos."
        )
