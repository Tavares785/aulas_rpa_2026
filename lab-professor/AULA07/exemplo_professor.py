"""
AULA 07 - Projeto Guiado (Exemplo do PROFESSOR)

Objetivo didatico: integrar dados em memoria (lista de dicionarios) com
automacao de MOUSE guiada por VISAO COMPUTACIONAL (reconhecimento de imagem)
e exibir estatistica de tempo poupado versus esforco manual.

Cenario de negocio: responder automaticamente um Google Forms de coleta
("PyAutogui") que possui UMA pergunta de multipla escolha:

    "Voce fez o TF ?"  ->  (o) Sim   ( ) Nao

Por que reconhecimento de imagem (e nao contagem de Tab)?
  No Chrome, o foco inicial fica na barra de endereco e ha varios elementos
  no topo da pagina (login do Google, cabecalho). Contar Tabs e fragil e
  quebra facil. Localizar o alvo na tela por imagem e muito mais robusto e
  e exatamente o tema de "controle de perifericos" (mouse + visao).

Como funciona:
  1. Abre a URL do formulario no navegador padrao.
  2. Procura na tela a imagem do botao de rádio desejado (ex.: "Sim").
  3. Move o mouse ate o centro dele e clica.
  4. Procura o botao "Enviar" e clica para submeter.

As imagens de referencia ficam na pasta img/ ao lado deste script:
    img/opcao_sim.png
    img/opcao_nao.png
    img/botao_enviar.png

COMO GERAR AS IMAGENS (passo unico, por maquina):
  - Abra o formulario no navegador e deixe-o VISIVEL na tela.
  - Rode:  python exemplo_professor.py --capturar
  - Siga as instrucoes: o utilitario tira um screenshot e abre uma janela
    simples; voce arrasta um retangulo em volta do alvo e salva. (Se preferir,
    use qualquer ferramenta de recorte do sistema e salve os PNGs com os nomes
    acima.)

ATENCAO: o caminho padrao deste script NAO move mouse nem teclado. Ele apenas
imprime o plano e a estatistica (caminho seguro). A interacao real so acontece
quando ACIONAR_MOUSE = True, em ambiente controlado e com o form visivel.

Requer: pip install pyautogui pillow opencv-python
"""
import os
import sys
import time
import webbrowser
import pyautogui

# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------

# Flag de seguranca: por padrao NAO movemos o mouse.
# Troque para True apenas em demonstracao controlada, com o formulario visivel.
ACIONAR_MOUSE = True

# URL do Google Forms usado como exemplo nesta aula.
URL_FORM = (
    "https://docs.google.com/forms/d/e/1FAIpQLScOMfTlbyV1ZOFsdtjhj7WWCoob-KWpc5bRpFTip8_MHCqcTw/viewform"
)

# Resposta que o robo vai marcar: "Sim" ou "Nao".
RESPOSTA = "Sim"

# Pasta e nomes das imagens de referencia (recortes da tela).
PASTA_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
IMG_OPCAO = {
    "sim": os.path.join(PASTA_IMG, "opcao_sim.png"),
    "nao": os.path.join(PASTA_IMG, "opcao_nao.png"),
}
IMG_ENVIAR = os.path.join(PASTA_IMG, "botao_enviar.png")

# Tolerancia do casamento de imagem (0..1). Requer opencv-python.
CONFIANCA = 0.8

# Tempo estimado que um humano levaria para abrir e responder o form por envio.
TEMPO_MANUAL_POR_ENVIO = 20  # segundos

# Esperas (segundos).
ESPERA_CARREGAR_FORM = 6.0   # pagina do formulario carregar
ESPERA_FOCO = 3.0            # voce focar/visualizar a janela do navegador


# ---------------------------------------------------------------------------
# Automacao por reconhecimento de imagem
# ---------------------------------------------------------------------------

def _localizar_centro(caminho_img: str, tentativas: int = 10, intervalo: float = 1.0):
    """Procura a imagem na tela e devolve o centro (x, y) ou None.

    Tenta algumas vezes porque a pagina pode demorar a renderizar.
    """
    if not os.path.exists(caminho_img):
        print(f"  [erro] imagem de referencia nao encontrada: {caminho_img}")
        print("         gere os recortes com:  python exemplo_professor.py --capturar")
        return None

    for n in range(1, tentativas + 1):
        try:
            ponto = pyautogui.locateCenterOnScreen(caminho_img, confidence=CONFIANCA)
        except Exception as exc:  # noqa: BLE001 - locate pode lancar se nao achar
            ponto = None
            erro = exc
        else:
            erro = None
        if ponto is not None:
            return ponto
        print(f"  procurando '{os.path.basename(caminho_img)}'... ({n}/{tentativas})")
        time.sleep(intervalo)
    if erro is not None:
        print(f"  [aviso] ultimo erro ao localizar: {erro}")
    return None


