import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

pyautogui.hotkey('command', 'space')
time.sleep(1)
pyautogui.write('textedit')
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)

pyautogui.hotkey('command', 'n')
time.sleep(1)
pyautogui.hotkey('command', 'shift', 't')  # texto simples
time.sleep(1)

pyautogui.write('Relatorio de Execucao Automatica - RPA PyAutoGUI Ativo!', interval=0.05)

pyautogui.hotkey('command', 's')
time.sleep(2)
pyautogui.write('status_bot.txt')
pyautogui.press('enter') 
