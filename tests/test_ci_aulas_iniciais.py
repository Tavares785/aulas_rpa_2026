"""
Testes unitários para o workflow `.github/workflows/ci_aulas_iniciais.yml`.

Cobertura:
- Requisito 1.2: fail-fast: false na estratégia Matrix
- Requisito 1.4: flake8 com --exclude=.venv nos dois steps de linting
- Requisito 1.5: chave de cache com runner.os, matrix.python-version e hashFiles('requirements.txt')
"""

import pathlib
import pytest
import yaml


WORKFLOW_PATH = pathlib.Path(__file__).parent.parent / ".github" / "workflows" / "ci_aulas_iniciais.yml"


@pytest.fixture(scope="module")
def workflow():
    """Carrega e faz parse do YAML do workflow ci_aulas_iniciais.yml."""
    with open(WORKFLOW_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def job(workflow):
    """Retorna o primeiro (e único) job do workflow."""
    jobs = workflow.get("jobs", {})
    assert jobs, "O workflow não contém nenhum job definido"
    return next(iter(jobs.values()))


@pytest.fixture(scope="module")
def steps(job):
    """Retorna a lista de steps do job principal."""
    return job.get("steps", [])


@pytest.fixture(scope="module")
def flake8_steps(steps):
    """Retorna apenas os steps que executam o flake8 diretamente (não instalação)."""
    return [
        step for step in steps
        if "run" in step and any(
            line.strip().startswith("flake8") for line in step["run"].splitlines()
        )
    ]


# ---------------------------------------------------------------------------
# Requisito 1.2 — fail-fast: false na estratégia Matrix
# ---------------------------------------------------------------------------

class TestFailFast:
    def test_strategy_key_exists(self, job):
        """O job deve ter uma chave 'strategy' definida."""
        assert "strategy" in job, "Chave 'strategy' não encontrada no job"

    def test_fail_fast_is_false(self, job):
        """fail-fast deve estar explicitamente definido como false (Req 1.2)."""
        strategy = job["strategy"]
        assert "fail-fast" in strategy, "Chave 'fail-fast' ausente em 'strategy'"
        assert strategy["fail-fast"] is False, (
            f"Esperado fail-fast: false, mas encontrado: {strategy['fail-fast']}"
        )

    def test_matrix_python_versions(self, job):
        """Matrix deve incluir Python 3.10 e 3.11."""
        matrix = job["strategy"].get("matrix", {})
        python_versions = [str(v) for v in matrix.get("python-version", [])]
        assert "3.10" in python_versions, "Python 3.10 não encontrado na matrix"
        assert "3.11" in python_versions, "Python 3.11 não encontrado na matrix"


# ---------------------------------------------------------------------------
# Requisito 1.4 — --exclude=.venv nos dois steps do flake8
# ---------------------------------------------------------------------------

class TestFlake8ExcludeVenv:
    def test_two_flake8_steps_exist(self, flake8_steps):
        """Devem existir exatamente dois steps que executam flake8 (Req 1.4)."""
        assert len(flake8_steps) >= 2, (
            f"Esperados pelo menos 2 steps com flake8, encontrados: {len(flake8_steps)}"
        )

    def test_critical_syntax_step_excludes_venv(self, flake8_steps):
        """Step de erros críticos (E9, F63, F7, F82) deve conter --exclude=.venv (Req 1.4)."""
        critical_steps = [
            s for s in flake8_steps if "E9,F63,F7,F82" in s["run"] or "select=E9" in s["run"]
        ]
        assert critical_steps, "Step de erros críticos do flake8 não encontrado"
        step = critical_steps[0]
        assert "--exclude=.venv" in step["run"], (
            "Flag --exclude=.venv ausente no step de erros críticos do flake8"
        )

    def test_pep8_step_excludes_venv(self, flake8_steps):
        """Step de avaliação PEP8 (max-line-length) deve conter --exclude=.venv (Req 1.4)."""
        pep8_steps = [
            s for s in flake8_steps if "max-line-length" in s["run"]
        ]
        assert pep8_steps, "Step de avaliação PEP8 do flake8 não encontrado"
        step = pep8_steps[0]
        assert "--exclude=.venv" in step["run"], (
            "Flag --exclude=.venv ausente no step de avaliação PEP8 do flake8"
        )

    def test_all_flake8_steps_exclude_venv(self, flake8_steps):
        """Todos os steps flake8, sem exceção, devem conter --exclude=.venv (Req 1.4)."""
        for step in flake8_steps:
            assert "--exclude=.venv" in step["run"], (
                f"Step '{step.get('name', '(sem nome)')}' não contém --exclude=.venv"
            )


# ---------------------------------------------------------------------------
# Requisito 1.5 — chave de cache estruturada corretamente
# ---------------------------------------------------------------------------

class TestCacheStep:
    @pytest.fixture(scope="class")
    @classmethod
    def cache_step(cls, steps):
        """Localiza o step de cache pip no workflow."""
        cache_steps = [
            s for s in steps
            if s.get("uses", "").startswith("actions/cache")
        ]
        assert cache_steps, "Nenhum step com actions/cache encontrado no workflow"
        return cache_steps[0]

    def test_cache_uses_v4(self, cache_step):
        """O step de cache deve usar actions/cache@v4."""
        assert cache_step["uses"] == "actions/cache@v4", (
            f"Esperado actions/cache@v4, encontrado: {cache_step['uses']}"
        )

    def test_cache_key_contains_runner_os(self, cache_step):
        """A chave de cache deve incluir runner.os (Req 1.5)."""
        key = cache_step["with"]["key"]
        assert "runner.os" in key, (
            f"Chave de cache não contém 'runner.os': {key}"
        )

    def test_cache_key_contains_python_version(self, cache_step):
        """A chave de cache deve incluir matrix.python-version (Req 1.5)."""
        key = cache_step["with"]["key"]
        assert "matrix.python-version" in key, (
            f"Chave de cache não contém 'matrix.python-version': {key}"
        )

    def test_cache_key_contains_hash_files(self, cache_step):
        """A chave de cache deve incluir hashFiles referenciando requirements.txt (Req 1.5)."""
        key = cache_step["with"]["key"]
        assert "hashFiles(" in key, (
            f"Chave de cache não contém 'hashFiles(...)': {key}"
        )
        assert "requirements.txt" in key, (
            f"Chave de cache não referencia 'requirements.txt': {key}"
        )

    def test_cache_key_full_structure(self, cache_step):
        """A chave de cache deve seguir o padrão completo definido no design (Req 1.5)."""
        key = cache_step["with"]["key"]
        # Verifica que a chave contém os três componentes exigidos juntos
        assert all(component in key for component in ["runner.os", "matrix.python-version", "hashFiles"]), (
            f"Chave de cache não contém todos os componentes obrigatórios. Chave atual: {key}"
        )
