"""
Testes unitários para o workflow .github/workflows/ci_aula_14.yml.

Valida a estrutura do workflow de validação de estrutura de repositório (AULA14).
Requirements: 7.2, 7.3, 7.4, 7.6
"""

import os
import yaml
import pytest


WORKFLOW_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    ".github",
    "workflows",
    "ci_aula_14.yml",
)


@pytest.fixture(scope="module")
def workflow() -> dict:
    """Carrega e faz parse do arquivo YAML do workflow ci_aula_14.yml."""
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


def _get_all_run_scripts(workflow: dict) -> str:
    """Concatena todos os scripts 'run' dos steps em uma única string."""
    steps = _get_all_steps(workflow)
    return "\n".join(step.get("run", "") for step in steps if "run" in step)


def _get_run_step_for_file(steps: list[dict], filename: str) -> dict | None:
    """
    Retorna o primeiro step cujo script 'run' menciona o arquivo dado.
    Retorna None se não encontrar.
    """
    for step in steps:
        run = step.get("run", "")
        if filename in run:
            return step
    return None


# ---------------------------------------------------------------------------
# Sanidade básica
# ---------------------------------------------------------------------------

def test_workflow_file_exists():
    """O arquivo ci_aula_14.yml deve existir em .github/workflows/."""
    assert os.path.isfile(os.path.abspath(WORKFLOW_PATH)), (
        f"Arquivo não encontrado: {WORKFLOW_PATH}"
    )


def test_workflow_has_jobs(workflow: dict):
    """O workflow deve definir ao menos um job."""
    assert workflow.get("jobs"), "O workflow não contém jobs."


def test_workflow_triggers_push_and_pr(workflow: dict):
    """O workflow deve ser disparado por push e pull_request na branch main.

    Nota: PyYAML parseia a chave 'on' do YAML como booleano True em Python.
    O campo é acessado via True (bool) ou 'on' dependendo da versão do parser.
    """
    # PyYAML converte a chave YAML 'on' para o booleano Python True
    on = workflow.get(True) or workflow.get("on", {})
    assert on, "O campo 'on' (triggers) não foi encontrado ou está vazio no workflow."
    assert isinstance(on, dict), "O campo 'on' deve ser um dicionário com os triggers."

    assert "push" in on, (
        f"O trigger 'push' não está configurado. Triggers encontrados: {list(on.keys())}"
    )
    assert "pull_request" in on, (
        f"O trigger 'pull_request' não está configurado. Triggers encontrados: {list(on.keys())}"
    )

    push_branches = on.get("push", {}).get("branches", [])
    pr_branches = on.get("pull_request", {}).get("branches", [])

    assert "main" in push_branches, (
        f"O trigger 'push' deve incluir 'main'. Branches encontradas: {push_branches}"
    )
    assert "main" in pr_branches, (
        f"O trigger 'pull_request' deve incluir 'main'. Branches encontradas: {pr_branches}"
    )


def test_uses_checkout_v4(workflow: dict):
    """O workflow deve usar actions/checkout@v4 como step de checkout."""
    steps = _get_all_steps(workflow)
    uses_values = [step.get("uses", "") for step in steps]
    assert any("actions/checkout@v4" in u for u in uses_values), (
        "Nenhum step usa 'actions/checkout@v4'. "
        f"Actions encontradas: {uses_values}"
    )


def test_does_not_use_setup_python(workflow: dict):
    """O workflow NÃO deve usar actions/setup-python (usa somente bash)."""
    steps = _get_all_steps(workflow)
    setup_python_steps = [
        step.get("uses", "") for step in steps
        if "setup-python" in step.get("uses", "")
    ]
    assert not setup_python_steps, (
        f"O workflow não deveria usar 'setup-python', mas encontrou: {setup_python_steps}"
    )


# ---------------------------------------------------------------------------
# Requisito 7.2 — Step dedicado para requirements.txt com AVISO
# ---------------------------------------------------------------------------

def test_requirements_txt_has_dedicated_step(workflow: dict):
    """
    Deve existir um step dedicado que mencione 'requirements.txt'.
    Requirements: 7.2
    """
    steps = _get_all_steps(workflow)
    step = _get_run_step_for_file(steps, "requirements.txt")
    assert step is not None, (
        "Nenhum step 'run' menciona 'requirements.txt'. "
        "O workflow deve ter um step dedicado para verificar esse arquivo."
    )


def test_requirements_txt_step_emits_aviso(workflow: dict):
    """
    O step de verificação de requirements.txt deve emitir 'AVISO' quando o arquivo estiver ausente.
    Requirements: 7.2
    """
    steps = _get_all_steps(workflow)
    step = _get_run_step_for_file(steps, "requirements.txt")
    assert step is not None, "Nenhum step menciona 'requirements.txt'."

    run_script = step.get("run", "")
    assert "AVISO" in run_script, (
        "O step de 'requirements.txt' não emite 'AVISO'. "
        f"Script atual:\n{run_script}"
    )


