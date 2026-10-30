"""
AULA 08 - Automacao Web com Selenium (site REAL, conteudo dinamico)
Exemplo do PROFESSOR

Tema didatico: webdriver, By.TAG_NAME / By.XPATH / By.CSS_SELECTOR,
espera explicita (WebDriverWait) e coleta de dados (web scraping) de uma
pagina que e renderizada por JavaScript.

Cenario: coletar TODOS os filmes do universo Harry Potter, agrupados por
CATEGORIA, a partir da pagina oficial:
    https://www.harrypotter.com/pt/discover/films

Por que Selenium e nao requests + BeautifulSoup?
    Esta pagina e uma SPA (Single Page Application). Se baixarmos o HTML "cru"
    com requests, a lista de filmes NAO aparece - ela e construida no navegador
    via JavaScript depois do carregamento. O Selenium controla um navegador de
    verdade, entao ele "enxerga" o conteudo ja renderizado. Otimo gancho para
    comparar as duas abordagens em aula (Modulo 3).

Estrutura observada na pagina (inspecao do DOM renderizado):
    - Cada CATEGORIA e um titulo <h2> terminando em "COLLECTION"
      (ex.: "HARRY POTTER COLLECTION", "FANTASTIC BEASTS COLLECTION").
    - Os FILMES daquela categoria sao os links <a> dentro da <section> que
      contem aquele <h2>. O nome do filme fica no texto do link e a URL no href.

Requer: pip install selenium
    (Selenium 4.6+ ja baixa o driver do Chrome automaticamente via Selenium Manager.)
"""
import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    webdriver = None
    print("Selenium nao instalado. Rode: pip install selenium")


URL_FILMES = "https://www.harrypotter.com/pt/discover/films"


def criar_navegador() -> "webdriver.Chrome":
    """Cria uma instancia do Chrome configurada para rodar sem abrir janela.

    As opcoes abaixo deixam a execucao estavel em servidores/CI e em maquinas
    de laboratorio. Em sala, remova '--headless=new' para VER o robo agindo.
    """
    options = Options()
    # options.add_argument("--headless=new")        # roda sem abrir janela
    options.add_argument("--no-sandbox")           # necessario em alguns Linux
    options.add_argument("--disable-dev-shm-usage")  # evita falta de memoria compartilhada
    options.add_argument("--window-size=1920,4000")  # janela alta: carrega tudo
    options.add_argument("--lang=pt-BR")
    return webdriver.Chrome(options=options)


def aceitar_cookies(driver) -> None:
    """Tenta fechar o banner de cookies, se ele aparecer.

    Em sites reais o banner de consentimento pode cobrir elementos e atrapalhar
    cliques. Aqui tratamos a ausencia do banner como algo NORMAL (nao e erro).
    """
    for texto in ("Accept", "Aceitar", "ACEITAR", "Aceito"):
        try:
            botao = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//button[contains(., '{texto}')]")
                )
            )
            botao.click()
            time.sleep(1)
            return
        except Exception:
            continue  # banner nao apareceu com esse texto; segue o fluxo


def coletar_filmes_por_categoria(driver) -> dict[str, list[dict[str, str]]]:
    """Le a pagina e devolve os filmes organizados por categoria.

    Retorno (estrutura de dados propria, facil de reaproveitar depois):
        {
            "HARRY POTTER COLLECTION": [
                {"titulo": "...", "url": "..."},
                ...
            ],
            "FANTASTIC BEASTS COLLECTION": [ ... ],
        }
    """
    driver.get(URL_FILMES)
    aceitar_cookies(driver)

    # ESPERA EXPLICITA: so seguimos quando pelo menos um <h2> de "COLLECTION"
    # ja foi renderizado pelo JavaScript. Muito mais confiavel que time.sleep fixo.
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(translate(., 'collection', 'COLLECTION'), 'COLLECTION')]")
        )
    )

    catalogo: dict[str, list[dict[str, str]]] = {}

    # 1) Localiza cada CATEGORIA (os <h2> que terminam em "COLLECTION").
    titulos = driver.find_elements(By.TAG_NAME, "h2")
    for titulo_el in titulos:
        categoria = titulo_el.text.strip()
        if not categoria.upper().endswith("COLLECTION"):
            continue  # ignora h2 que nao sao de categorias de filme

        # 2) Sobe ate a <section> que envolve o titulo e pega os links de filme.
        #    By.XPATH com "ancestor::" e um otimo exemplo de navegacao no DOM.
        try:
            secao = titulo_el.find_element(By.XPATH, "./ancestor::section[1]")
        except Exception:
            # Fallback: se nao houver <section>, sobe alguns niveis de <div>.
            secao = titulo_el.find_element(By.XPATH, "./ancestor::div[3]")

        filmes: list[dict[str, str]] = []
        for link in secao.find_elements(By.CSS_SELECTOR, "a[href*='/discover/films/']"):
            nome = link.text.strip()
            url = link.get_attribute("href") or ""
            if nome:  # so guarda links que tem nome de filme visivel
                filmes.append({"titulo": nome, "url": url})

        if filmes:
            catalogo[categoria] = filmes

    return catalogo


def imprimir_catalogo(catalogo: dict[str, list[dict[str, str]]]) -> None:
    """Mostra os filmes agrupados por categoria de forma legivel no terminal."""
    if not catalogo:
        print("Nenhum filme coletado (a pagina pode ter mudado de estrutura).")
        return

    total = 0
    for categoria, filmes in catalogo.items():
        print(f"\n=== {categoria} ({len(filmes)} filmes) ===")
        for i, filme in enumerate(filmes, start=1):
            print(f"  {i:>2}. {filme['titulo']}")
            print(f"      {filme['url']}")
            total += 1
    print(f"\nTotal geral: {total} filmes em {len(catalogo)} categorias.")


def main() -> None:
    driver = criar_navegador()
    try:
        catalogo = coletar_filmes_por_categoria(driver)
        imprimir_catalogo(catalogo)
    finally:
        driver.quit()  # SEMPRE fechar o navegador (evita processos zumbis)


if __name__ == "__main__":
    if webdriver is None:
        # Sem a lib instalada o guard de ImportError ja avisou; saida graciosa.
        raise SystemExit(0)

    try:
        main()
    except Exception as erro:
        # Degradacao graciosa: sem navegador/driver/internet, nao quebramos a aula.
        print("Navegador/driver/internet indisponivel; pulando a demo.")
        print("Detalhe tecnico:", erro.__class__.__name__, "-", erro)
        raise SystemExit(0)
