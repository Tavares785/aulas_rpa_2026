"""
AULA 09 - Dropdowns, Pop-ups e Iframes (Selenium avancado)
Exemplo do PROFESSOR

Tema didatico: classe Select (dropdown), captura de Alert (pop-up nativo),
troca de contexto com switch_to.frame / switch_to.default_content (iframe)
e controle de multiplas abas com window_handles / switch_to.window.

Cenario divergente: em vez de depender de paginas publicas na internet, o
exemplo monta em tempo de execucao uma pagina HTML LOCAL (arquivo temporario)
com um painel de escala de trabalho. Assim o roteiro roda sem rede e os dados
pertencem a um dominio proprio (turnos e setores operacionais).

Requer: pip install selenium
Observacao: sem navegador/driver disponivel, o script degrada de forma
graciosa e encerra com codigo de saida 0.
"""
import os
import shutil
import tempfile
import time

# Tempo de pausa (em segundos) entre cada acao, para os alunos acompanharem.
# Aumente este valor se quiser que o robo va ainda mais devagar.
PAUSA = 2

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.chrome.options import Options
except ImportError:
    webdriver = None
    print("Selenium nao instalado. Rode: pip install selenium")


# Conteudo da pagina principal: um painel com select de turno/setor, um botao
# que dispara alert() e um iframe proprio que carrega outra pagina local.
PAGINA_PAINEL = """<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <title>Painel de Escala</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 90px 30px 30px; font-size: 18px; }
    h1 { color: #2c3e50; }
    label { font-weight: bold; }
    select, button { font-size: 18px; padding: 6px 10px; margin: 8px 0; }
    button { cursor: pointer; background: #2980b9; color: #fff; border: none; border-radius: 4px; }
    iframe { margin-top: 15px; border: 2px solid #bbb; border-radius: 4px; }

    /* Banner fixo no topo mostrando a acao atual do robo */
    #robo_status {
      position: fixed; top: 0; left: 0; right: 0;
      background: #2c3e50; color: #fff;
      font-size: 20px; font-weight: bold;
      padding: 16px 24px; box-shadow: 0 2px 8px rgba(0,0,0,.3);
      z-index: 9999;
    }

    /* Efeito de destaque aplicado via JS no elemento-alvo */
    .robo-destaque {
      outline: 4px solid #f1c40f !important;
      box-shadow: 0 0 12px 4px rgba(241, 196, 15, .9) !important;
      background: #fff8d6 !important;
      transition: all .2s ease-in-out;
    }
  </style>
</head>
<body>
  <!-- Banner de status: o robo escreve aqui o que esta fazendo -->
  <div id="robo_status">Robo pronto. Aguardando inicio...</div>

  <h1>Painel de Escala Operacional</h1>

  <!-- Dropdown proprio: turnos de trabalho -->
  <label for="escala">Turno:</label>
  <select id="escala">
    <option value="manha">Turno Matutino</option>
    <option value="tarde">Turno Vespertino</option>
    <option value="noite">Turno Noturno</option>
  </select>

  <br>

  <!-- Botao que dispara um alert nativo do navegador -->
  <button id="confirmar" onclick="alert('Escala registrada com sucesso')">
    Confirmar escala
  </button>

  <!-- Botao que abre uma SEGUNDA aba (target=_blank) -->
  <button id="abrir_relatorio"
          onclick="window.open('SRC_RELATORIO', '_blank')">
    Abrir relatorio em nova aba
  </button>

  <br>

  <!-- Iframe proprio com documento aninhado -->
  <iframe id="quadro_setor" src="SRC_SETOR" width="320" height="80"></iframe>
</body>
</html>
"""

# Documento aberto em uma SEGUNDA aba (outra janela/handle do navegador).
PAGINA_RELATORIO = """<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <title>Relatorio de Escala</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 90px 30px 30px; font-size: 18px; }
    h1 { color: #16a085; }
    #robo_status {
      position: fixed; top: 0; left: 0; right: 0;
      background: #16a085; color: #fff;
      font-size: 20px; font-weight: bold;
      padding: 16px 24px; box-shadow: 0 2px 8px rgba(0,0,0,.3);
      z-index: 9999;
    }
    .robo-destaque {
      outline: 4px solid #f1c40f !important;
      box-shadow: 0 0 12px 4px rgba(241, 196, 15, .9) !important;
      background: #fff8d6 !important;
    }
  </style>
</head>
<body>
  <div id="robo_status">Esta e a SEGUNDA aba (relatorio).</div>
  <h1>Relatorio de Escala</h1>
  <p id="resumo_relatorio">Total de colaboradores escalados: 42</p>
</body>
</html>
"""

