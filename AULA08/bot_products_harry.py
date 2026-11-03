import os
import re
import sys

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


LOGIN_URL = "https://www.cursoemvideo.com/minha-conta/"
MY_COURSES_URL = "https://www.cursoemvideo.com/meus-cursos/"
COURSE_CATALOG_URL = "https://www.cursoemvideo.com/cursos/"
COURSE_HOURS = re.compile(r"\[(\d+)\s*HORAS?\]", re.IGNORECASE)
MAX_RESULTS = 10


def find_login_form(driver):
    for form in driver.find_elements(By.TAG_NAME, "form"):
        if not form.is_displayed():
            continue

        inputs = form.find_elements(By.CSS_SELECTOR, "input")
        has_password = any(
            (element.get_attribute("type") or "").lower() == "password"
            for element in inputs
        )
        has_login_identifier = any(
            (element.get_attribute("name") or "").lower()
            in {"username", "user_login", "login", "email", "user_email", "log"}
            for element in inputs
        )
        form_classes = (form.get_attribute("class") or "").lower()
        if has_password and (
            has_login_identifier or "login" in form_classes
        ):
            return form

    return None


def describe_login_fields(form):
    labels = form.find_elements(By.TAG_NAME, "label")
    field_descriptions = []

    for element in form.find_elements(By.CSS_SELECTOR, "input"):
        field_type = (element.get_attribute("type") or "text").lower()
        if field_type not in {"text", "email", "password"}:
            continue

        field_id = element.get_attribute("id")
        label = next(
            (
                " ".join(item.text.split())
                for item in labels
                if field_id and item.get_attribute("for") == field_id
            ),
            "",
        )
        if not label:
            wrapping_labels = element.find_elements(By.XPATH, "./ancestor::label[1]")
            if wrapping_labels:
                label = " ".join(wrapping_labels[0].text.split())

        field_descriptions.append(
            {
                "rotulo": label or element.get_attribute("placeholder") or "Sem rótulo",
                "tipo": field_type,
                "obrigatorio": element.get_attribute("required") is not None,
            }
        )

    return field_descriptions


def page_main(driver):
    content_areas = driver.find_elements(
        By.CSS_SELECTOR, "main, #main, #content, .site-main"
    )
    return content_areas[0] if content_areas else driver


def collect_account_summary(driver):
    root = page_main(driver)
    summary = {"cursos": None, "terminados": None, "mensagem": None}

    for value in root.find_elements(By.CSS_SELECTOR, "strong"):
        parent_text = " ".join(value.find_element(By.XPATH, "..").text.split())
        if not value.text.isdigit():
            continue
        if re.search(r"\bcursos\b", parent_text, re.IGNORECASE):
            summary["cursos"] = int(value.text)
        elif re.search(r"\bterminado\b", parent_text, re.IGNORECASE):
            summary["terminados"] = int(value.text)

    for status in root.find_elements(By.CSS_SELECTOR, "[role='status']"):
        message = " ".join(status.text.split())
        if message:
            summary["mensagem"] = message
            break

    return summary


def collect_course_cards(driver):
    root = page_main(driver)
    results = []
    seen_urls = set()

    for heading in root.find_elements(By.CSS_SELECTOR, "h3"):
        title = " ".join(heading.text.split())
        if not title:
            continue

        container = heading
        course_url = ""
        description = ""
        for _ in range(6):
            links = container.find_elements(By.CSS_SELECTOR, "a[href]")
            course_link = next(
                (
                    link
                    for link in links
                    if "/curso/" in (link.get_attribute("href") or "")
                ),
                None,
            )
            paragraphs = [
                " ".join(paragraph.text.split())
                for paragraph in container.find_elements(By.TAG_NAME, "p")
                if paragraph.text.strip()
            ]
            if course_link:
                course_url = course_link.get_attribute("href") or ""
                if paragraphs:
                    description = paragraphs[0]
                    break
            parents = container.find_elements(By.XPATH, "./..")
            if not parents:
                break
            container = parents[0]

        if not course_url or course_url in seen_urls:
            continue

        hours_match = COURSE_HOURS.search(title)
        results.append(
            {
                "titulo": title,
                "carga_horaria": (
                    f"{hours_match.group(1)} horas" if hours_match else "Não informada"
                ),
                "descricao": description or "Descrição não disponível no catálogo.",
                "url": course_url,
            }
        )
        seen_urls.add(course_url)

    return results[:MAX_RESULTS]


def wait_for_page(wait):
    wait.until(
        lambda browser: browser.execute_script("return document.readyState")
        == "complete"
    )


def authenticate_manually(driver, wait):
    login_form = find_login_form(driver)
    if not login_form:
        print("Sessão já autenticada; seguindo para a área de cursos.")
        return

    print(
        "\nCampos do formulário encontrados no DOM "
        "(sem ler valores digitados):"
    )
    for field in describe_login_fields(login_form):
        required = "sim" if field["obrigatorio"] else "não"
        print(
            f"- {field['rotulo']} | tipo: {field['tipo']} "
            f"| obrigatório: {required}"
        )

    input(
        "\nFaça login na janela do Chrome. "
        "Quando a página mostrar sua conta, volte ao terminal "
        "e pressione Enter. O script não coleta usuário ou senha."
    )
    try:
        wait.until(lambda browser: find_login_form(browser) is None)
    except TimeoutException as error:
        raise RuntimeError(
            "O formulário de login ainda está visível. Conclua o "
            "login na janela do Chrome antes de continuar."
        ) from error
    print("Login confirmado.")


def print_course_report(driver, wait):
    account_summary = collect_account_summary(driver)
    print(f"\nPágina após o login: {driver.title}")
    print("Resumo da conta:")
    if account_summary["cursos"] is not None:
        print(f"- Cursos na conta: {account_summary['cursos']}")
    if account_summary["terminados"] is not None:
        print(f"- Cursos terminados: {account_summary['terminados']}")
    if account_summary["mensagem"]:
        print(f"- Estado da lista: {account_summary['mensagem']}")

    courses = collect_course_cards(driver)
    if not courses:
        print(
            "\nNenhum curso associado à conta foi listado. "
            "Consultando o catálogo público como alternativa."
        )
        driver.get(COURSE_CATALOG_URL)
        wait_for_page(wait)
        courses = collect_course_cards(driver)
        print(f"\nCatálogo público: {driver.title}")
    else:
        print("\nCursos associados à conta:")

    for item in courses:
        print(f"\n- {item['titulo']}")
        print(f"  Carga horária: {item['carga_horaria']}")
        print(f"  Descrição: {item['descricao']}")
        print(f"  Link: {item['url']}")
    print(f"\nQuantidade total coletada: {len(courses)}")
    if not courses:
        raise RuntimeError(
            "Não foi possível encontrar cards de cursos na conta nem "
            "no catálogo público."
        )


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    if (
        sys.platform.startswith("linux")
        and os.environ.get("WAYLAND_DISPLAY")
        and os.environ.get("DISPLAY")
    ):
        options.add_argument("--ozone-platform=x11")

    print("Abrindo o Curso em Vídeo no Chrome...")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 20)
        wait_for_page(wait)
        authenticate_manually(driver, wait)

        driver.get(MY_COURSES_URL)
        wait_for_page(wait)
        print_course_report(driver, wait)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
