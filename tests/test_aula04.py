"""
Testes unitários para AULA04/processador_csv.py.

Cobertura:
- Existência do script
- Função processar_arquivo existe e aceita um caminho
- Tratamento de FileNotFoundError (não quebra ao receber arquivo inexistente)
- Geração de log ao processar arquivo válido
"""

import importlib.util
import logging
import pathlib
import sys
import tempfile

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA04" / "processador_csv.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        """O arquivo processador_csv.py deve existir em AULA04/."""
        assert SCRIPT_PATH.exists(), (
            f"Arquivo não encontrado: {SCRIPT_PATH}. "
            "Crie o arquivo AULA04/processador_csv.py conforme o enunciado."
        )

    def test_arquivo_nao_vazio(self):
        """O script não deve estar vazio."""
        assert SCRIPT_PATH.stat().st_size > 0, (
            "O arquivo processador_csv.py está vazio."
        )


@pytest.fixture(scope="module")
def mod_processador():
    """Importa o módulo processador_csv.py dinamicamente."""
    if not SCRIPT_PATH.exists():
        pytest.skip("processador_csv.py não encontrado")
    spec = importlib.util.spec_from_file_location("processador_csv", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["processador_csv"] = mod
    spec.loader.exec_module(mod)
    return mod


class TestFuncaoProcessarArquivo:
    def test_funcao_existe(self, mod_processador):
        """A função processar_arquivo deve existir."""
        assert hasattr(mod_processador, "processar_arquivo"), (
            "Função 'processar_arquivo' não encontrada em processador_csv.py"
        )

    def test_funcao_aceita_parametro_caminho(self, mod_processador):
        """processar_arquivo deve aceitar um argumento (caminho do arquivo)."""
        import inspect
        sig = inspect.signature(mod_processador.processar_arquivo)
        assert len(sig.parameters) >= 1, (
            "processar_arquivo deve aceitar pelo menos 1 parâmetro (caminho)"
        )

    def test_arquivo_inexistente_nao_quebra(self, mod_processador):
        """processar_arquivo NÃO deve lançar exceção para arquivo inexistente."""
        # O aluno deve tratar FileNotFoundError internamente
        try:
            mod_processador.processar_arquivo("/caminho/inexistente/fake.csv")
        except FileNotFoundError:
            pytest.fail(
                "processar_arquivo lançou FileNotFoundError. "
                "Use try/except para tratar essa exceção internamente."
            )

    def test_processa_arquivo_valido(self, mod_processador):
        """processar_arquivo deve executar sem erro com um CSV válido."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as f:
            f.write("nome,valor\n")
            f.write("Item A,100\n")
            f.write("Item B,200\n")
            temp_path = f.name

        try:
            mod_processador.processar_arquivo(temp_path)
        except Exception as e:
            pytest.fail(
                f"processar_arquivo falhou com arquivo válido: {e}"
            )
        finally:
            pathlib.Path(temp_path).unlink(missing_ok=True)


class TestLogging:
    def test_usa_modulo_logging(self, mod_processador):
        """O script deve importar e utilizar o módulo logging."""
        assert hasattr(mod_processador, "logging") or "logging" in dir(mod_processador), (
            "O módulo 'logging' não foi importado em processador_csv.py"
        )
