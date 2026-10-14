"""Script de automação do Bloco de Notas para o Lab 06 (PyAutoGUI)."""

import platform
import time
import pyautogui

# Configuração de segurança operacional
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


def executar_bot() -> None:
    """Executa o fluxo de automação do Bloco de Notas."""
    sistema = platform.system().lower()

    # 1. Pressiona a tecla Win (ou Super no Linux)
    if "linux" in sistema:
        pyautogui.press("super")
        app = "gedit"
    else:
        pyautogui.press("win")
        app = "notepad"

    time.sleep(1)

    # 2. Digita o nome do editor e pressiona Enter
    pyautogui.write(app, interval=0.1)
    pyautogui.press("enter")

    # 3. Aguarda 2 segundos para o aplicativo carregar
    time.sleep(2)

    # 4. Digita o texto solicitado
    texto = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"
    pyautogui.write(texto, interval=0.05)

    time.sleep(1)

    # 5. Atalho para salvar (Ctrl + S)
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)

    # 6. Digita o nome do arquivo e confirma
    pyautogui.write("status_bot.txt", interval=0.05)
    pyautogui.press("enter")


if __name__ == "__main__":
    executar_bot()
