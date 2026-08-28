"""
Testes unitários para AULA02/validador_transacoes.py.

Cobertura:
- Existência do script
- Execução sem erros de sintaxe
- Output correto para transações normais, suspeitas e inválidas
"""

import pathlib
import subprocess

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA02" / "validador_transacoes.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        """O arquivo validador_transacoes.py deve existir em AULA02/."""
        assert SCRIPT_PATH.exists(), (
            f"Arquivo não encontrado: {SCRIPT_PATH}. "
            "Crie o arquivo AULA02/validador_transacoes.py conforme o enunciado."
        )

    def test_arquivo_nao_vazio(self):
        """O script não deve estar vazio."""
        assert SCRIPT_PATH.stat().st_size > 0, (
            "O arquivo validador_transacoes.py está vazio."
        )


class TestExecucao:
    @pytest.fixture(scope="class")
    def resultado(self):
        """Executa o script e captura a saída."""
        if not SCRIPT_PATH.exists():
            pytest.skip("Script não encontrado")
        result = subprocess.run(
            ["python", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result

    def test_sem_erro_de_execucao(self, resultado):
        """O script deve executar sem erros (exit code 0)."""
        assert resultado.returncode == 0, (
            f"Script retornou código {resultado.returncode}.\n"
            f"Stderr: {resultado.stderr}"
        )

    def test_output_contem_alerta(self, resultado):
        """O output deve conter '[ALERTA]' para transações > 10000."""
        assert "[ALERTA]" in resultado.stdout, (
            "Output não contém '[ALERTA]'. "
            "Transações acima de R$ 10.000 devem gerar alerta."
        )

    def test_output_contem_erro_critico(self, resultado):
        """O output deve conter '[ERRO CRÍTICO]' para transações <= 0."""
        # Aceita variações comuns de encoding
        saida = resultado.stdout
        tem_erro = "[ERRO CRÍTICO]" in saida or "[ERRO CRITICO]" in saida
        assert tem_erro, (
            "Output não contém '[ERRO CRÍTICO]'. "
            "Transações negativas ou zero devem interromper o loop."
        )

    def test_output_contem_sucesso(self, resultado):
        """O output deve conter '[SUCESSO]' para transações normais."""
        assert "[SUCESSO]" in resultado.stdout, (
            "Output não contém '[SUCESSO]'. "
            "Transações normais devem ser marcadas como processadas."
        )

    def test_break_interrompe_apos_valor_negativo(self, resultado):
        """Após transação inválida (-50.0), o bot NÃO deve processar R$ 800.0."""
        assert "800.0" not in resultado.stdout.split("[ERRO")[
            -1
        ] if "[ERRO" in resultado.stdout else True, (
            "O script parece continuar processando após transação inválida. "
            "Use 'break' para interromper o loop."
        )
