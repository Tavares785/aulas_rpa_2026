"""
Testes unitários para AULA03/mod_rh.py.

Cobertura:
- Existência do script
- Função cadastrar_colaborador retorna dicionário correto
- Função exibir_colaboradores aceita lista e imprime sem erro
"""

import importlib.util
import pathlib
import sys

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA03" / "mod_rh.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        """O arquivo mod_rh.py deve existir em AULA03/."""
        assert SCRIPT_PATH.exists(), (
            f"Arquivo não encontrado: {SCRIPT_PATH}. "
            "Crie o arquivo AULA03/mod_rh.py conforme o enunciado."
        )

    def test_arquivo_nao_vazio(self):
        """O script não deve estar vazio."""
        assert SCRIPT_PATH.stat().st_size > 0, (
            "O arquivo mod_rh.py está vazio."
        )


@pytest.fixture(scope="module")
def mod_rh():
    """Importa o módulo mod_rh.py dinamicamente."""
    if not SCRIPT_PATH.exists():
        pytest.skip("mod_rh.py não encontrado")
    spec = importlib.util.spec_from_file_location("mod_rh", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    # Evita execução do menu interativo (if __name__ == '__main__')
    sys.modules["mod_rh"] = mod
    spec.loader.exec_module(mod)
    return mod


class TestCadastrarColaborador:
    def test_funcao_existe(self, mod_rh):
        """A função cadastrar_colaborador deve existir."""
        assert hasattr(mod_rh, "cadastrar_colaborador"), (
            "Função 'cadastrar_colaborador' não encontrada em mod_rh.py"
        )

    def test_retorna_dicionario(self, mod_rh):
        """cadastrar_colaborador deve retornar um dicionário."""
        resultado = mod_rh.cadastrar_colaborador("Ana", "Analista", 5000.0)
        assert isinstance(resultado, dict), (
            f"Esperado dict, retornou {type(resultado).__name__}"
        )

    def test_chaves_obrigatorias(self, mod_rh):
        """O dicionário deve conter as chaves 'nome', 'cargo' e 'salario'."""
        resultado = mod_rh.cadastrar_colaborador("Carlos", "Dev", 8000.0)
        for chave in ["nome", "cargo", "salario"]:
            assert chave in resultado, (
                f"Chave '{chave}' ausente no dicionário retornado"
            )

    def test_valores_corretos(self, mod_rh):
        """Os valores do dicionário devem corresponder aos parâmetros."""
        resultado = mod_rh.cadastrar_colaborador("Maria", "Gerente", 12000.0)
        assert resultado["nome"] == "Maria"
        assert resultado["cargo"] == "Gerente"
        assert resultado["salario"] == 12000.0

    def test_tipo_salario_float(self, mod_rh):
        """O salário no dicionário deve ser do tipo float."""
        resultado = mod_rh.cadastrar_colaborador("João", "Estagiário", 2000.0)
        assert isinstance(resultado["salario"], (int, float)), (
            f"Salário deveria ser numérico, mas é {type(resultado['salario']).__name__}"
        )


class TestExibirColaboradores:
    def test_funcao_existe(self, mod_rh):
        """A função exibir_colaboradores deve existir."""
        assert hasattr(mod_rh, "exibir_colaboradores"), (
            "Função 'exibir_colaboradores' não encontrada em mod_rh.py"
        )

    def test_aceita_lista_vazia(self, mod_rh):
        """exibir_colaboradores deve aceitar lista vazia sem erro."""
        # Não deve lançar exceção
        mod_rh.exibir_colaboradores([])

    def test_aceita_lista_com_colaboradores(self, mod_rh, capsys):
        """exibir_colaboradores deve imprimir os dados da lista."""
        lista = [
            {"nome": "Ana", "cargo": "Dev", "salario": 7000.0},
            {"nome": "Pedro", "cargo": "QA", "salario": 5500.0},
        ]
        mod_rh.exibir_colaboradores(lista)
        capturado = capsys.readouterr()
        assert "Ana" in capturado.out, "Nome 'Ana' não apareceu na saída"
        assert "Pedro" in capturado.out, "Nome 'Pedro' não apareceu na saída"

    def test_retorno_none(self, mod_rh):
        """exibir_colaboradores deve retornar None (apenas imprime)."""
        resultado = mod_rh.exibir_colaboradores([])
        assert resultado is None, (
            f"Esperado retorno None, mas retornou {resultado}"
        )
