# Controle de Periféricos e Segurança Fail-Safe

import time
import platform
import pyautogui
import pyperclip
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
sistema = platform.system()

if sistema == "Windows":
    tecla_sistema = "win"
    aplicativo = "notepad"
elif sistema == "Linux":
    tecla_sistema = "super"
    aplicativo = "gedit"
else:
    raise SystemExit("Sistema operacional não suportado.")

pyautogui.press(tecla_sistema)
time.sleep(1)

pyautogui.write(aplicativo, interval=0.1)
pyautogui.press("enter")

time.sleep(2)

texto = "Relatório de Execusão Automática - RPA PyAutoGUI Ativo!"

pyperclip.copy(texto)
pyautogui.hotkey("ctrl", "v")

pyautogui.hotkey("ctrl", "s")
time.sleep(1)

pyperclip.copy("status_bot.txt")
pyautogui.hotkey("ctrl", "v")

pyautogui.press("enter")

print("Execução do robô concluída.")
