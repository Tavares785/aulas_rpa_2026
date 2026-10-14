import sys
import time

import pyautogui
import pyperclip


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


def main() -> None:
    if sys.platform.startswith("win"):
        launcher_key = "win"
        app_name = "notepad"
    elif sys.platform.startswith("linux"):
        launcher_key = "super"
        app_name = "gedit"
    else:
        raise RuntimeError("Este script oferece suporte apenas a Windows e Linux.")

    pyautogui.press(launcher_key)
    pyautogui.write(app_name, interval=0.1)
    pyautogui.press("enter")
    time.sleep(2)

    texto = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"
    pyperclip.copy(texto)
    pyautogui.hotkey("ctrl", "v")

    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)
    pyautogui.write("status_bot.txt")
    pyautogui.press("enter")


if __name__ == "__main__":
    main()
