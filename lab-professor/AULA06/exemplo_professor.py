"""
AULA 06 - Controle de Perifericos e Fail-Safe (PyAutoGUI)
Exemplo do PROFESSOR

Tema didatico: pyautogui, FAILSAFE, PAUSE e coordenadas (X, Y).
Cenario divergente: registrar a conclusao de um "Checklist de Abertura de
Turno" em um sistema legado operado via interface grafica.

ATENCAO: o caminho padrao deste script NAO move mouse nem teclado. Ele apenas
demonstra as travas de seguranca e as coordenadas da tela. A acao que digita
no sistema legado fica desativada por padrao (flag + bloco comentado) para
rodar com seguranca em qualquer maquina.
Requer: pip install pyautogui
"""
import os
import time

pyautogui = None
# os.environ["DISPLAY"] = ":0"
if os.environ.get("DISPLAY"):
    try:
        import pyautogui
    except Exception as exc:
        print("PyAutoGUI nao pode ser inicializado neste ambiente.")
        print(f"Erro: {exc}")
        print("Rode: iniciar o script em uma sessão graphical autorizada.")
else:
    print("DISPLAY nao definido. A interacao graphical sera ignorada.")


# Flag de seguranca: por padrao a demo NAO interage com perifericos.
# Mude para True apenas em ambiente controlado e com um editor em foco.
PERMITIR_DIGITACAO: bool = False

# Dados do cenario (texto e nome de arquivo exclusivos deste exemplo).
MENSAGEM_TURNO: str = "Checklist de Abertura de Turno concluido"
ARQUIVO_REGISTRO: str = "registro_turno.sav"


def demo_seguranca() -> None:
    """Mostra as travas de seguranca ANTES de qualquer acao."""
    pyautogui.FAILSAFE = True   # mouse no canto superior esquerdo aborta
    pyautogui.PAUSE = 0.5       # pausa entre cada comando (mais seguro/visivel)

    largura, altura = pyautogui.size()
    x, y = pyautogui.position()
    print(f"Resolucao da tela: {largura} x {altura}")
    print(f"Posicao atual do mouse: X={x}, Y={y}")


def demo_registrar_turno() -> None:
    """Digita o registro de turno no sistema legado (desativado por padrao)."""
    print("Voce tem 3 segundos para deixar um editor de texto em foco...")
    time.sleep(3)
    # Caminho de alto risco: so executa quando a flag esta ligada em aula.
    pyautogui.write(MENSAGEM_TURNO, interval=0.05)  # digita char a char
    pyautogui.press("enter")
    # DICA DE AULA: aqui entraria o atalho de salvar e o nome do arquivo.
    # Em aula, demonstre como salvar o registro usando ARQUIVO_REGISTRO.


def imprimir_resumo() -> None:
    """Imprime um resumo do cenario sem tocar em perifericos."""
    print("Resumo do cenario (nenhum periferico foi movido):")
    print(f"  Mensagem planejada: {MENSAGEM_TURNO}")
    print(f"  Arquivo de registro: {ARQUIVO_REGISTRO}")
    print(f"  Digitacao habilitada: {PERMITIR_DIGITACAO}")


if __name__ == "__main__":
    if pyautogui is None:
        imprimir_resumo()
        raise SystemExit(0)

    demo_seguranca()

    # DICA DE AULA: so chamamos a digitacao quando a flag estiver ligada.
    # O caminho padrao mantem a flag desativada e apenas imprime o resumo.
    if PERMITIR_DIGITACAO:
        demo_registrar_turno()
    else:
        imprimir_resumo()

    print("Demo concluida. (digitacao desativada por seguranca por padrao)")