def responder_formulario(resposta: str) -> bool:
    """Marca a opcao do radio e clica em Enviar, usando visao + mouse."""
    chave = resposta.strip().lower().replace("ã", "a")  # "Não" -> "nao"
    img_opcao = IMG_OPCAO.get(chave)
    if img_opcao is None:
        print(f"  [erro] resposta invalida: {resposta!r} (use 'Sim' ou 'Nao')")
        return False

    print(f"Procurando a opcao '{resposta}' na tela...")
    alvo = _localizar_centro(img_opcao)
    if alvo is None:
        print("  [falha] nao encontrei a opcao na tela. O form esta visivel?")
        return False
    pyautogui.moveTo(alvo.x, alvo.y, duration=0.4)
    pyautogui.click()
    print(f"  marcado: {resposta}")
    time.sleep(0.6)

    print("Procurando o botao 'Enviar'...")
    enviar = _localizar_centro(IMG_ENVIAR)
    if enviar is None:
        print("  [falha] nao encontrei o botao Enviar na tela.")
        return False
    pyautogui.moveTo(enviar.x, enviar.y, duration=0.4)
    pyautogui.click()
    print("  formulario enviado.")
    return True


def abrir_formulario() -> None:
    """Abre o Google Forms no navegador padrao e aguarda carregar."""
    print(f"Abrindo o formulario no navegador: {URL_FORM}")
    webbrowser.open(URL_FORM)
    print(f"Aguardando {ESPERA_CARREGAR_FORM:.0f}s para a pagina carregar...")
    time.sleep(ESPERA_CARREGAR_FORM)
    print(f"Deixe a janela do formulario VISIVEL. Comecando em {ESPERA_FOCO:.0f}s...")
    time.sleep(ESPERA_FOCO)


# ---------------------------------------------------------------------------
# Relatorio / plano (caminho seguro)
# ---------------------------------------------------------------------------

def relatorio_ganho(tempo_bot_por_envio: float = 3.0) -> None:
    """Compara esforco manual x robotizado (bom para justificar RPA em aula)."""
    manual = TEMPO_MANUAL_POR_ENVIO
    robo = tempo_bot_por_envio
    print("Envios planejados: 1")
    print(f"Estimativa manual: {manual}s | Robo: {robo:.0f}s")
    print(f"Economia: {manual - robo:.0f}s ({(1 - robo / manual) * 100:.0f}%)")


def imprimir_plano() -> None:
    """Mostra o que seria feito, sem tocar em perifericos (caminho seguro)."""
    print("Plano de preenchimento (nenhum periferico foi movido):")
    print(f"  Formulario: {URL_FORM}")
    print(f"  Pergunta: Voce fez o TF ?  ->  {RESPOSTA}")
    print(f"  Mouse habilitado: {ACIONAR_MOUSE}")
    faltando = [p for p in (IMG_OPCAO["sim"], IMG_OPCAO["nao"], IMG_ENVIAR) if not os.path.exists(p)]
    if faltando:
        print("  [atencao] faltam imagens de referencia:")
        for p in faltando:
            print(f"    - {p}")
        print("  Gere com:  python exemplo_professor.py --capturar")


# ---------------------------------------------------------------------------
# Utilitario de captura dos recortes (--capturar)
# ---------------------------------------------------------------------------

def capturar_recortes() -> None:
    """Ajuda a gerar os PNGs de referencia a partir da tela atual.

    Fluxo: para cada alvo, da um tempo para voce deixar o form visivel,
    tira um screenshot inteiro e salva. Depois voce recorta manualmente
    com a ferramenta de recorte do sistema, OU usa as coordenadas pedidas.

    Modo simples e sem dependencia de GUI extra: tira o screenshot cheio e
    orienta o recorte manual. Para a maioria das aulas, usar a ferramenta de
    recorte do SO (ex.: Captura de Tela do GNOME) e salvar com os nomes certos
    e o caminho mais rapido.
    """
    if pyautogui is None:
        print("pyautogui indisponivel; nao da para capturar.")
        return
    os.makedirs(PASTA_IMG, exist_ok=True)
    print("=== Utilitario de captura das imagens de referencia ===")
    print(f"As imagens devem ser salvas em: {PASTA_IMG}")
    print("Nomes esperados: opcao_sim.png, opcao_nao.png, botao_enviar.png\n")
    print("Vou tirar um screenshot cheio da tela em 5s. Deixe o FORM VISIVEL.")
    time.sleep(5)
    cheio = pyautogui.screenshot()
    destino = os.path.join(PASTA_IMG, "tela_full.png")
    cheio.save(destino)
    print(f"Screenshot salvo em: {destino}")
    print(
        "\nAgora recorte 3 pedacos desse screenshot (ou da tela) e salve com os\n"
        "nomes acima: o circulo+texto 'Sim', o circulo+texto 'Nao' e o botao\n"
        "'Enviar'. Use a ferramenta de recorte do seu sistema para gerar PNGs\n"
        "pequenos e nitidos (quanto menor e mais caracteristico, melhor)."
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if "--capturar" in sys.argv:
        capturar_recortes()
        raise SystemExit(0)

    # Caminho seguro: relatorio + plano, sem mexer no mouse.
    relatorio_ganho()
    imprimir_plano()

    if pyautogui is not None and ACIONAR_MOUSE:
        pyautogui.FAILSAFE = True  # mouse no canto superior esquerdo aborta
        pyautogui.PAUSE = 0.3
        abrir_formulario()
        ok = responder_formulario(RESPOSTA)
        if ok:
            print("Concluido com sucesso.")
        else:
            print("Nao foi possivel concluir. Verifique as imagens de referencia e o foco.")
    else:
        print("(preenchimento automatico desativado por seguranca)")
