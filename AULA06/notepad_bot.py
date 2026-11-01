import platform
import time
import pyautogui

# Configurações de segurança e velocidade
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


def executar_bot() -> None:
    """Executa o robô para abrir o editor de texto, digitar o relatório

    e salvar o arquivo com atalhos de teclado.
    """
    # 1. Pressiona a tecla Win (ou Super no Linux)
    pyautogui.press("win")

    # 2. Digita 'notepad' (ou 'gedit' no Linux) e pressiona Enter
    editor = "notepad" if platform.system() == "Windows" else "gedit"
    pyautogui.write(editor)
    pyautogui.press("enter")

    # 3. Aguarda 2 segundos para o aplicativo carregar
    time.sleep(2)

    # 4. Digita o texto de forma visível
    texto = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"
    pyautogui.write(texto, interval=0.05)

    # 5. Salva o arquivo: Ctrl + S, digita 'status_bot.txt' e confirma com Enter
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)
    pyautogui.write("status_bot.txt")
    pyautogui.press("enter")


if __name__ == "__main__":
    executar_bot()
