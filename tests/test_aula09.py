"""
Testes estruturais para AULA09/web_avancado.py.

Valida que:
- O script existe
- Importa selenium e usa Select
- Referencia as URLs de treino (dropdown, alerts, iframe)
"""

import pathlib

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA09" / "web_avancado.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        assert SCRIPT_PATH.exists(), "AULA09/web_avancado.py não encontrado."

    def test_arquivo_nao_vazio(self):
        assert SCRIPT_PATH.stat().st_size > 0, "web_avancado.py está vazio."


@pytest.fixture(scope="module")
def source_code():
    if not SCRIPT_PATH.exists():
        pytest.skip("Script não encontrado")
    return SCRIPT_PATH.read_text(encoding="utf-8")


class TestImports:
    def test_importa_selenium(self, source_code):
        assert "selenium" in source_code, "selenium não importado."

    def test_usa_select(self, source_code):
        """O script deve usar a classe Select para dropdowns."""
        assert "Select" in source_code, "Classe Select não utilizada."


class TestPartes:
    def test_url_dropdown(self, source_code):
        """Parte 1: deve acessar /dropdown."""
        assert "dropdown" in source_code, "URL /dropdown não referenciada."

    def test_url_alerts(self, source_code):
        """Parte 2: deve acessar /javascript_alerts."""
        assert "javascript_alerts" in source_code, "URL /javascript_alerts não referenciada."

    def test_usa_accept_alert(self, source_code):
        """Parte 2: deve usar accept() no alert."""
        assert "accept" in source_code, "Método accept() para alertas não encontrado."

    def test_url_iframe(self, source_code):
        """Parte 3: deve acessar /iframe."""
        assert "iframe" in source_code, "URL /iframe não referenciada."

    def test_switch_to_frame(self, source_code):
        """Parte 3: deve trocar contexto para iframe."""
        assert "switch_to" in source_code, "switch_to não utilizado para iframe."
