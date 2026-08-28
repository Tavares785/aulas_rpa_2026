"""
Testes estruturais para AULA13/bot_faturamento_avancado.py.

Valida que:
- O script existe
- Usa queue.Queue (Produtor-Consumidor)
- Usa logging com RotatingFileHandler
- Usa tenacity para retry
"""

import pathlib

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA13" / "bot_faturamento_avancado.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        assert SCRIPT_PATH.exists(), "AULA13/bot_faturamento_avancado.py não encontrado."

    def test_arquivo_nao_vazio(self):
        assert SCRIPT_PATH.stat().st_size > 0, "bot_faturamento_avancado.py está vazio."


@pytest.fixture(scope="module")
def source_code():
    if not SCRIPT_PATH.exists():
        pytest.skip("Script não encontrado")
    return SCRIPT_PATH.read_text(encoding="utf-8")


class TestQueue:
    def test_importa_queue(self, source_code):
        """O script deve importar queue."""
        assert "queue" in source_code.lower() or "Queue" in source_code, (
            "Módulo queue não importado."
        )

    def test_usa_queue_put_ou_get(self, source_code):
        """O script deve usar put/get da Queue."""
        usa = "put" in source_code and "get" in source_code
        assert usa, "Métodos put()/get() da Queue não utilizados."


class TestLogging:
    def test_importa_logging(self, source_code):
        assert "logging" in source_code, "Módulo logging não importado."

    def test_usa_rotating_file_handler(self, source_code):
        """O script deve usar RotatingFileHandler."""
        assert "RotatingFileHandler" in source_code, (
            "RotatingFileHandler não utilizado."
        )

    def test_app_rpa_log(self, source_code):
        """O log deve ser gravado em app_rpa.log."""
        assert "app_rpa.log" in source_code, (
            "Nome do arquivo de log 'app_rpa.log' não encontrado."
        )


class TestRetry:
    def test_importa_tenacity(self, source_code):
        """O script deve importar tenacity."""
        assert "tenacity" in source_code, "tenacity não importado."

    def test_usa_retry_decorator(self, source_code):
        """O script deve usar @retry ou retry()."""
        assert "retry" in source_code, "Decorator/função retry não encontrado."
