"""
Testes estruturais para AULA08/bot_web_login.py.

Valida que:
- O script existe
- Importa selenium
- Referencia a URL de treino e os campos corretos
"""

import pathlib

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA08" / "bot_web_login.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        assert SCRIPT_PATH.exists(), "AULA08/bot_web_login.py não encontrado."

    def test_arquivo_nao_vazio(self):
        assert SCRIPT_PATH.stat().st_size > 0, "bot_web_login.py está vazio."


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


class TestLogicaLogin:
    def test_url_treino(self, source_code):
        """O script deve acessar the-internet.herokuapp.com/login."""
        assert "the-internet.herokuapp.com/login" in source_code, (
            "URL de treino não encontrada no script."
        )

    def test_campo_username(self, source_code):
        """O script deve localizar o campo 'username'."""
        assert "username" in source_code, "Campo 'username' não referenciado."

    def test_campo_password(self, source_code):
        """O script deve localizar o campo 'password'."""
        assert "password" in source_code, "Campo 'password' não referenciado."

    def test_implicitly_wait(self, source_code):
        """O script deve configurar implicitly_wait."""
        assert "implicitly_wait" in source_code, "implicitly_wait não configurado."