# ---------------------------------------------------------------------------
# Requisito 7.3 — Step dedicado para .gitignore com AVISO
# ---------------------------------------------------------------------------

def test_gitignore_has_dedicated_step(workflow: dict):
    """
    Deve existir um step dedicado que mencione '.gitignore'.
    Requirements: 7.3
    """
    steps = _get_all_steps(workflow)
    step = _get_run_step_for_file(steps, ".gitignore")
    assert step is not None, (
        "Nenhum step 'run' menciona '.gitignore'. "
        "O workflow deve ter um step dedicado para verificar esse arquivo."
    )


def test_gitignore_step_emits_aviso(workflow: dict):
    """
    O step de verificação de .gitignore deve emitir 'AVISO' quando o arquivo estiver ausente.
    Requirements: 7.3
    """
    steps = _get_all_steps(workflow)
    step = _get_run_step_for_file(steps, ".gitignore")
    assert step is not None, "Nenhum step menciona '.gitignore'."

    run_script = step.get("run", "")
    assert "AVISO" in run_script, (
        "O step de '.gitignore' não emite 'AVISO'. "
        f"Script atual:\n{run_script}"
    )


# ---------------------------------------------------------------------------
# Requisito 7.4 — Step dedicado para README.md com AVISO
# ---------------------------------------------------------------------------

def test_readme_md_has_dedicated_step(workflow: dict):
    """
    Deve existir um step dedicado que mencione 'README.md'.
    Requirements: 7.4
    """
    steps = _get_all_steps(workflow)
    step = _get_run_step_for_file(steps, "README.md")
    assert step is not None, (
        "Nenhum step 'run' menciona 'README.md'. "
        "O workflow deve ter um step dedicado para verificar esse arquivo."
    )


def test_readme_md_step_emits_aviso(workflow: dict):
    """
    O step de verificação de README.md deve emitir 'AVISO' quando o arquivo estiver ausente.
    Requirements: 7.4
    """
    steps = _get_all_steps(workflow)
    step = _get_run_step_for_file(steps, "README.md")
    assert step is not None, "Nenhum step menciona 'README.md'."

    run_script = step.get("run", "")
    assert "AVISO" in run_script, (
        "O step de 'README.md' não emite 'AVISO'. "
        f"Script atual:\n{run_script}"
    )


# ---------------------------------------------------------------------------
# Requisito 7.6 — Step final (resumo) contém exit 0 explícito
# ---------------------------------------------------------------------------

def test_final_step_contains_exit_0(workflow: dict):
    """
    O step final deve conter 'exit 0' explícito para garantir o caráter pedagógico
    (o job sempre conclui com sucesso independentemente dos arquivos ausentes).
    Requirements: 7.6
    """
    steps = _get_all_steps(workflow)
    run_steps = [s for s in steps if "run" in s]
    assert run_steps, "Nenhum step com 'run' encontrado no workflow."

    last_run_step = run_steps[-1]
    run_script = last_run_step.get("run", "")
    assert "exit 0" in run_script, (
        "O step final (resumo) não contém 'exit 0' explícito. "
        f"Script do último step 'run':\n{run_script}"
    )


# ---------------------------------------------------------------------------
# Verificação combinada — os três arquivos obrigatórios têm steps separados
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("required_file", [
    "requirements.txt",
    ".gitignore",
    "README.md",
])
def test_each_required_file_has_dedicated_step(required_file: str, workflow: dict):
    """
    Cada um dos três arquivos obrigatórios deve ter seu próprio step dedicado.
    Requirements: 7.2, 7.3, 7.4
    """
    steps = _get_all_steps(workflow)
    step = _get_run_step_for_file(steps, required_file)
    assert step is not None, (
        f"Nenhum step 'run' menciona '{required_file}'. "
        "O workflow deve ter um step dedicado por arquivo obrigatório."
    )


@pytest.mark.parametrize("required_file", [
    "requirements.txt",
    ".gitignore",
    "README.md",
])
def test_each_required_file_step_emits_aviso(required_file: str, workflow: dict):
    """
    O step de cada arquivo obrigatório deve emitir 'AVISO' para cobrir o caso de ausência.
    Requirements: 7.2, 7.3, 7.4
    """
    steps = _get_all_steps(workflow)
    step = _get_run_step_for_file(steps, required_file)
    assert step is not None, f"Nenhum step menciona '{required_file}'."

    run_script = step.get("run", "")
    assert "AVISO" in run_script, (
        f"O step para '{required_file}' não emite 'AVISO'. "
        f"Script atual:\n{run_script}"
    )
