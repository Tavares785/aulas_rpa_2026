import time
import pyautogui
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

pyautogui.hotkey("win")
pyautogui.write("notepad", interval=0.05)
pyautogui.press("enter")

time.sleep(2)

pyautogui.hotkey("ctrl", "n")
time.sleep(1)

texto = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"

pyperclip.copy(texto)
pyautogui.hotkey("ctrl", "v")

pyautogui.hotkey("ctrl", "s")

time.sleep(1)

pyautogui.write("status_bot.txt", interval=0.05)
pyautogui.press("enter")