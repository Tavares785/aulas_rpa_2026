import time
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

pyautogui.press('win')

pyautogui.write('notepad', interval=0.1)
pyautogui.press('enter')

time.sleep(2)

texto = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"
pyautogui.write(texto, interval=0.05)

pyautogui.hotkey('ctrl', 's')
time.sleep(1)

pyautogui.write('status_bot.txt', interval=0.1)
pyautogui.press('enter')