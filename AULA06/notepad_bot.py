import time 

import pyautogui

import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

pyautogui.press('win')
pyautogui.write('notepad', interval=0.1)
time.sleep(1)
pyautogui.press('enter')

time.sleep(4)

pyperclip.copy("Relatório de Execução Automática - RPA PyAutoGUI Ativo!")
pyautogui.hotkey('ctrl', 'v')
pyautogui.hotkey('ctrl', 's')

time.sleep(2)

pyautogui.write("status_box.txt", interval=0.1)
pyautogui.press('enter')
