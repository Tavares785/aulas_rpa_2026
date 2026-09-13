"""
Testes unitários para o workflow ci_aulas_12_13.yml
(Validação de Integração com APIs e Arquitetura Assíncrona — AULA12 e AULA13)

Requirements: 6.3, 6.4
"""

import os
import pytest
import yaml

WORKFLOW_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    ".github",
    "workflows",
    "ci_aulas_12_13.yml",
)


@pytest.fixture(scope="module")
def workflow() -> dict:
    """Carrega e faz parse do YAML do workflow ci_aulas_12_13.yml."""
    abs_path = os.path.abspath(WORKFLOW_PATH)
    with open(abs_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def all_steps(workflow: dict) -> list[dict]:
    """Retorna a lista de todos os steps do único job do workflow."""
    jobs = workflow.get("jobs", {})
    assert jobs, "O workflow não contém nenhum job."
    # Pega o primeiro (e único) job
    job = next(iter(jobs.values()))
    steps = job.get("steps", [])
    assert steps, "O job não contém nenhum step."
    return steps


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _step_run_commands(step: dict) -> list[str]:
    """Retorna as linhas do campo 'run' de um step como lista de strings."""
    run_block = step.get("run", "")
    return [line.strip() for line in run_block.splitlines() if line.strip()]


def _find_steps_with_command(steps: list[dict], command: str) -> list[dict]:
    """Retorna steps cujo campo 'run' contém a string `command`."""
    return [
        step for step in steps
        if command in step.get("run", "")
    ]


# ---------------------------------------------------------------------------
# Testes de sintaxe — py_compile (Requirements: 10.3, 6.1)
# ---------------------------------------------------------------------------

class TestPyCompileSteps:

    def test_step_py_compile_aula12_exists(self, all_steps: list[dict]):
        """
        Verifica que existe ao menos um step com o comando
        'python -m py_compile AULA12/bot_cotacao_alerta.py'.

        Validates: Requirements 6.1, 10.3
        """
        cmd = "python -m py_compile AULA12/bot_cotacao_alerta.py"
        matching = _find_steps_with_command(all_steps, cmd)
        assert matching, (
            f"Nenhum step encontrado com o comando '{cmd}'. "
            "O workflow deve verificar a sintaxe de AULA12/bot_cotacao_alerta.py."
        )

    def test_step_py_compile_aula13_exists(self, all_steps: list[dict]):
        """
        Verifica que existe ao menos um step com o comando
        'python -m py_compile AULA13/bot_faturamento_avancado.py'.

        Validates: Requirements 6.1, 10.3
        """
        cmd = "python -m py_compile AULA13/bot_faturamento_avancado.py"
        matching = _find_steps_with_command(all_steps, cmd)
        assert matching, (
            f"Nenhum step encontrado com o comando '{cmd}'. "
            "O workflow deve verificar a sintaxe de AULA13/bot_faturamento_avancado.py."
        )

    def test_py_compile_steps_are_distinct(self, all_steps: list[dict]):
        """
        Verifica que os steps de py_compile para AULA12 e AULA13 são steps
        distintos (não estão colapsados num único step).

        Validates: Requirements 6.1
        """
        steps_aula12 = _find_steps_with_command(
            all_steps, "py_compile AULA12/bot_cotacao_alerta.py"
        )
        steps_aula13 = _find_steps_with_command(
            all_steps, "py_compile AULA13/bot_faturamento_avancado.py"
        )
        # Steps distintos não devem ser o mesmo objeto
        ids_aula12 = {id(s) for s in steps_aula12}
        ids_aula13 = {id(s) for s in steps_aula13}
        assert ids_aula12.isdisjoint(ids_aula13), (
            "Os comandos py_compile de AULA12 e AULA13 devem estar em steps separados."
        )


# ---------------------------------------------------------------------------
# Teste de variável de ambiente MOCK_EMAIL (Requirements: 6.3)
# ---------------------------------------------------------------------------

class TestMockEmailEnvVar:

    def test_bot_cotacao_step_has_mock_email_env(self, all_steps: list[dict]):
        """
        Verifica que o step de execução do bot_cotacao_alerta.py define a
        variável de ambiente MOCK_EMAIL com o valor 'true'.

        Validates: Requirements 6.3
        """
        cmd = "bot_cotacao_alerta.py"
        execution_steps = _find_steps_with_command(all_steps, cmd)
        # Filtra somente os steps de execução (não os de py_compile)
        exec_steps = [
            s for s in execution_steps
            if "py_compile" not in s.get("run", "")
        ]
        assert exec_steps, (
            f"Nenhum step de execução encontrado para '{cmd}'."
        )
        step = exec_steps[0]
        env = step.get("env", {})
        assert "MOCK_EMAIL" in env, (
            "O step de execução de bot_cotacao_alerta.py deve definir a "
            "variável de ambiente MOCK_EMAIL."
        )
        assert str(env["MOCK_EMAIL"]).lower() == "true", (
            f"MOCK_EMAIL deve ser 'true', mas foi '{env['MOCK_EMAIL']}'. "
            "O valor 'true' evita envio real de e-mails em CI."
        )

    def test_bot_faturamento_step_does_not_require_mock_email(self, all_steps: list[dict]):
        """
        Verifica que o step de execução de bot_faturamento_avancado.py
        NÃO exige MOCK_EMAIL (diferente do bot de cotação).

        Validates: Requirements 6.3
        """
        cmd = "bot_faturamento_avancado.py"
        exec_steps = [
            s for s in _find_steps_with_command(all_steps, cmd)
            if "py_compile" not in s.get("run", "")
        ]
        if exec_steps:
            env = exec_steps[0].get("env", {})
            # Não é obrigatório ter MOCK_EMAIL — apenas validamos que não há
            # conflito. Este teste é informativo.
            assert isinstance(env, dict), "O campo 'env' do step deve ser um dict."


# ---------------------------------------------------------------------------
# Teste de verificação do app_rpa.log (Requirements: 6.4)
# ---------------------------------------------------------------------------

class TestAppRpaLogVerification:

    def test_step_verifica_app_rpa_log_exists(self, all_steps: list[dict]):
        """
        Verifica que existe ao menos um step cujo campo 'run' referencia
        'app_rpa.log', confirmando que o workflow valida a criação do log.

        Validates: Requirements 6.4
        """
        log_steps = _find_steps_with_command(all_steps, "app_rpa.log")
        assert log_steps, (
            "Nenhum step encontrado que verifique 'app_rpa.log'. "
            "O workflow deve confirmar que ao menos um dos bots gerou o arquivo de log."
        )

    def test_step_verifica_app_rpa_log_checks_presence(self, all_steps: list[dict]):
        """
        Verifica que o step de verificação do app_rpa.log usa uma condicional
        de existência do arquivo (padrão: '! -f app_rpa.log' ou '[ -f app_rpa.log ]').

        Validates: Requirements 6.4
        """
        log_steps = _find_steps_with_command(all_steps, "app_rpa.log")
        assert log_steps, "Nenhum step encontrado com referência a 'app_rpa.log'."

        step_run = log_steps[0].get("run", "")
        # O step deve testar a existência do arquivo com construções shell padrão
        presence_check = "! -f app_rpa.log" in step_run or "-f app_rpa.log" in step_run
        assert presence_check, (
            "O step de verificação de app_rpa.log deve incluir um teste de existência "
            "do arquivo (ex: '[ ! -f app_rpa.log ]' ou '[ -f app_rpa.log ]')."
        )

    def test_step_verifica_app_rpa_log_fails_if_absent(self, all_steps: list[dict]):
        """
        Verifica que o step de verificação do app_rpa.log contém 'exit 1'
        para falhar o job caso o arquivo não seja criado.

        Validates: Requirements 6.4
        """
        log_steps = _find_steps_with_command(all_steps, "app_rpa.log")
        assert log_steps, "Nenhum step encontrado com referência a 'app_rpa.log'."

        step_run = log_steps[0].get("run", "")
        assert "exit 1" in step_run, (
            "O step de verificação de app_rpa.log deve conter 'exit 1' para "
            "falhar o job quando o arquivo não for criado."
        )


# ---------------------------------------------------------------------------
# Sanidade geral do workflow
# ---------------------------------------------------------------------------

class TestWorkflowStructure:

    def test_workflow_file_exists(self):
        """Verifica que o arquivo ci_aulas_12_13.yml existe no repositório."""
        abs_path = os.path.abspath(WORKFLOW_PATH)
        assert os.path.isfile(abs_path), (
            f"Arquivo de workflow não encontrado: {abs_path}"
        )

    def test_workflow_uses_checkout_v4(self, all_steps: list[dict]):
        """Verifica que o workflow usa actions/checkout@v4. Validates: Requirements 9.1"""
        checkout_steps = [
            s for s in all_steps
            if "actions/checkout@v4" in s.get("uses", "")
        ]
        assert checkout_steps, "O workflow deve usar 'actions/checkout@v4'."

    def test_workflow_uses_setup_python_v5(self, all_steps: list[dict]):
        """Verifica que o workflow usa actions/setup-python@v5. Validates: Requirements 9.2"""
        setup_steps = [
            s for s in all_steps
            if "actions/setup-python@v5" in s.get("uses", "")
        ]
        assert setup_steps, "O workflow deve usar 'actions/setup-python@v5'."

    def test_workflow_uses_ubuntu_latest(self, workflow: dict):
        """Verifica que o job usa ubuntu-latest como runner. Validates: Requirements 9.6"""
        jobs = workflow.get("jobs", {})
        for job in jobs.values():
            runs_on = job.get("runs-on", "")
            assert runs_on == "ubuntu-latest", (
                f"O job deve usar 'ubuntu-latest', mas usa '{runs_on}'."
            )
