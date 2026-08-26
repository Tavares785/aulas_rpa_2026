"""
Testes estruturais para AULA06/notepad_bot.py.

Valida que o script:
- Existe e não está vazio
- Importa pyautogui
- Configura FAILSAFE = True e PAUSE
"""

import ast
import pathlib

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA06" / "notepad_bot.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        assert SCRIPT_PATH.exists(), "AULA06/notepad_bot.py não encontrado."

    def test_arquivo_nao_vazio(self):
        assert SCRIPT_PATH.stat().st_size > 0, "notepad_bot.py está vazio."


@pytest.fixture(scope="module")
def source_code():
    if not SCRIPT_PATH.exists():
        pytest.skip("Script não encontrado")
    return SCRIPT_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def tree(source_code):
    return ast.parse(source_code)


class TestImportPyautogui:
    def test_importa_pyautogui(self, source_code):
        """O script deve importar pyautogui."""
        assert "pyautogui" in source_code, "pyautogui não importado no script."


class TestConfiguracaoSeguranca:
    def test_failsafe_configurado(self, source_code):
        """FAILSAFE deve ser configurado como True."""
        assert "FAILSAFE" in source_code, "pyautogui.FAILSAFE não configurado."
        assert "True" in source_code, "FAILSAFE deve ser True."

    def test_pause_configurado(self, source_code):
        """PAUSE deve ser configurado."""
        assert "PAUSE" in source_code, "pyautogui.PAUSE não configurado."
