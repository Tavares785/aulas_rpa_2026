"""
Testes estruturais para AULA07 (script de lançamento de notas).

Valida que:
- Existe pelo menos um .py na pasta AULA07
- O script importa pyautogui
- A lista 'alunos' está definida com dicionários contendo 'matricula' e 'nota'
"""

import ast
import pathlib

import pytest


AULA_DIR = pathlib.Path(__file__).parent.parent / "AULA07"


@pytest.fixture(scope="module")
def script_path():
    """Encontra o script principal (primeiro .py que não é test_)."""
    scripts = [f for f in AULA_DIR.glob("*.py") if not f.name.startswith("test_")]
    assert scripts, "Nenhum script Python encontrado em AULA07/"
    return scripts[0]


@pytest.fixture(scope="module")
def source_code(script_path):
    return script_path.read_text(encoding="utf-8")


class TestScriptExiste:
    def test_pasta_existe(self):
        assert AULA_DIR.exists(), "Pasta AULA07/ não encontrada."

    def test_script_python_existe(self, script_path):
        assert script_path.exists()


class TestImports:
    def test_importa_pyautogui(self, source_code):
        """O script deve importar pyautogui."""
        assert "pyautogui" in source_code, "pyautogui não importado."


class TestEstruturaAlunos:
    def test_lista_alunos_definida(self, source_code):
        """A variável 'alunos' deve estar definida."""
        assert "alunos" in source_code, "Variável 'alunos' não encontrada."

    def test_contem_matricula(self, source_code):
        """A lista deve ter chave 'matricula'."""
        assert "matricula" in source_code, "Chave 'matricula' não encontrada."

    def test_contem_nota(self, source_code):
        """A lista deve ter chave 'nota'."""
        assert "nota" in source_code, "Chave 'nota' não encontrada."
