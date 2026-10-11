import time
import pyautogui
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

texto = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"

print("Iniciando o robo...")

pyautogui.press("win")
time.sleep(1)
pyautogui.write("notepad")
pyautogui.press("enter")

time.sleep(2)

pyautogui.hotkey("ctrl", "n")
time.sleep(1)

pyperclip.copy(texto)
pyautogui.hotkey("ctrl", "v")

pyautogui.hotkey("ctrl", "s")
time.sleep(2)
pyautogui.write("status_bot.txt")
pyautogui.press("enter")

print("Robo finalizado!")