# Documento carregado dentro do iframe (contexto separado da pagina principal).
PAGINA_SETOR = """<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <title>Setor</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 10px; font-size: 16px; }
    .robo-destaque {
      outline: 4px solid #f1c40f !important;
      box-shadow: 0 0 12px 4px rgba(241, 196, 15, .9) !important;
      background: #fff8d6 !important;
    }
  </style>
</head>
<body>
  <p id="setor_responsavel">Setor responsavel: Logistica Interna</p>
</body>
</html>
"""


def gerar_paginas_locais() -> tuple[str, str, str]:
    # Cria tres arquivos .html temporarios: o painel, o conteudo do iframe
    # e o relatorio (aberto em uma segunda aba).
    # Retorna os caminhos absolutos para uso e posterior limpeza.
    pasta = tempfile.mkdtemp(prefix="aula09_")
    caminho_setor = os.path.join(pasta, "setor.html")
    caminho_relatorio = os.path.join(pasta, "relatorio.html")
    caminho_painel = os.path.join(pasta, "painel.html")

    with open(caminho_setor, "w", encoding="utf-8") as arq:
        arq.write(PAGINA_SETOR)

    with open(caminho_relatorio, "w", encoding="utf-8") as arq:
        arq.write(PAGINA_RELATORIO)

    # Aponta os src do iframe e do botao de nova aba via URL file://
    url_setor = "file://" + caminho_setor
    url_relatorio = "file://" + caminho_relatorio
    html_painel = (
        PAGINA_PAINEL
        .replace("SRC_SETOR", url_setor)
        .replace("SRC_RELATORIO", url_relatorio)
    )
    with open(caminho_painel, "w", encoding="utf-8") as arq:
        arq.write(html_painel)

    return caminho_painel, caminho_setor, caminho_relatorio


def status(driver: "webdriver.Chrome", mensagem: str) -> None:
    # Escreve a mensagem no banner fixo do topo (visivel na pagina).
    print(">>", mensagem)
    driver.execute_script(
        "var b=document.getElementById('robo_status'); if(b){b.textContent=arguments[0];}",
        mensagem,
    )


def destacar(driver: "webdriver.Chrome", elemento) -> None:
    # Rola a pagina ate o elemento e aplica a borda amarela de destaque,
    # para o aluno ver EXATAMENTE onde o robo vai agir.
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});"
        "arguments[0].classList.add('robo-destaque');",
        elemento,
    )
    time.sleep(PAUSA)


def remover_destaque(driver: "webdriver.Chrome", elemento) -> None:
    # Remove o destaque do elemento apos a acao.
    driver.execute_script(
        "arguments[0].classList.remove('robo-destaque');", elemento
    )


def demo_dropdown(driver: "webdriver.Chrome") -> None:
    # Demonstra a classe Select escolhendo a opcao pelo texto visivel.
    status(driver, "[1/4] DROPDOWN: localizando o menu de turnos...")
    time.sleep(PAUSA)
    elemento = driver.find_element(By.ID, "escala")
    destacar(driver, elemento)
    status(driver, "[1/4] DROPDOWN: selecionando 'Turno Noturno'...")
    campo = Select(elemento)
    campo.select_by_visible_text("Turno Noturno")
    print("Turno selecionado:", campo.first_selected_option.text)
    time.sleep(PAUSA)
    remover_destaque(driver, elemento)


def demo_alert(driver: "webdriver.Chrome") -> None:
    # Dispara o alert via botao, captura o texto e confirma com accept().
    status(driver, "[2/4] POP-UP: localizando o botao de confirmacao...")
    time.sleep(PAUSA)
    botao = driver.find_element(By.ID, "confirmar")
    destacar(driver, botao)
    status(driver, "[2/4] POP-UP: clicando no botao para abrir o alert...")
    botao.click()
    time.sleep(PAUSA)
    # IMPORTANTE: com um alert nativo aberto, o Chrome NAO permite rodar
    # outros comandos (nem execute_script). Por isso NAO chamamos status()
    # aqui -- apenas lemos o texto e confirmamos o alert.
    alerta = driver.switch_to.alert
    texto_alerta = alerta.text
    print("Texto do alert:", texto_alerta)
    time.sleep(PAUSA)
    alerta.accept()
    time.sleep(PAUSA)
    # Agora que o alert foi fechado, ja podemos voltar a escrever no banner.
    status(driver, "[2/4] POP-UP: alert dizia -> " + texto_alerta)
    status(driver, "[2/4] POP-UP: alert confirmado (accept).")
    print("Alert confirmado (accept).")
    time.sleep(PAUSA)
    remover_destaque(driver, botao)


