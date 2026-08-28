"""
Testes unitários para AULA01/bot_initializer.py.

Cobertura:
- Existência das variáveis obrigatórias (BOT_NAME, MAX_RETRIES, EXECUTION_TIMEOUT, IS_PRODUCTION)
- Validação dos tipos esperados (str, int, float, bool)
- Validação dos valores definidos pelo aluno
"""

import importlib.util
import pathlib

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA01" / "bot_initializer.py"


@pytest.fixture(scope="module")
def bot_module():
    """Importa o módulo bot_initializer.py dinamicamente."""
    assert SCRIPT_PATH.exists(), (
        f"Arquivo não encontrado: {SCRIPT_PATH}. "
        "Certifique-se de que AULA01/bot_initializer.py existe no repositório."
    )
    spec = importlib.util.spec_from_file_location("bot_initializer", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Existência das variáveis obrigatórias
# ---------------------------------------------------------------------------

class TestVariaveisExistem:
    def test_bot_name_definida(self, bot_module):
        """A variável BOT_NAME deve estar definida no módulo."""
        assert hasattr(bot_module, "BOT_NAME"), "Variável BOT_NAME não encontrada"

    def test_max_retries_definida(self, bot_module):
        """A variável MAX_RETRIES deve estar definida no módulo."""
        assert hasattr(bot_module, "MAX_RETRIES"), "Variável MAX_RETRIES não encontrada"

    def test_execution_timeout_definida(self, bot_module):
        """A variável EXECUTION_TIMEOUT deve estar definida no módulo."""
        assert hasattr(bot_module, "EXECUTION_TIMEOUT"), "Variável EXECUTION_TIMEOUT não encontrada"

    def test_is_production_definida(self, bot_module):
        """A variável IS_PRODUCTION deve estar definida no módulo."""
        assert hasattr(bot_module, "IS_PRODUCTION"), "Variável IS_PRODUCTION não encontrada"


# ---------------------------------------------------------------------------
# Validação de tipos
# ---------------------------------------------------------------------------

class TestTiposCorretos:
    def test_bot_name_e_string(self, bot_module):
        """BOT_NAME deve ser do tipo str."""
        assert isinstance(bot_module.BOT_NAME, str), (
            f"BOT_NAME deveria ser str, mas é {type(bot_module.BOT_NAME).__name__}"
        )

    def test_max_retries_e_int(self, bot_module):
        """MAX_RETRIES deve ser do tipo int."""
        assert isinstance(bot_module.MAX_RETRIES, int), (
            f"MAX_RETRIES deveria ser int, mas é {type(bot_module.MAX_RETRIES).__name__}"
        )

    def test_execution_timeout_e_float(self, bot_module):
        """EXECUTION_TIMEOUT deve ser do tipo float."""
        assert isinstance(bot_module.EXECUTION_TIMEOUT, float), (
            f"EXECUTION_TIMEOUT deveria ser float, mas é {type(bot_module.EXECUTION_TIMEOUT).__name__}"
        )

    def test_is_production_e_bool(self, bot_module):
        """IS_PRODUCTION deve ser do tipo bool."""
        assert isinstance(bot_module.IS_PRODUCTION, bool), (
            f"IS_PRODUCTION deveria ser bool, mas é {type(bot_module.IS_PRODUCTION).__name__}"
        )


# ---------------------------------------------------------------------------
# Validação de valores
# ---------------------------------------------------------------------------

class TestValoresEsperados:
    def test_bot_name_valor(self, bot_module):
        """BOT_NAME deve ser 'RPA_FINANCEIRO_01'."""
        assert bot_module.BOT_NAME == "RPA_FINANCEIRO_01", (
            f"BOT_NAME esperado: 'RPA_FINANCEIRO_01', encontrado: '{bot_module.BOT_NAME}'"
        )

    def test_max_retries_valor(self, bot_module):
        """MAX_RETRIES deve ser 3."""
        assert bot_module.MAX_RETRIES == 3, (
            f"MAX_RETRIES esperado: 3, encontrado: {bot_module.MAX_RETRIES}"
        )

    def test_execution_timeout_valor(self, bot_module):
        """EXECUTION_TIMEOUT deve ser 30.0."""
        assert bot_module.EXECUTION_TIMEOUT == 30.0, (
            f"EXECUTION_TIMEOUT esperado: 30.0, encontrado: {bot_module.EXECUTION_TIMEOUT}"
        )

    def test_is_production_valor(self, bot_module):
        """IS_PRODUCTION deve ser False."""
        assert bot_module.IS_PRODUCTION is False, (
            f"IS_PRODUCTION esperado: False, encontrado: {bot_module.IS_PRODUCTION}"
        )
