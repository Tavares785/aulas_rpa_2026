"""
Testes unitários para o workflow .github/workflows/ci_aula_04.yml

Valida a estrutura do workflow de testes unitários com cobertura (AULA04).
Requirements: 2.2, 2.4
"""

import os
import yaml
import pytest


WORKFLOW_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    ".github",
    "workflows",
    "ci_aula_04.yml",
)


@pytest.fixture(scope="module")
def workflow():
    """Carrega e parseia o YAML do workflow ci_aula_04.yml."""
    with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def job(workflow):
    """Retorna o primeiro (e único) job definido no workflow."""
    jobs = workflow.get("jobs", {})
    assert jobs, "O workflow não contém nenhum job."
    return next(iter(jobs.values()))


@pytest.fixture(scope="module")
def steps(job):
    """Retorna a lista de steps do job principal."""
    return job.get("steps", [])


# ---------------------------------------------------------------------------
# Testes de estrutura básica
# ---------------------------------------------------------------------------

def test_workflow_file_exists():
    """O arquivo ci_aula_04.yml deve existir em .github/workflows/."""
    assert os.path.isfile(WORKFLOW_PATH), (
        f"Arquivo não encontrado: {WORKFLOW_PATH}"
    )


def test_workflow_has_jobs(workflow):
    """O workflow deve definir ao menos um job."""
    assert workflow.get("jobs"), "O workflow não contém jobs."


# ---------------------------------------------------------------------------
# Requisito 2.2 — fail-fast: false na estratégia Matrix
# ---------------------------------------------------------------------------

def test_fail_fast_is_false(job):
    """
    O job deve ter strategy.fail-fast definido como False.
    Garante que ambas as versões Python executem mesmo se uma falhar.
    Requirements: 2.2
    """
    strategy = job.get("strategy", {})
    assert strategy, "O job não possui uma seção 'strategy'."
    assert "fail-fast" in strategy, (
        "A seção 'strategy' não contém a chave 'fail-fast'."
    )
    assert strategy["fail-fast"] is False, (
        f"Esperado fail-fast: false, mas encontrado: {strategy['fail-fast']}"
    )


def test_matrix_python_versions(job):
    """
    A matrix deve incluir Python 3.10 e 3.11.
    Requirements: 2.2
    """
    matrix = job.get("strategy", {}).get("matrix", {})
    python_versions = matrix.get("python-version", [])
    assert "3.10" in python_versions, "Python 3.10 não está na matrix."
    assert "3.11" in python_versions, "Python 3.11 não está na matrix."


# ---------------------------------------------------------------------------
# Requisito 2.4 — Step de cache com chave estruturada corretamente
# ---------------------------------------------------------------------------

def test_cache_step_exists(steps):
    """
    Deve existir um step que usa actions/cache@v4.
    Requirements: 2.4 (via Requirement 9.3)
    """
    cache_steps = [
        s for s in steps
        if isinstance(s.get("uses"), str) and s["uses"].startswith("actions/cache@v4")
    ]
    assert cache_steps, "Nenhum step com 'actions/cache@v4' foi encontrado."


def test_cache_key_contains_runner_os(steps):
    """
    A chave de cache deve referenciar runner.os para diferenciar por SO.
    Requirements: 2.4
    """
    cache_steps = [
        s for s in steps
        if isinstance(s.get("uses"), str) and s["uses"].startswith("actions/cache@v4")
    ]
    assert cache_steps, "Nenhum step de cache encontrado."

    cache_key = cache_steps[0].get("with", {}).get("key", "")
    assert "runner.os" in cache_key, (
        f"A chave de cache não contém 'runner.os'. Chave atual: {cache_key!r}"
    )


def test_cache_key_contains_matrix_python_version(steps):
    """
    A chave de cache deve referenciar matrix.python-version para diferenciar por versão Python.
    Requirements: 2.4
    """
    cache_steps = [
        s for s in steps
        if isinstance(s.get("uses"), str) and s["uses"].startswith("actions/cache@v4")
    ]
    assert cache_steps, "Nenhum step de cache encontrado."

    cache_key = cache_steps[0].get("with", {}).get("key", "")
    assert "matrix.python-version" in cache_key, (
        f"A chave de cache não contém 'matrix.python-version'. Chave atual: {cache_key!r}"
    )


def test_cache_key_contains_hash_files_requirements(steps):
    """
    A chave de cache deve referenciar hashFiles('requirements.txt') para invalidar ao mudar dependências.
    Requirements: 2.4
    """
    cache_steps = [
        s for s in steps
        if isinstance(s.get("uses"), str) and s["uses"].startswith("actions/cache@v4")
    ]
    assert cache_steps, "Nenhum step de cache encontrado."

    cache_key = cache_steps[0].get("with", {}).get("key", "")
    assert "hashFiles('requirements.txt')" in cache_key, (
        f"A chave de cache não contém \"hashFiles('requirements.txt')\". "
        f"Chave atual: {cache_key!r}"
    )


# ---------------------------------------------------------------------------
# Requisito 2.4 — Flag --cov-fail-under=80 no comando pytest
# ---------------------------------------------------------------------------

def _get_pytest_run_steps(steps):
    """
    Retorna os steps que executam o pytest como comando (não apenas instalam).
    Um step de execução pytest contém 'pytest' no run E não é apenas instalação.
    Linhas que começam com 'pytest' ou contêm '&& pytest' ou '\npytest' são execuções reais.
    """
    run_steps = []
    for step in steps:
        if "run" not in step:
            continue
        run_text = step["run"]
        # Verifica se alguma linha do script começa com 'pytest' (execução direta)
        lines = run_text.splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("pytest ") or stripped == "pytest":
                run_steps.append(step)
                break
    return run_steps


def test_pytest_step_exists(steps):
    """Deve existir ao menos um step que executa o pytest como comando."""
    pytest_steps = _get_pytest_run_steps(steps)
    assert pytest_steps, "Nenhum step com execução de pytest encontrado."


def test_cov_fail_under_80(steps):
    """
    O comando pytest deve conter --cov-fail-under=80.
    Garante que o job falha se a cobertura estiver abaixo de 80%.
    Requirements: 2.4
    """
    pytest_steps = _get_pytest_run_steps(steps)
    assert pytest_steps, "Nenhum step com execução de pytest encontrado."

    pytest_run = pytest_steps[0]["run"]
    assert "--cov-fail-under=80" in pytest_run, (
        f"Flag '--cov-fail-under=80' não encontrada no comando pytest. "
        f"Comando atual:\n{pytest_run}"
    )


def test_cov_report_term_missing(steps):
    """
    O comando pytest deve conter --cov-report=term-missing para exibir linhas não cobertas.
    Requirements: 2.4
    """
    pytest_steps = _get_pytest_run_steps(steps)
    assert pytest_steps, "Nenhum step com execução de pytest encontrado."

    pytest_run = pytest_steps[0]["run"]
    assert "--cov-report=term-missing" in pytest_run, (
        f"Flag '--cov-report=term-missing' não encontrada no comando pytest. "
        f"Comando atual:\n{pytest_run}"
    )


def test_pytest_ignores_venv(steps):
    """
    O comando pytest deve conter --ignore=.venv para não cobrir dependências instaladas.
    Requirements: 2.5
    """
    pytest_steps = _get_pytest_run_steps(steps)
    assert pytest_steps, "Nenhum step com execução de pytest encontrado."

    pytest_run = pytest_steps[0]["run"]
    assert "--ignore=.venv" in pytest_run, (
        f"Flag '--ignore=.venv' não encontrada no comando pytest. "
        f"Comando atual:\n{pytest_run}"
    )
