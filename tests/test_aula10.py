"""
Testes estruturais para AULA10/leitor_faturas_pdf.py.

Valida que:
- O script existe
- Importa as bibliotecas obrigatórias (pdfplumber, pandas, re)
- Usa expressões regulares
- Gera o arquivo Excel
"""

import pathlib

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA10" / "leitor_faturas_pdf.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        assert SCRIPT_PATH.exists(), "AULA10/leitor_faturas_pdf.py não encontrado."

    def test_arquivo_nao_vazio(self):
        assert SCRIPT_PATH.stat().st_size > 0, "leitor_faturas_pdf.py está vazio."


@pytest.fixture(scope="module")
def source_code():
    if not SCRIPT_PATH.exists():
        pytest.skip("Script não encontrado")
    return SCRIPT_PATH.read_text(encoding="utf-8")


class TestImports:
    def test_importa_pdfplumber(self, source_code):
        assert "pdfplumber" in source_code, "pdfplumber não importado."

    def test_importa_pandas(self, source_code):
        assert "pandas" in source_code or "import pd" in source_code, (
            "pandas não importado."
        )

    def test_importa_re(self, source_code):
        """O script deve usar expressões regulares (módulo re)."""
        assert "import re" in source_code or "from re" in source_code, (
            "Módulo 're' não importado."
        )


class TestRegex:
    def test_usa_re_search_ou_findall(self, source_code):
        """O script deve usar re.search ou re.findall para extrair padrões."""
        usa_regex = "re.search" in source_code or "re.findall" in source_code
        assert usa_regex, "re.search ou re.findall não utilizados."


class TestExportacao:
    def test_gera_excel(self, source_code):
        """O script deve salvar em .xlsx."""
        assert "xlsx" in source_code, "Referência a .xlsx não encontrada."

    def test_usa_to_excel(self, source_code):
        """O script deve usar DataFrame.to_excel()."""
        assert "to_excel" in source_code, "Método to_excel() não utilizado."
