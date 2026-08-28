"""
Testes unitários para o workflow .github/workflows/ci_documentos.yml.

Validates: Requirements 10.1, 10.2
"""

import os
import pytest
import yaml

WORKFLOW_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    ".github",
    "workflows",
    "ci_documentos.yml",
)


@pytest.fixture(scope="module")
def workflow() -> dict:
    """Carrega e faz parse do arquivo YAML do workflow."""
    abs_path = os.path.abspath(WORKFLOW_PATH)
    assert os.path.isfile(abs_path), (
        f"Workflow não encontrado: {abs_path}"
    )
    with open(abs_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _get_all_steps(workflow: dict) -> list[dict]:
    """Retorna a lista plana de todos os steps de todos os jobs."""
    steps = []
    jobs = workflow.get("jobs", {})
    for job in jobs.values():
        steps.extend(job.get("steps", []))
    return steps


# ---------------------------------------------------------------------------
# 1. Verifica que o workflow usa actions/checkout@v4
# ---------------------------------------------------------------------------

def test_uses_checkout_v4(workflow: dict):
    """O workflow deve usar actions/checkout@v4 como step de checkout."""
    steps = _get_all_steps(workflow)
    uses_values = [step.get("uses", "") for step in steps]
    assert any("actions/checkout@v4" in u for u in uses_values), (
        "Nenhum step usa 'actions/checkout@v4'. "
        f"Actions encontradas: {uses_values}"
    )


# ---------------------------------------------------------------------------
# 2. Verifica ausência de actions/setup-python (workflow usa somente bash)
# ---------------------------------------------------------------------------

def test_does_not_use_setup_python(workflow: dict):
    """O workflow NÃO deve usar actions/setup-python (usa somente bash)."""
    steps = _get_all_steps(workflow)
    uses_values = [step.get("uses", "") for step in steps]
    setup_python_steps = [u for u in uses_values if "setup-python" in u]
    assert not setup_python_steps, (
        f"O workflow não deveria usar 'setup-python', mas encontrou: {setup_python_steps}"
    )


# ---------------------------------------------------------------------------
# 3. Verifica que os arquivos Markdown obrigatórios são mencionados nos steps
# ---------------------------------------------------------------------------

REQUIRED_MARKDOWN_FILES = [
    "AULA02/lab-02.md",
    "AULA02/lab-02_resp.md",
    "AULA03/lab-03.md",
    "AULA03/lab-03_resp.md",
    "AULA05/AVALIACAO_PROCESSO.md",
]


def _get_all_run_scripts(workflow: dict) -> str:
    """Concatena todos os scripts 'run' dos steps em uma única string."""
    steps = _get_all_steps(workflow)
    scripts = []
    for step in steps:
        run = step.get("run", "")
        if run:
            scripts.append(run)
    return "\n".join(scripts)


@pytest.mark.parametrize("md_file", REQUIRED_MARKDOWN_FILES)
def test_required_markdown_file_mentioned_in_steps(md_file: str, workflow: dict):
    """Cada arquivo Markdown obrigatório deve ser mencionado em algum step 'run'."""
    all_scripts = _get_all_run_scripts(workflow)
    assert md_file in all_scripts, (
        f"O arquivo '{md_file}' não foi encontrado em nenhum step 'run' do workflow."
    )


# ---------------------------------------------------------------------------
# 4. Sanidade geral do workflow
# ---------------------------------------------------------------------------

def test_workflow_has_jobs(workflow: dict):
    """O workflow deve definir ao menos um job."""
    jobs = workflow.get("jobs", {})
    assert jobs, "O workflow não possui jobs definidos."


def test_workflow_triggers_push_and_pr(workflow: dict):
    """O workflow deve ser disparado por push e pull_request na branch main."""
    on = workflow.get("on", {})
    # O campo 'on' pode ser string ou dict; aqui esperamos dict
    assert isinstance(on, dict), "O campo 'on' deve ser um dicionário com os triggers."
    assert "push" in on, "O trigger 'push' não está configurado no workflow."
    assert "pull_request" in on, "O trigger 'pull_request' não está configurado no workflow."

    push_branches = on.get("push", {}).get("branches", [])
    pr_branches = on.get("pull_request", {}).get("branches", [])

    assert "main" in push_branches, (
        f"O trigger 'push' deve incluir a branch 'main'. Branches encontradas: {push_branches}"
    )
    assert "main" in pr_branches, (
        f"O trigger 'pull_request' deve incluir a branch 'main'. Branches encontradas: {pr_branches}"
    )