def demo_iframe(driver: "webdriver.Chrome") -> None:
    # Troca o contexto para o iframe, le o conteudo e volta ao documento base.
    iframe = driver.find_element(By.ID, "quadro_setor")
    destacar(driver, iframe)
    status(driver, "[3/4] IFRAME: entrando no contexto do iframe...")
    time.sleep(PAUSA)
    driver.switch_to.frame("quadro_setor")
    corpo = driver.find_element(By.ID, "setor_responsavel")
    destacar(driver, corpo)
    print("Conteudo dentro do iframe:", corpo.text)
    time.sleep(PAUSA)
    driver.switch_to.default_content()
    remover_destaque(driver, iframe)
    # De volta ao documento principal: o select voltou a ser visivel.
    status(driver, "[3/4] IFRAME: de volta ao documento principal.")
    print("Fora do iframe, select presente:",
          driver.find_element(By.ID, "escala").is_displayed())
    time.sleep(PAUSA)


def demo_troca_aba(driver: "webdriver.Chrome") -> None:
    # Demonstra o controle de multiplas abas usando window_handles.
    # Guarda o identificador (handle) da aba original para poder voltar.
    aba_original = driver.current_window_handle
    status(driver, "[4/4] ABAS: localizando o botao que abre nova aba...")
    time.sleep(PAUSA)
    botao = driver.find_element(By.ID, "abrir_relatorio")
    destacar(driver, botao)

    status(driver, "[4/4] ABAS: clicando para abrir o relatorio em outra aba...")
    botao.click()
    time.sleep(PAUSA)
    remover_destaque(driver, botao)

    # Agora existem 2 handles. Localiza a aba nova (diferente da original).
    handles = driver.window_handles
    print("Abas abertas agora:", len(handles))
    aba_nova = [h for h in handles if h != aba_original][0]

    # Troca o foco do robo para a nova aba.
    driver.switch_to.window(aba_nova)
    status(driver, "[4/4] ABAS: foco movido para a SEGUNDA aba (relatorio).")
    time.sleep(PAUSA)
    resumo = driver.find_element(By.ID, "resumo_relatorio")
    destacar(driver, resumo)
    print("Titulo da nova aba:", driver.title)
    print("Conteudo lido na nova aba:", resumo.text)
    time.sleep(PAUSA)

    # Fecha a aba do relatorio e devolve o foco para a aba original.
    status(driver, "[4/4] ABAS: fechando a segunda aba e voltando a original...")
    driver.close()
    driver.switch_to.window(aba_original)
    time.sleep(PAUSA)
    status(driver, "[4/4] ABAS: de volta ao painel. Aba atual: " + driver.title)
    print("Foco de volta na aba original:", driver.title)
    time.sleep(PAUSA)


def executar_roteiro() -> None:
    # Gera as paginas locais e executa as quatro demonstracoes em sequencia.
    caminho_painel, _caminho_setor, _caminho_relatorio = gerar_paginas_locais()
    pasta_temporaria = os.path.dirname(caminho_painel)
    driver = None
    opcoes = Options()
    # opcoes.add_argument("--headless=new")  # ligue para rodar sem abrir janela
    try:
        driver = webdriver.Chrome(options=opcoes)
        driver.maximize_window()
        driver.implicitly_wait(5)
        driver.get("file://" + caminho_painel)
        status(driver, "Pagina carregada. Observem o painel antes das acoes...")
        time.sleep(PAUSA)
        demo_dropdown(driver)
        demo_alert(driver)
        demo_iframe(driver)
        demo_troca_aba(driver)

        status(driver, "Roteiro concluido! Fechando o navegador em instantes...")
        print("\nRoteiro concluido. Fechando o navegador em instantes...")
        time.sleep(PAUSA)
    finally:
        # SEMPRE fechar o navegador e remover a pasta temporaria inteira.
        if driver is not None:
            driver.quit()
        shutil.rmtree(pasta_temporaria, ignore_errors=True)


def main() -> None:
    # Sem selenium instalado, encerra de forma graciosa (saida zero).
    if webdriver is None:
        raise SystemExit(0)
    try:
        executar_roteiro()
    except Exception as erro:
        # DICA DE AULA: sem navegador/driver instalado o Selenium levanta
        # excecao. Aqui degradamos a execucao e seguimos com saida zero,
        # para o exemplo rodar em qualquer maquina sem travar.
        print("Navegador/driver indisponivel. Exemplo encerrado:", erro)
        raise SystemExit(0)


if __name__ == "__main__":
    main()
